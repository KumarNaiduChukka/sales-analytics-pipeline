# Sales Analytics Pipeline

This project delivers a complete sales analytics pipeline using the Superstore dataset. It includes data ingestion, quality checks, exploratory data analysis, anomaly detection, summary tables, and a Power BI dashboard.

## Project Structure

```
├── data/
│   ├── raw/             # Original data files
│   └── processed/       # Cleaned and transformed data
├── notebooks/           # Jupyter notebooks for analysis
├── outputs/
│   ├── figures/         # Generated charts and visualizations
│   └── tables/          # Summary tables and exports
├── reports/             # Documentation and reports
├── dashboard/           # Power BI dashboard files
├── requirements.txt     # Python package dependencies
├── setup_env.ps1        # Environment setup script
└── README.md            # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Power BI Desktop (for viewing and editing the dashboard)

### Environment Setup

1. Clone or download this repository
2. Open PowerShell in the project directory
3. Run the setup script to create a virtual environment and install dependencies:

```powershell
.\setup_env.ps1
```

Alternatively, you can set up the environment manually:

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

## Running the Analysis

1. Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

2. Launch Jupyter Notebook:

```powershell
jupyter notebook
```

3. Open the `notebooks/sales_analysis.ipynb` notebook

## Key Deliverables

- **Jupyter Notebook**: `notebooks/sales_analysis.ipynb` - Contains the full analytics pipeline including exploratory data analysis, data cleaning, quality checks, feature engineering, aggregation, anomaly detection, and visualization.

- **Summary Tables**: `outputs/tables/Summary_Tables.xlsx` - Excel file containing the following sheets:
  - Revenue_by_Month
  - Revenue_by_Region
  - Top_Customers
  - Top_Products
  - Anomalies

- **Power BI Dashboard**: `dashboard/Sales_Dashboard.pbix` - Interactive dashboard with KPIs, trends, regional performance, top products/customers, and anomaly detection.

- **DAX Measures**: `dashboard/dax_measures.md` - Documentation of DAX measures used in the Power BI dashboard.

- **Data Quality Report**: `reports/data_quality_report.json` and `reports/Data_Quality_and_Assumptions.md` - Documentation of data quality checks, cleaning steps, and assumptions made during analysis.

- **Executive Summary**: `reports/Executive_Summary.md` - Summary of key findings and actionable recommendations.

## Data Processing Steps

1. **Data Ingestion**: Load raw data from CSV/Excel files
2. **Data Quality Checks**: Identify missing values, duplicates, and anomalies
3. **Data Cleaning**: Handle missing values, standardize formats, and fix inconsistencies
4. **Feature Engineering**: Create date-based features and derived metrics
5. **Exploratory Analysis**: Generate summary statistics and visualizations
6. **Anomaly Detection**: Identify outliers using statistical methods
7. **Summary Tables**: Create aggregated views of the data
8. **Dashboard Creation**: Build interactive visualizations in Power BI

## Contact

For questions or feedback about this project, please contact the Data Analytics team.