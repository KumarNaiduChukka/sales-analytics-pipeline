# DAX Measures for Sales Dashboard

## Core Measures

```dax
// Total Revenue
TotalRevenue = SUM(FactSales[Revenue])

// Total Quantity
TotalQty = SUM(FactSales[Quantity])

// Distinct Orders
DistinctOrders = DISTINCTCOUNT(FactSales[OrderID])

// Average Order Value
AvgOrderValue = DIVIDE([TotalRevenue], [DistinctOrders])

// Total Profit
TotalProfit = SUM(FactSales[Profit])

// Profit Margin
ProfitMargin = DIVIDE([TotalProfit], [TotalRevenue], 0)

// Profit Margin %
ProfitMarginPct = [ProfitMargin] * 100
```

## Time Intelligence Measures

```dax
// Revenue Year over Year %
RevenueYoY% = 
VAR CurrentRevenue = [TotalRevenue]
VAR PriorRevenue = CALCULATE([TotalRevenue], SAMEPERIODLASTYEAR('DimDate'[Date]))
RETURN
    DIVIDE(CurrentRevenue - PriorRevenue, PriorRevenue, 0)

// Revenue Quarter over Quarter %
RevenueQoQ% = 
VAR CurrentRevenue = [TotalRevenue]
VAR PriorRevenue = CALCULATE([TotalRevenue], DATEADD('DimDate'[Date], -1, QUARTER))
RETURN
    DIVIDE(CurrentRevenue - PriorRevenue, PriorRevenue, 0)

// Revenue Month over Month %
RevenueMoM% = 
VAR CurrentRevenue = [TotalRevenue]
VAR PriorRevenue = CALCULATE([TotalRevenue], DATEADD('DimDate'[Date], -1, MONTH))
RETURN
    DIVIDE(CurrentRevenue - PriorRevenue, PriorRevenue, 0)

// Rolling 3-Month Revenue
Rolling3M = 
CALCULATE(
    [TotalRevenue],
    DATESINPERIOD('DimDate'[Date], MAX('DimDate'[Date]), -3, MONTH)
)

// Year to Date Revenue
YTD Revenue = 
CALCULATE(
    [TotalRevenue],
    DATESYTD('DimDate'[Date])
)

// Quarter to Date Revenue
QTD Revenue = 
CALCULATE(
    [TotalRevenue],
    DATESQTD('DimDate'[Date])
)

// Month to Date Revenue
MTD Revenue = 
CALCULATE(
    [TotalRevenue],
    DATESMTD('DimDate'[Date])
)
```

## Ranking Measures

```dax
// Product Rank by Revenue
ProductRankByRevenue = 
RANKX(
    ALL(FactSales[Product]),
    CALCULATE([TotalRevenue])
)

// Customer Rank by Revenue
CustomerRankByRevenue = 
RANKX(
    ALL(FactSales[CustomerName]),
    CALCULATE([TotalRevenue])
)

// Region Rank by Revenue
RegionRankByRevenue = 
RANKX(
    ALL(FactSales[Region]),
    CALCULATE([TotalRevenue])
)
```

## Anomaly Detection Measures

```dax
// Z-Score for Order Revenue
OrderRevenueZScore = 
VAR OrderRevenue = CALCULATE([TotalRevenue], ALLEXCEPT(FactSales, FactSales[OrderID]))
VAR AvgOrderRevenue = AVERAGE(SUMMARIZE(FactSales, FactSales[OrderID], "OrderRevenue", [TotalRevenue]))
VAR StdDevOrderRevenue = STDEVX.P(SUMMARIZE(FactSales, FactSales[OrderID], "OrderRevenue", [TotalRevenue]), [OrderRevenue])
RETURN
    DIVIDE(OrderRevenue - AvgOrderRevenue, StdDevOrderRevenue)

// Is Order Revenue Anomaly
IsOrderRevenueAnomaly = ABS([OrderRevenueZScore]) > 3

// Anomaly Threshold Parameter
AnomalyThreshold = 
VAR DefaultThreshold = 3
VAR SelectedThreshold = SELECTEDVALUE('AnomalyParameters'[ZScoreThreshold], DefaultThreshold)
RETURN
    SelectedThreshold
```

## Conditional Formatting Measures

```dax
// Revenue Status Color
RevenueStatusColor = 
IF(
    [RevenueYoY%] > 0.05, "#4CAF50",  // Green for >5% growth
    IF(
        [RevenueYoY%] >= 0, "#FFC107",  // Yellow for 0-5% growth
        "#F44336"  // Red for negative growth
    )
)

// Profit Status Color
ProfitStatusColor = 
IF(
    [ProfitMargin] > 0.15, "#4CAF50",  // Green for >15% margin
    IF(
        [ProfitMargin] >= 0.05, "#FFC107",  // Yellow for 5-15% margin
        "#F44336"  // Red for <5% margin
    )
)
```

## Date Table Creation

```dax
// Create Date table
DimDate = 
VAR MinDate = MIN(FactSales[Date])
VAR MaxDate = MAX(FactSales[Date])
VAR DayCount = DATEDIFF(MinDate, MaxDate, DAY) + 1
RETURN
    ADDCOLUMNS(
        CALENDAR(MinDate, MaxDate),
        "Year", YEAR([Date]),
        "Quarter", QUARTER([Date]),
        "Month", MONTH([Date]),
        "MonthName", FORMAT([Date], "MMMM"),
        "MonthShort", FORMAT([Date], "MMM"),
        "YearMonth", FORMAT([Date], "yyyy-MM"),
        "YearMonthName", FORMAT([Date], "yyyy-MMM"),
        "WeekNum", WEEKNUM([Date]),
        "DayOfWeek", WEEKDAY([Date]),
        "DayName", FORMAT([Date], "dddd"),
        "DayShort", FORMAT([Date], "ddd"),
        "IsWeekend", IF(WEEKDAY([Date], 2) > 5, TRUE, FALSE),
        "MonthStart", DATE(YEAR([Date]), MONTH([Date]), 1),
        "QuarterStart", DATE(YEAR([Date]), (QUARTER([Date]) - 1) * 3 + 1, 1),
        "YearStart", DATE(YEAR([Date]), 1, 1)
    )
```

## Usage Instructions

1. Create a Date table using the DAX formula provided above
2. Create a relationship between FactSales[Date] and DimDate[Date]
3. Add these measures to your model as needed
4. For anomaly detection, create a parameter table with threshold values

```dax
// Create Parameter table for anomaly thresholds
AnomalyParameters = 
VAR DefaultThreshold = 3
RETURN
    DATATABLE(
        "ZScoreThreshold", DOUBLE,
        {{DefaultThreshold}}
    )
```

5. Use What-If parameters to allow users to adjust thresholds dynamically