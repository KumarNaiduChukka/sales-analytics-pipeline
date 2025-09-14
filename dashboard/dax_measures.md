# DAX Measures for Sales Dashboard 
 
## Core Measures 
 
``` 
TotalRevenue = SUM(FactSales[Revenue]) 
TotalQty = SUM(FactSales[Quantity]) 
DistinctOrders = DISTINCTCOUNT(FactSales[OrderID]) 
AvgOrderValue = DIVIDE([TotalRevenue], [DistinctOrders]) 
``` 
 
## Time Intelligence Measures 
 
``` 
RevenueYoY% =  
DIVIDE( 
    [TotalRevenue] - CALCULATE([TotalRevenue], SAMEPERIODLASTYEAR('DimDate'[Date])), 
    CALCULATE([TotalRevenue], SAMEPERIODLASTYEAR('DimDate'[Date])) 
) 
 
RevenueQoQ% =  
DIVIDE( 
    [TotalRevenue] - CALCULATE([TotalRevenue], DATEADD('DimDate'[Date], -1, QUARTER)), 
    CALCULATE([TotalRevenue], DATEADD('DimDate'[Date], -1, QUARTER)) 
) 
 
Rolling3M =  
CALCULATE( 
    [TotalRevenue],  
    DATESINPERIOD('DimDate'[Date], MAX('DimDate'[Date]), -3, MONTH) 
) 
``` 
 
## Ranking Measures 
 
``` 
ProductRank =  
RANKX( 
    ALL(FactSales[Product]), 
    CALCULATE([TotalRevenue]) 
) 
 
CustomerRank =  
RANKX( 
    ALL(FactSales[CustomerID]), 
    CALCULATE([TotalRevenue]) 
) 
``` 
 
## Anomaly Detection Measures 
 
``` 
OrderAverage = AVERAGEX(VALUES(FactSales[OrderID]), CALCULATE([TotalRevenue])) 
OrderStdDev = STDEVX.P(VALUES(FactSales[OrderID]), CALCULATE([TotalRevenue])) 
 
OrderZScore =  
DIVIDE( 
    CALCULATE([TotalRevenue]) - [OrderAverage], 
    [OrderStdDev] 
) 
 
IsAnomalyOrder = ABS([OrderZScore]) > [ZScoreThreshold] 
``` 
 
## What-If Parameters 
 
``` 
// Create a What-If Parameter for Z-Score threshold 
ZScoreThreshold = 3.0 // Default value, can be adjusted by user 
 
// Create a What-If Parameter for currency conversion 
ExchangeRate = 1.0 // Default value (USD), can be adjusted by user 
 
// Converted Revenue 
ConvertedRevenue = [TotalRevenue] * [ExchangeRate] 
``` 
