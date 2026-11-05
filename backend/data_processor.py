
import pandas as pd

# Load the sales dataset
df = pd.read_csv("data/sales_data.csv")

# Display first 5 records
print("FIRST 5 RECORDS")
print(df.head())

# Display dataset information
print("\nDATASET INFORMATION")
print(df.info())

# Display number of rows and columns
print("\nDATASET SHAPE")
print(df.shape)

# Display column names
print("\nCOLUMN NAMES")
print(df.columns.tolist())

# STEP 7: DATA QUALITY ANALYSIS

print("\n========== DATA QUALITY REPORT ==========")

# 1. Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# 2. Check duplicate records
duplicate_count = df.duplicated().sum()

print("\nDUPLICATE RECORDS:")
print(duplicate_count)

# 3. Check duplicate transaction IDs
duplicate_ids = df["transaction_id"].duplicated().sum()

print("\nDUPLICATE TRANSACTION IDs:")
print(duplicate_ids)

# 4. Count rows containing data quality issues
problem_rows = (
    df.isnull().any(axis=1) | df.duplicated()
).sum()

# 5. Calculate data quality score
quality_score = (
    (len(df) - problem_rows) / len(df)
) * 100

print("\nDATA QUALITY SCORE:")
print(f"{quality_score:.2f}%")


# STEP 8: DATA CLEANING

print("\n========== DATA CLEANING ==========")

# 1. Remove duplicate records
df = df.drop_duplicates()

# 2. Fill missing quantity using median
median_quantity = df["quantity"].median()
df["quantity"] = df["quantity"].fillna(median_quantity)

# 3. Convert transaction_date into datetime
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)

# 4. Add total_amount column
df["total_amount"] = df["quantity"] * df["unit_price"]

# 5. Check remaining missing values
print("\nMISSING VALUES AFTER CLEANING:")
print(df.isnull().sum())

# 6. Check remaining duplicates
print("\nDUPLICATES AFTER CLEANING:")
print(df.duplicated().sum())

# 7. Save cleaned dataset
df.to_csv("data/processed_sales_data.csv", index=False)

print("\nCLEANED DATASET SHAPE:")
print(df.shape)

print("\nCLEANED DATASET SAVED SUCCESSFULLY!")


# STEP 9: BUSINESS DATA ANALYTICS

print("\n========== BUSINESS ANALYTICS ==========")

# Load cleaned dataset
df = pd.read_csv("data/processed_sales_data.csv")

# 1. Total Revenue
total_revenue = df["total_amount"].sum()

# 2. Total Transactions
total_transactions = df["transaction_id"].nunique()

# 3. Average Order Value
average_order_value = (
    total_revenue / total_transactions
)

# 4. Total Quantity Sold
total_quantity = df["quantity"].sum()

# 5. Product-wise Sales Analysis
product_analysis = df.groupby("product").agg(
    total_quantity=("quantity", "sum"),
    total_revenue=("total_amount", "sum"),
    total_transactions=("transaction_id", "count")
).reset_index()

# 6. Best Selling Product
best_selling_product = product_analysis.loc[
    product_analysis["total_quantity"].idxmax(),
    "product"
]

# 7. Highest Revenue Product
top_revenue_product = product_analysis.loc[
    product_analysis["total_revenue"].idxmax(),
    "product"
]

# Display KPIs
print(f"\nTotal Revenue: Rs. {total_revenue:,.2f}")
print(f"Total Transactions: {total_transactions}")
print(f"Average Order Value: Rs. {average_order_value:,.2f}")
print(f"Total Quantity Sold: {total_quantity}")

print(f"\nBest Selling Product: {best_selling_product}")
print(f"Top Revenue Product: {top_revenue_product}")

# Display product analysis
print("\nPRODUCT-WISE SALES ANALYSIS:")
print(product_analysis.to_string(index=False))

# Save analytics report
product_analysis.to_csv(
    "reports/product_analysis.csv",
    index=False
)

print("\nANALYTICS REPORT SAVED SUCCESSFULLY!")

# STEP 10: DAILY SALES TREND ANALYSIS

import plotly.express as px

print("\n========== DAILY SALES TREND ANALYSIS ==========")

# Convert date column
df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)

# Group sales by date
daily_sales = df.groupby("transaction_date").agg(
    daily_revenue=("total_amount", "sum"),
    daily_transactions=("transaction_id", "count")
).reset_index()

# Display daily sales
print("\nDAILY SALES:")
print(daily_sales.to_string(index=False))

# Find highest sales date
highest_sales_date = daily_sales.loc[
    daily_sales["daily_revenue"].idxmax()
]

print("\nHIGHEST SALES DATE:")
print(highest_sales_date)

# Save daily sales report
daily_sales.to_csv(
    "reports/daily_sales_analysis.csv",
    index=False
)

# Create interactive sales trend chart
fig = px.line(
    daily_sales,
    x="transaction_date",
    y="daily_revenue",
    title="Daily Sales Revenue Trend",
    markers=True,
    labels={
        "transaction_date": "Transaction Date",
        "daily_revenue": "Revenue (INR)"
    }
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Date",
    yaxis_title="Revenue (INR)"
)

# Save interactive chart
fig.write_html("reports/daily_sales_chart.html")

print("\nDAILY SALES CHART CREATED SUCCESSFULLY!")


