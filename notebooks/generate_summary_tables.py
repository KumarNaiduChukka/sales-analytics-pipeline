import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# Set paths
RAW_DATA_PATH = '../data/raw/Sample - Superstore.csv'
PROCESSED_DATA_PATH = '../data/processed/FactSales_clean.csv'
SUMMARY_TABLES_PATH = '../outputs/tables/Summary_Tables.xlsx'

# Create directories if they don't exist
os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
os.makedirs(os.path.dirname(SUMMARY_TABLES_PATH), exist_ok=True)

# Load the data
print("Loading data...")
# Try different encodings to handle potential encoding issues
try:
    df = pd.read_csv(RAW_DATA_PATH, encoding='utf-8')
except UnicodeDecodeError:
    try:
        df = pd.read_csv(RAW_DATA_PATH, encoding='latin1')
    except UnicodeDecodeError:
        df = pd.read_csv(RAW_DATA_PATH, encoding='cp1252')

# Print original column names for debugging
print(f"Original columns: {df.columns.tolist()}")

# Create a copy of the dataframe with normalized column names
df_clean = df.copy()

# Rename columns to match required schema
print("Renaming columns...")
column_mapping = {
    'Row ID': 'RowID',
    'Order ID': 'OrderID',
    'Order Date': 'Date',
    'Ship Date': 'ShipDate',
    'Ship Mode': 'ShipMode',
    'Customer ID': 'CustomerID',
    'Customer Name': 'CustomerName',
    'Segment': 'Segment',
    'Country': 'Country',
    'City': 'City',
    'State': 'State',
    'Postal Code': 'PostalCode',
    'Region': 'Region',
    'Product ID': 'ProductID',
    'Category': 'Category',
    'Sub-Category': 'SubCategory',
    'Product Name': 'Product',
    'Sales': 'Revenue',
    'Quantity': 'Quantity',
    'Discount': 'Discount',
    'Profit': 'Profit'
}

# Apply column renaming
df_clean.rename(columns=column_mapping, inplace=True)

# Convert date columns to datetime
print("Converting date columns...")
df_clean['Date'] = pd.to_datetime(df_clean['Date'])
df_clean['ShipDate'] = pd.to_datetime(df_clean['ShipDate'])

# Feature engineering - create date-related columns
print("Creating date features...")
df_clean['Year'] = df_clean['Date'].dt.year
df_clean['Month'] = df_clean['Date'].dt.month
df_clean['YearMonth'] = df_clean['Date'].dt.strftime('%Y-%m')
df_clean['Quarter'] = df_clean['Date'].dt.quarter
df_clean['MonthStart'] = df_clean['Date'].dt.to_period('M').dt.to_timestamp()

# Standardize categorical values
print("Standardizing categorical values...")
categorical_cols = ['ShipMode', 'Segment', 'Country', 'City', 'State', 'Region', 'Category', 'SubCategory']
for col in categorical_cols:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].str.strip().str.title()

# Calculate UnitPrice if missing
print("Calculating UnitPrice...")
if 'UnitPrice' not in df_clean.columns:
    df_clean['UnitPrice'] = df_clean['Revenue'] / df_clean['Quantity']

# Anomaly detection
print("Performing anomaly detection...")

# Z-score method for per-order revenue
order_revenue = df_clean.groupby('OrderID')['Revenue'].sum().reset_index()
order_revenue['RevenueZScore'] = (order_revenue['Revenue'] - order_revenue['Revenue'].mean()) / order_revenue['Revenue'].std()
order_revenue['IsAnomalyZScore'] = abs(order_revenue['RevenueZScore']) > 3.0

# Rolling median deviation by region-quarter
region_quarter_revenue = df_clean.groupby(['Region', 'Year', 'Quarter'])['Revenue'].sum().reset_index()
region_quarter_revenue = region_quarter_revenue.sort_values(['Region', 'Year', 'Quarter'])

# Calculate rolling median and deviation for each region
anomalies_region_quarter = []
for region in region_quarter_revenue['Region'].unique():
    region_data = region_quarter_revenue[region_quarter_revenue['Region'] == region].copy()
    if len(region_data) >= 3:  # Need at least 3 quarters for rolling median
        region_data['RollingMedian'] = region_data['Revenue'].rolling(window=3, min_periods=1).median()
        region_data['MedianDeviation'] = abs(region_data['Revenue'] - region_data['RollingMedian']) / region_data['RollingMedian']
        region_data['IsAnomalyMedian'] = region_data['MedianDeviation'] > 0.5  # 50% threshold
        anomalies_region_quarter.append(region_data[region_data['IsAnomalyMedian']])

