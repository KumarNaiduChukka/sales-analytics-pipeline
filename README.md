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

1. Clone this repository or download the source code

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. You can also use the provided setup script to create a virtual environment (Windows):
```powershell
.\setup_env.ps1
```

### Environment Setup Script

The `setup_env.ps1` PowerShell script automates the environment setup process:

- Creates a Python virtual environment (`venv`)
- Activates the virtual environment
- Installs all required packages from `requirements.txt`
- Provides status messages throughout the process

4. Run the dashboard using one of the provided scripts:
   - **Python command**:
   ```bash
   streamlit run streamlit_dashboard.py
   ```
   - **Windows Batch file**: Double-click `run_dashboard.bat`
   - **PowerShell script**: 
   ```powershell
   .\run_dashboard.ps1
   ```

### Run Scripts

The project includes convenience scripts for running the dashboard:

- **run_dashboard.bat** (Windows Batch file):
  - Automatically installs dependencies
  - Starts the Streamlit server on port 8501
  - Simple double-click execution

- **run_dashboard.ps1** (PowerShell script):
  - Checks for Python installation
  - Installs dependencies
  - Configures and starts the Streamlit server
  - Provides colorful status messages

## 📁 Data Structure

The dashboard expects a CSV file with the following columns:
- `RowID`, `OrderID`, `Date`, `ShipDate`
- `ShipMode`, `CustomerID`, `CustomerName`, `Segment`
- `Country`, `City`, `State`, `PostalCode`, `Region`
- `ProductID`, `Category`, `SubCategory`, `Product`
- `Revenue`, `Quantity`, `Discount`, `Profit`
- `Year`, `Month`, `YearMonth`, `Quarter`, `MonthStart`, `UnitPrice`

## 📂 Project Structure

```
├── .streamlit/                  # Streamlit configuration
│   └── config.toml              # Streamlit configuration file
├── data/                        # Data directory
│   ├── processed/               # Processed data files
│   │   └── FactSales_clean.csv  # Clean sales data
│   └── raw/                     # Raw data files
│       └── Sample - Superstore.csv  # Original data source
├── notebooks/                   # Jupyter notebooks
│   ├── generate_summary_tables.py  # Script to generate summary tables
│   └── sales_analysis.ipynb     # Main analysis notebook
├── outputs/                     # Output files
│   ├── figures/                 # Generated visualizations
│   │   ├── monthly_revenue_trend.png
│   │   ├── quarterly_revenue.png
│   │   ├── revenue_by_category.png
│   │   ├── revenue_by_region.png
│   │   ├── revenue_by_state_top15.png
│   │   ├── top10_customers_by_revenue.png
│   │   └── top10_products_by_revenue.png
│   └── tables/                  # Generated tables
│       └── Summary_Tables.xlsx  # Excel summary tables
├── reports/                     # Project reports
│   ├── Data_Quality_and_Assumptions.md  # Data quality documentation
│   └── Executive_Summary.md     # Executive summary
├── demo_usage.py               # Demo script
├── requirements.txt            # Project dependencies
├── run_dashboard.bat           # Windows batch script to run dashboard
├── run_dashboard.ps1           # PowerShell script to run dashboard
├── setup_env.ps1               # Environment setup script
├── streamlit_dashboard.py      # Main Streamlit dashboard application
└── test_data_loading.py        # Test script for data loading
```

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
- **Configuration**: Custom Streamlit settings in `.streamlit/config.toml`

### Streamlit Configuration

The dashboard uses a custom Streamlit configuration:

```toml
[global]
developmentMode = false

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

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
3. Run the dashboard using one of these methods:
   - **Python command**: `streamlit run streamlit_dashboard.py`
   - **Windows Batch file**: Double-click `run_dashboard.bat`
   - **PowerShell script**: Right-click `run_dashboard.ps1` and select "Run with PowerShell"
4. Open your browser to the provided URL (typically http://localhost:8501)
5. Use the sidebar filters to explore different data segments
6. Interact with charts for detailed insights

## 📊 Sample Insights

- **Revenue Trends**: Identify seasonal patterns and growth opportunities
- **Regional Performance**: Optimize geographic strategies
- **Product Mix**: Focus on high-performing categories
- **Customer Segments**: Tailor strategies to different customer types
- **Profitability**: Identify areas for margin improvement

## 🧪 Demo and Test Scripts

### Demo Script

The project includes a demo script (`demo_usage.py`) that showcases key features and capabilities of the dashboard:

- **Key Insights Demo**: Examples of insights that can be derived from the dashboard
- **Usage Examples**: How to interact with different dashboard components
- **Data Exploration**: Techniques for exploring the sales data
- **Visualization Capabilities**: Examples of visualization options

Run the demo script to see examples of how to use the dashboard effectively:

```bash
python demo_usage.py
```

### Test Script

The project includes a test script (`test_data_loading.py`) to verify data loading functionality:

- **Data Validation**: Checks if the data can be loaded correctly
- **Data Summary**: Provides a quick overview of the dataset
- **Missing Value Check**: Identifies any missing values in the dataset

Run the test script to verify data integrity before using the dashboard:

```bash
python test_data_loading.py
```

---

*Built with passion for practical data analysis and business intelligence* 🚀