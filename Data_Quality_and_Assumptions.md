# Data Quality and Assumptions

## Column Mappings

The following mappings were applied to normalize the column names from the original dataset:

| Original Column | Normalized Column |
|----------------|-------------------|
| Row ID | RowID |
| Order ID | OrderID |
| Order Date | Date |
| Ship Date | ShipDate |
| Ship Mode | ShipMode |
| Customer ID | CustomerID |
| Customer Name | CustomerName |
| Segment | Segment |
| Country | Country |
| City | City |
| State | State |
| Postal Code | PostalCode |
| Region | Region |
| Product ID | ProductID |
| Category | Category |
| Sub-Category | SubCategory |
| Product Name | Product |
| Sales | Revenue |
| Quantity | Quantity |
| Discount | Discount |
| Profit | Profit |

## Data Cleaning Steps

1. **Column Normalization**: Standardized column names by removing spaces and applying consistent casing.
2. **Date Formatting**: Converted 'Date' and 'ShipDate' columns to datetime format.
3. **Feature Engineering**: Created additional date-related columns:
   - Year
   - Month
   - YearMonth (YYYY-MM format)
   - Quarter
   - MonthStart
4. **Categorical Values**: Standardized categorical values by trimming whitespace and applying title-case formatting.
5. **Missing Values**: Identified and handled missing values:
   - Numeric columns: Filled with zeros or flagged as missing
   - Categorical columns: Filled with 'Unknown' or flagged as missing
6. **Revenue Calculation**: Verified Revenue (Sales) values and ensured consistency with Quantity * UnitPrice where applicable.

## Currency Handling

All monetary values in the dataset are assumed to be in USD. No currency conversion was necessary for this analysis.

## Anomaly Detection Thresholds

The following thresholds were used for anomaly detection:

1. **Z-Score Method**:
   - Threshold: |z| > 3.0
   - Applied to: Per-order revenue
   - Interpretation: Orders with revenue more than 3 standard deviations from the mean

2. **Rolling Median Deviation**:
   - Threshold: > 50%
   - Applied to: Region-quarter revenue
   - Interpretation: Quarters where regional revenue deviates more than 50% from the rolling median

## Data Quality Assumptions

1. **Order IDs**: Each Order ID represents a unique transaction.
2. **Dates**: All dates are valid and within a reasonable business timeframe.
3. **Geographic Data**: All regions, countries, states, and cities are valid geographic entities.
4. **Product Hierarchy**: Category > Sub-Category > Product represents the product hierarchy.
5. **Revenue**: All revenue values are positive or zero.
6. **Quantity**: All quantity values are positive integers or zero.

## Known Limitations

1. The dataset may not include all possible product categories or customer segments.
2. Seasonal patterns may be influenced by factors not captured in the dataset.
3. Geographic analysis is limited to the regions represented in the dataset.
4. Customer behavior analysis is limited to the transaction data without demographic information.

*Note: This document will be updated as additional data quality issues or assumptions are identified during the analysis process.*