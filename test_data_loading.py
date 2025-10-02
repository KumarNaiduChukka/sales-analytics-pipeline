import pandas as pd
import sys

def test_data_loading():
    """Test if the data can be loaded correctly"""
    try:
        # Load the data
        df = pd.read_csv('data/processed/FactSales_clean.csv')
        
        print("✅ Data loaded successfully!")
        print(f"📊 Data shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        print(f"📅 Date range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"💰 Total Revenue: ${df['Revenue'].sum():,.2f}")
        print(f"📦 Total Orders: {df['OrderID'].nunique():,}")
        print(f"👥 Unique Customers: {df['CustomerID'].nunique():,}")
        print(f"🌍 Regions: {df['Region'].unique()}")
        print(f"📦 Categories: {df['Category'].unique()}")
        print(f"👤 Segments: {df['Segment'].unique()}")
        
        # Check for missing values
        missing_values = df.isnull().sum()
        if missing_values.sum() > 0:
            print("\n⚠️ Missing values found:")
            print(missing_values[missing_values > 0])
        else:
            print("\n✅ No missing values found!")
            
        return True
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

if __name__ == "__main__":
    success = test_data_loading()
    sys.exit(0 if success else 1)