# Combine anomalies
if anomalies_region_quarter:
    anomalies_df = pd.concat(anomalies_region_quarter)
    anomalies_df = anomalies_df[['Region', 'Year', 'Quarter', 'Revenue', 'RollingMedian', 'MedianDeviation']]
    anomalies_df.rename(columns={'MedianDeviation': 'DeviationPercentage'}, inplace=True)
    anomalies_df['DeviationPercentage'] = anomalies_df['DeviationPercentage'] * 100  # Convert to percentage
    anomalies_df['AnomalyType'] = 'Region-Quarter Revenue Deviation'
else:
    anomalies_df = pd.DataFrame(columns=['Region', 'Year', 'Quarter', 'Revenue', 'RollingMedian', 'DeviationPercentage', 'AnomalyType'])

# Add order-level anomalies
order_anomalies = df_clean.merge(order_revenue[order_revenue['IsAnomalyZScore']][['OrderID', 'Revenue', 'RevenueZScore']], on='OrderID')
if not order_anomalies.empty:
    order_anomalies_summary = order_anomalies.groupby('OrderID').agg({
        'Date': 'first',
        'Region': 'first',
        'Revenue_x': 'sum',
        'RevenueZScore': 'first'
    }).reset_index()
    order_anomalies_summary.rename(columns={'Revenue_x': 'Revenue', 'RevenueZScore': 'ZScore'}, inplace=True)
    order_anomalies_summary['AnomalyType'] = 'Order Revenue Z-Score'
    order_anomalies_summary['Year'] = order_anomalies_summary['Date'].dt.year
    order_anomalies_summary['Quarter'] = order_anomalies_summary['Date'].dt.quarter

# Save cleaned data
print("Saving cleaned data...")
df_clean.to_csv(PROCESSED_DATA_PATH, index=False)

# Generate summary tables
print("Generating summary tables...")

# 1. Revenue by Month
revenue_by_month = df_clean.groupby('YearMonth').agg({
    'Revenue': 'sum',
    'OrderID': pd.Series.nunique,
    'Profit': 'sum'
}).reset_index()
revenue_by_month.rename(columns={'OrderID': 'OrderCount'}, inplace=True)
revenue_by_month['AvgOrderValue'] = revenue_by_month['Revenue'] / revenue_by_month['OrderCount']
revenue_by_month.sort_values('YearMonth', inplace=True)

# 2. Revenue by Region
revenue_by_region = df_clean.groupby(['Region', 'Year', 'Quarter']).agg({
    'Revenue': 'sum',
    'OrderID': pd.Series.nunique,
    'Profit': 'sum'
}).reset_index()
revenue_by_region.rename(columns={'OrderID': 'OrderCount'}, inplace=True)
revenue_by_region['AvgOrderValue'] = revenue_by_region['Revenue'] / revenue_by_region['OrderCount']
revenue_by_region.sort_values(['Year', 'Quarter', 'Revenue'], ascending=[True, True, False], inplace=True)

# 3. Top Customers
top_customers = df_clean.groupby('CustomerName').agg({
    'Revenue': 'sum',
    'OrderID': pd.Series.nunique,
    'Profit': 'sum'
}).reset_index()
top_customers.rename(columns={'OrderID': 'OrderCount'}, inplace=True)
top_customers['AvgOrderValue'] = top_customers['Revenue'] / top_customers['OrderCount']
top_customers.sort_values('Revenue', ascending=False, inplace=True)
top_customers = top_customers.head(20)  # Top 20 customers

# 4. Top Products
top_products = df_clean.groupby(['Category', 'SubCategory', 'Product']).agg({
    'Revenue': 'sum',
    'Quantity': 'sum',
    'Profit': 'sum'
}).reset_index()
top_products['ProfitMargin'] = (top_products['Profit'] / top_products['Revenue']) * 100
top_products.sort_values('Revenue', ascending=False, inplace=True)
top_products = top_products.head(20)  # Top 20 products

# 5. Anomalies table (combine both types of anomalies)
# This would be populated with the anomalies detected above

