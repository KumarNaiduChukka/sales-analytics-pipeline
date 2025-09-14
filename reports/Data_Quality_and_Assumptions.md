# Data Quality and Assumptions 
 
## Data Mapping 
 
The following column mappings were applied to standardize the dataset: 
 
| Original Column | Mapped Column | 
|----------------|---------------| 
| Order Date | Date | 
| Order ID | OrderID | 
| Customer ID | CustomerID | 
| Region | Region | 
| Country | Country | 
| State | State | 
| Product Name | Product | 
| Category | Category | 
| Quantity | Quantity | 
| Sales | Revenue | 
| Discount | Discount | 
| Profit | Profit | 
 
## Data Quality Issues 
 
The following data quality issues were identified and addressed: 
 
### Missing Values 
 
- **Date**: 0 missing values. Rows with missing dates were dropped as dates are critical for time-series analysis. 
- **Quantity**: 0 missing values. Filled with median value. 
- **Revenue**: 0 missing values. Calculated from Quantity where possible, otherwise filled with median revenue per quantity. 
 
### Duplicates 
 
- **Duplicate Rows**: 0 duplicate rows identified. 
- **Duplicate Order IDs**: 7456 rows with duplicate Order IDs. These were kept as they represent different line items within the same order. 
 
### Invalid Values 
 
- **Invalid Dates**: 0 invalid date values identified and handled. 
- **Negative/Zero Quantities**: 0 instances of negative or zero quantities. 
- **Negative/Zero Revenue**: 0 instances of negative or zero revenue. 
 
## Data Cleaning Steps 
 
1. **Date Standardization**: Converted all dates to datetime format. 
2. **Missing Value Handling**: Applied appropriate strategies for each column type. 
3. **Categorical Value Standardization**: Trimmed whitespace and standardized case (title case). 
4. **Feature Engineering**: Created Year, Month, YearMonth, Quarter, and MonthStart features. 
 
## Anomaly Detection 
 
Two methods were used to detect anomalies: 
 
1. **Z-Score Method**: Identified orders with revenue that deviates significantly from the mean. 
   - Threshold: Z-score > 3.0 (absolute value) 
   - Number of anomalies detected: 87 
 
2. **Rolling Median Deviation**: Identified region-quarter combinations with revenue that deviates significantly from the rolling median. 
   - Threshold: Deviation > 50.0% from rolling median 
   - Number of anomalies detected: 15 
 
## Assumptions 
 
1. **Order Structure**: Multiple rows with the same Order ID represent different products within the same order. 
2. **Currency**: All revenue values are assumed to be in the same currency (USD). 
3. **Business Calendar**: Standard calendar months and quarters are used for time-based analysis. 
4. **Outliers**: Extreme values were kept in the dataset but flagged as anomalies for further investigation. 
