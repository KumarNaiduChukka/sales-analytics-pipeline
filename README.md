# 📊 Sales Analytics Dashboard

An interactive EDA (Exploratory Data Analysis) dashboard built with Streamlit for analyzing sales data. This dashboard provides comprehensive insights into sales performance, customer behavior, and business trends.

## 🚀 Features

### 📈 Key Performance Indicators
- Total Revenue, Orders, Average Order Value, and Profit Margin
- Real-time metrics that update based on selected filters

### 🌍 Regional Analysis
- Revenue distribution across regions
- Profit analysis by region
- Interactive pie charts and bar charts

### 📦 Product Category Performance
- Revenue analysis by product categories
- Treemap visualization for subcategories
- Profitability insights

### 👥 Customer Segment Analysis
- Revenue vs Profit scatter plots
- Customer count by segment
- Segment performance comparison

### ⏰ Time-based Analysis
- Monthly revenue trends
- Quarterly performance analysis
- Revenue heatmap by year and month

### 💰 Profitability Deep Dive
- Profit distribution histograms
- Revenue vs Profit scatter plots
- Break-even analysis

### 🏆 Top Performers
- Top 10 products by revenue
- Top 10 customers by revenue
- Performance ranking with color coding

### 🔗 Correlation Analysis
- Correlation matrix heatmap
- Relationship analysis between numeric variables

### 📊 Summary Statistics
- Comprehensive data summaries
- Categorical and numeric statistics

## 🎨 Custom Styling

The dashboard features:
- Modern gradient backgrounds
- Custom color schemes
- Interactive hover effects
- Responsive design
- Professional typography
- Insight boxes with key takeaways

## 🛠️ Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
streamlit run streamlit_dashboard.py
```

## 📁 Data Structure

The dashboard expects a CSV file with the following columns:
- `RowID`, `OrderID`, `Date`, `ShipDate`
- `ShipMode`, `CustomerID`, `CustomerName`, `Segment`
- `Country`, `City`, `State`, `PostalCode`, `Region`
- `ProductID`, `Category`, `SubCategory`, `Product`
- `Revenue`, `Quantity`, `Discount`, `Profit`
- `Year`, `Month`, `YearMonth`, `Quarter`, `MonthStart`, `UnitPrice`

## 🔍 Interactive Features

### Filters
- **Date Range**: Select specific time periods
- **Region**: Filter by geographic regions
- **Customer Segment**: Filter by customer types
- **Product Category**: Filter by product categories

### Visualizations
- **Interactive Charts**: Hover for detailed information
- **Zoom and Pan**: Explore data in detail
- **Color Coding**: Visual indicators for performance
- **Responsive Design**: Works on all screen sizes

## 💡 Key Insights

Each visualization includes:
- **Insight Boxes**: Key takeaways and business implications
- **Color Coding**: Visual performance indicators
- **Trend Analysis**: Pattern identification
- **Comparative Analysis**: Performance comparisons

## 🎯 Business Applications

This dashboard helps with:
- **Sales Performance Monitoring**: Track revenue and profit trends
- **Customer Analysis**: Understand customer behavior and segments
- **Product Performance**: Identify best and worst performing products
- **Regional Analysis**: Optimize geographic strategies
- **Seasonal Planning**: Identify seasonal patterns and opportunities
- **Profitability Optimization**: Focus on high-margin products and customers

## 🔧 Technical Details

- **Framework**: Streamlit
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS with gradients and animations
- **Performance**: Cached data loading for optimal performance

## 📈 Dashboard Sections

1. **Header**: Professional title and description
2. **KPI Cards**: Key metrics at a glance
3. **Revenue Trends**: Time-series analysis
4. **Regional Analysis**: Geographic performance
5. **Product Analysis**: Category and subcategory insights
6. **Customer Analysis**: Segment performance
7. **Time Analysis**: Temporal patterns
8. **Profitability**: Financial performance
9. **Top Performers**: Best products and customers
10. **Correlation**: Variable relationships
11. **Summary**: Statistical overview

## 🚀 Getting Started

1. Ensure your data file is in the correct location (`data/processed/FactSales_clean.csv`)
2. Install dependencies: `pip install -r requirements.txt`
3. Run the dashboard: `streamlit run streamlit_dashboard.py`
4. Open your browser to the provided URL
5. Use the sidebar filters to explore different data segments
6. Interact with charts for detailed insights

## 📊 Sample Insights

- **Revenue Trends**: Identify seasonal patterns and growth opportunities
- **Regional Performance**: Optimize geographic strategies
- **Product Mix**: Focus on high-performing categories
- **Customer Segments**: Tailor strategies to different customer types
- **Profitability**: Identify areas for margin improvement

---

*Built with passion for practical data analysis and business intelligence* 🚀