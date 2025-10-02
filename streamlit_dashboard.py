import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .insight-box {
        background: #f8f9fa;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    
    .stSlider > div > div > div {
        background-color: #1f77b4;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .sidebar .sidebar-content .block-container {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/processed/FactSales_clean.csv')
        # Convert date columns
        df['Date'] = pd.to_datetime(df['Date'])
        df['ShipDate'] = pd.to_datetime(df['ShipDate'])
        df['MonthStart'] = pd.to_datetime(df['MonthStart'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Main dashboard
def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Sales Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Comprehensive EDA Dashboard for Sales Data Analysis</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # Sidebar filters
    st.sidebar.markdown("## 🔍 Filters & Controls")
    
    # Date range filter
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Region filter
    regions = ['All'] + sorted(df['Region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Select Region", regions)
    
    # Segment filter
    segments = ['All'] + sorted(df['Segment'].unique().tolist())
    selected_segment = st.sidebar.selectbox("Select Customer Segment", segments)
    
    # Category filter
    categories = ['All'] + sorted(df['Category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Select Product Category", categories)
    
    # Apply filters
    filtered_df = df.copy()
    
    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['Date'].dt.date >= date_range[0]) & 
            (filtered_df['Date'].dt.date <= date_range[1])
        ]
    
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    
    if selected_segment != 'All':
        filtered_df = filtered_df[filtered_df['Segment'] == selected_segment]
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    
    # Key Metrics
    st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_revenue = filtered_df['Revenue'].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with col2:
        total_orders = filtered_df['OrderID'].nunique()
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col3:
        avg_order_value = filtered_df.groupby('OrderID')['Revenue'].sum().mean()
        st.metric("Average Order Value", f"${avg_order_value:,.2f}")
    
    with col4:
        total_profit = filtered_df['Profit'].sum()
        profit_margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0
        st.metric("Profit Margin", f"{profit_margin:.1f}%")
    
    # Revenue Trend Analysis
    st.markdown('<div class="section-header">📈 Revenue Trend Analysis</div>', unsafe_allow_html=True)
    
    # Monthly revenue trend
    monthly_revenue = filtered_df.groupby(['Year', 'Month']).agg({
        'Revenue': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).reset_index()
    monthly_revenue['Date'] = pd.to_datetime(monthly_revenue[['Year', 'Month']].assign(day=1))
    
    fig_trend = px.line(
        monthly_revenue, 
        x='Date', 
        y='Revenue',
        title='Monthly Revenue Trend',
        color_discrete_sequence=['#1f77b4']
    )
    fig_trend.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Insight for revenue trend
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Revenue Trend Insights:</strong><br>
        • The chart shows revenue patterns over time, helping identify seasonal trends and growth patterns<br>
        • Look for peaks and valleys to understand business cycles<br>
        • Compare with profit trends to assess profitability consistency
    </div>
    """, unsafe_allow_html=True)
    
    # Regional Analysis
    st.markdown('<div class="section-header">🌍 Regional Performance Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by region
        region_revenue = filtered_df.groupby('Region').agg({
            'Revenue': 'sum',
            'Profit': 'sum',
            'OrderID': 'nunique'
        }).reset_index()
        
        fig_region = px.pie(
            region_revenue, 
            values='Revenue', 
            names='Region',
            title='Revenue Distribution by Region',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_region.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        # Top regions by profit
        region_profit = filtered_df.groupby('Region')['Profit'].sum().sort_values(ascending=True)
        
        fig_profit = px.bar(
            x=region_profit.values,
            y=region_profit.index,
            orientation='h',
            title='Profit by Region',
            color=region_profit.values,
            color_continuous_scale='Viridis'
        )
        fig_profit.update_layout(
            xaxis_title="Profit ($)",
            yaxis_title="Region",
            showlegend=False
        )
        st.plotly_chart(fig_profit, use_container_width=True)
    
    # Regional insights
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Regional Analysis Insights:</strong><br>
        • Identify which regions contribute most to revenue and profit<br>
        • Look for regions with high revenue but low profit margins<br>
        • Consider regional market penetration and growth opportunities
    </div>
    """, unsafe_allow_html=True)
    
    # Product Category Analysis
    st.markdown('<div class="section-header">📦 Product Category Performance</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue by category
        category_revenue = filtered_df.groupby('Category').agg({
            'Revenue': 'sum',
            'Quantity': 'sum'
        }).reset_index()
        
        fig_category = px.bar(
            category_revenue,
            x='Category',
            y='Revenue',
            title='Revenue by Product Category',
            color='Revenue',
            color_continuous_scale='Blues'
        )
        fig_category.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        # Subcategory analysis
        subcategory_analysis = filtered_df.groupby(['Category', 'SubCategory']).agg({
            'Revenue': 'sum',
            'Profit': 'sum'
        }).reset_index()
        
        fig_subcategory = px.treemap(
            subcategory_analysis,
            path=['Category', 'SubCategory'],
            values='Revenue',
            title='Revenue by Subcategory (Treemap)',
            color='Profit',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_subcategory, use_container_width=True)
    
    # Category insights
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Product Category Insights:</strong><br>
        • Analyze which product categories drive the most revenue<br>
        • The treemap shows both revenue size and profitability (green = profitable, red = loss)<br>
        • Focus on high-revenue, high-profit categories for growth strategies
    </div>
    """, unsafe_allow_html=True)
    
    # Customer Segment Analysis
    st.markdown('<div class="section-header">👥 Customer Segment Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Segment performance
        segment_analysis = filtered_df.groupby('Segment').agg({
            'Revenue': 'sum',
            'Profit': 'sum',
            'OrderID': 'nunique',
            'CustomerID': 'nunique'
        }).reset_index()
        segment_analysis['Avg_Order_Value'] = segment_analysis['Revenue'] / segment_analysis['OrderID']
        
        fig_segment = px.scatter(
            segment_analysis,
            x='Revenue',
            y='Profit',
            size='OrderID',
            color='Segment',
            title='Segment Performance: Revenue vs Profit',
            hover_data=['CustomerID', 'Avg_Order_Value']
        )
        st.plotly_chart(fig_segment, use_container_width=True)
    
    with col2:
        # Customer count by segment
        customer_count = filtered_df.groupby('Segment')['CustomerID'].nunique().reset_index()
        
        fig_customers = px.bar(
            customer_count,
            x='Segment',
            y='CustomerID',
            title='Number of Customers by Segment',
            color='CustomerID',
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig_customers, use_container_width=True)
    
    # Segment insights
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Customer Segment Insights:</strong><br>
        • The scatter plot shows revenue vs profit relationship for each segment<br>
        • Bubble size represents number of orders<br>
        • Identify segments with high revenue but low profitability for optimization
    </div>
    """, unsafe_allow_html=True)
    
    # Sales Performance by Time
    st.markdown('<div class="section-header">⏰ Time-based Sales Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Quarterly performance
        quarterly_data = filtered_df.groupby('Quarter').agg({
            'Revenue': 'sum',
            'Profit': 'sum',
            'OrderID': 'nunique'
        }).reset_index()
        
        fig_quarterly = px.bar(
            quarterly_data,
            x='Quarter',
            y='Revenue',
            title='Revenue by Quarter',
            color='Revenue',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_quarterly, use_container_width=True)
    
    with col2:
        # Monthly heatmap
        monthly_heatmap = filtered_df.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
        monthly_heatmap['Month_Name'] = monthly_heatmap['Month'].map({
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        })
        
        pivot_heatmap = monthly_heatmap.pivot(index='Year', columns='Month_Name', values='Revenue')
        
        fig_heatmap = px.imshow(
            pivot_heatmap,
            title='Revenue Heatmap by Year and Month',
            color_continuous_scale='Blues',
            aspect='auto'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Time-based insights
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Time-based Analysis Insights:</strong><br>
        • Quarterly analysis helps identify seasonal patterns and business cycles<br>
        • The heatmap shows revenue intensity across months and years<br>
        • Darker colors indicate higher revenue periods
    </div>
    """, unsafe_allow_html=True)
    
    # Profitability Analysis
    st.markdown('<div class="section-header">💰 Profitability Deep Dive</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Profit distribution
        fig_profit_dist = px.histogram(
            filtered_df,
            x='Profit',
            nbins=50,
            title='Profit Distribution',
            color_discrete_sequence=['#ff7f0e']
        )
        fig_profit_dist.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Break-even")
        st.plotly_chart(fig_profit_dist, use_container_width=True)
    
    with col2:
        # Revenue vs Profit scatter
        fig_rev_profit = px.scatter(
            filtered_df,
            x='Revenue',
            y='Profit',
            color='Category',
            title='Revenue vs Profit by Category',
            hover_data=['Product', 'Quantity']
        )
        fig_rev_profit.add_hline(y=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig_rev_profit, use_container_width=True)
    
    # Profitability insights
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Profitability Insights:</strong><br>
        • The histogram shows the distribution of profit margins across all transactions<br>
        • Red line indicates break-even point<br>
        • Scatter plot reveals which categories have better profit margins relative to revenue
    </div>
    """, unsafe_allow_html=True)
    
    # Top Performers
    st.markdown('<div class="section-header">🏆 Top Performers Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top products by revenue
        top_products = filtered_df.groupby('Product').agg({
            'Revenue': 'sum',
            'Quantity': 'sum',
            'Profit': 'sum'
        }).reset_index().nlargest(10, 'Revenue')
        
        fig_top_products = px.bar(
            top_products,
            x='Revenue',
            y='Product',
            orientation='h',
            title='Top 10 Products by Revenue',
            color='Profit',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_top_products, use_container_width=True)
    
    with col2:
        # Top customers by revenue
        top_customers = filtered_df.groupby('CustomerName').agg({
            'Revenue': 'sum',
            'OrderID': 'nunique',
            'Profit': 'sum'
        }).reset_index().nlargest(10, 'Revenue')
        
        fig_top_customers = px.bar(
            top_customers,
            x='Revenue',
            y='CustomerName',
            orientation='h',
            title='Top 10 Customers by Revenue',
            color='OrderID',
            color_continuous_scale='Plasma'
        )
        st.plotly_chart(fig_top_customers, use_container_width=True)
    
    # Top performers insights
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Top Performers Insights:</strong><br>
        • Identify best-selling products and most valuable customers<br>
        • Color coding shows profitability (products) and order frequency (customers)<br>
        • Focus on these high-performers for retention and expansion strategies
    </div>
    """, unsafe_allow_html=True)
    
    # Correlation Analysis
    st.markdown('<div class="section-header">🔗 Correlation Analysis</div>', unsafe_allow_html=True)
    
    # Select numeric columns for correlation
    numeric_cols = ['Revenue', 'Quantity', 'Discount', 'Profit', 'UnitPrice']
    correlation_data = filtered_df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        correlation_data,
        text_auto=True,
        aspect="auto",
        title='Correlation Matrix of Numeric Variables',
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Correlation insights
    st.markdown("""
    <div class="insight-box">
        <strong>💡 Correlation Analysis Insights:</strong><br>
        • Red indicates positive correlation, blue indicates negative correlation<br>
        • Strong correlations help identify key relationships in the data<br>
        • Look for unexpected correlations that might indicate business opportunities
    </div>
    """, unsafe_allow_html=True)
    
    # Summary Statistics
    st.markdown('<div class="section-header">📊 Summary Statistics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Numeric Summary")
        numeric_summary = filtered_df[numeric_cols].describe()
        st.dataframe(numeric_summary, use_container_width=True)
    
    with col2:
        st.markdown("### Categorical Summary")
        categorical_summary = pd.DataFrame({
            'Unique Count': [
                filtered_df['Region'].nunique(),
                filtered_df['Segment'].nunique(),
                filtered_df['Category'].nunique(),
                filtered_df['SubCategory'].nunique(),
                filtered_df['Product'].nunique(),
                filtered_df['CustomerName'].nunique()
            ]
        }, index=['Regions', 'Segments', 'Categories', 'Subcategories', 'Products', 'Customers'])
        st.dataframe(categorical_summary, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>📊 Sales Analytics Dashboard</strong></p>
        <p>Built with ❤️ using Streamlit | Data-driven insights for business growth</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