# Export all tables to Excel
print("Exporting tables to Excel...")
with pd.ExcelWriter(SUMMARY_TABLES_PATH) as writer:
    revenue_by_month.to_excel(writer, sheet_name='Revenue_by_Month', index=False)
    revenue_by_region.to_excel(writer, sheet_name='Revenue_by_Region', index=False)
    top_customers.to_excel(writer, sheet_name='Top_Customers', index=False)
    top_products.to_excel(writer, sheet_name='Top_Products', index=False)
    
    # Export anomalies if they exist
    if not anomalies_df.empty or not order_anomalies.empty:
        if 'order_anomalies_summary' in locals():
            # Select relevant columns for Excel export
            order_cols = ['OrderID', 'Region', 'Year', 'Quarter', 'Revenue', 'ZScore', 'AnomalyType']
            order_anomalies_for_excel = order_anomalies_summary[order_cols]
            
            # Combine with region-quarter anomalies if they exist
            if not anomalies_df.empty:
                # Ensure compatible columns for concatenation
                region_cols = ['Region', 'Year', 'Quarter', 'Revenue', 'RollingMedian', 'DeviationPercentage', 'AnomalyType']
                region_anomalies_for_excel = anomalies_df[region_cols]
                
                # Add placeholder columns to make dataframes compatible
                order_anomalies_for_excel['RollingMedian'] = np.nan
                order_anomalies_for_excel['DeviationPercentage'] = np.nan
                region_anomalies_for_excel['OrderID'] = 'N/A'
                region_anomalies_for_excel['ZScore'] = np.nan
                
                # Combine anomalies
                all_anomalies = pd.concat([order_anomalies_for_excel, region_anomalies_for_excel])
                all_anomalies.to_excel(writer, sheet_name='Anomalies', index=False)
            else:
                order_anomalies_for_excel.to_excel(writer, sheet_name='Anomalies', index=False)
        elif not anomalies_df.empty:
            anomalies_df.to_excel(writer, sheet_name='Anomalies', index=False)
    
    # Also export the cleaned data
    df_clean.head(1000).to_excel(writer, sheet_name='FactSales_clean_sample', index=False)

print(f"Summary tables exported to {SUMMARY_TABLES_PATH}")

# Save data quality metrics to JSON
data_quality = {
    "row_count": len(df_clean),
    "null_counts": {col: df_clean[col].isnull().sum() for col in df_clean.columns},
    "duplicate_order_ids": df_clean['OrderID'].duplicated().sum(),
    "date_range": {
        "min_date": df_clean['Date'].min().strftime('%Y-%m-%d'),
        "max_date": df_clean['Date'].max().strftime('%Y-%m-%d')
    },
    "numeric_stats": {
        "Revenue": {
            "min": df_clean['Revenue'].min(),
            "max": df_clean['Revenue'].max(),
            "mean": df_clean['Revenue'].mean(),
            "median": df_clean['Revenue'].median()
        },
        "Quantity": {
            "min": df_clean['Quantity'].min(),
            "max": df_clean['Quantity'].max(),
            "mean": df_clean['Quantity'].mean(),
            "median": df_clean['Quantity'].median()
        }
    },
    "categorical_counts": {
        "Region": df_clean['Region'].value_counts().to_dict(),
        "Category": df_clean['Category'].value_counts().to_dict(),
        "Segment": df_clean['Segment'].value_counts().to_dict()
    }
}

# Save data quality report to JSON file
DATA_QUALITY_PATH = '../outputs/data_quality_report.json'
os.makedirs(os.path.dirname(DATA_QUALITY_PATH), exist_ok=True)
with open(DATA_QUALITY_PATH, 'w') as f:
    json.dump(data_quality, f, indent=4, default=str)
print(f"Data quality report saved to {DATA_QUALITY_PATH}")

# Print summary
print("\nData Processing Summary:")
print(f"Total rows processed: {len(df_clean)}")
print(f"Date range: {data_quality['date_range']['min_date']} to {data_quality['date_range']['max_date']}")
print(f"Total revenue: ${df_clean['Revenue'].sum():,.2f}")
print(f"Total profit: ${df_clean['Profit'].sum():,.2f}")
print(f"Number of unique orders: {df_clean['OrderID'].nunique()}")
print(f"Number of unique customers: {df_clean['CustomerName'].nunique()}")
print(f"Number of unique products: {df_clean['Product'].nunique()}")

print("\nProcess completed successfully!")