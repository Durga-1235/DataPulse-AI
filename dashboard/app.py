import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# 1. PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="DataPulse AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataPulse AI")
st.subheader(
    "AI-Powered Data Quality & Business Intelligence Platform"
)

# =====================================
# 2. LOAD DATASETS
# =====================================

df = pd.read_csv("data/processed_sales_data.csv")
anomaly_df = pd.read_csv("reports/anomaly_results.csv")

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"]
)

# =====================================
# 3. KPI CALCULATIONS
# =====================================

total_revenue = df["total_amount"].sum()
total_transactions = df["transaction_id"].nunique()

average_order_value = (
    total_revenue / total_transactions
    if total_transactions > 0 else 0
)

total_quantity = df["quantity"].sum()

total_anomalies = (
    anomaly_df["anomaly"] == -1
).sum()

# =====================================
# 4. KPI DASHBOARD
# =====================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Transactions",
    total_transactions
)

col3.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)

col4.metric(
    "Anomalies Detected",
    int(total_anomalies)
)

st.divider()

# =====================================
# 5. DATA QUALITY OVERVIEW
# =====================================

st.header("Data Quality Overview")

total_records = len(df)

missing_values = int(
    df.isnull().sum().sum()
)

duplicate_records = int(
    df.duplicated().sum()
)

quality_score = (
    (total_records - missing_values - duplicate_records)
    / total_records * 100
    if total_records > 0 else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Records",
    total_records
)

col2.metric(
    "Missing Values",
    missing_values
)

col3.metric(
    "Duplicate Records",
    duplicate_records
)

st.metric(
    "Data Quality Score",
    f"{quality_score:.2f}%"
)

st.divider()

# =====================================
# 6. INTERACTIVE PRODUCT FILTER
# =====================================

st.header("Sales Filters")

selected_product = st.selectbox(
    "Select Product",
    ["All Products"] + sorted(
        df["product"].unique().tolist()
    ),
    key="product_filter"
)

if selected_product == "All Products":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["product"] == selected_product
    ].copy()

st.write(
    f"Showing {len(filtered_df)} transactions"
)

# =====================================
# 7. PRODUCT-WISE REVENUE ANALYSIS
# =====================================

st.header("Product-Wise Revenue Analysis")

product_sales = filtered_df.groupby(
    "product",
    as_index=False
)["total_amount"].sum()

fig1 = px.bar(
    product_sales,
    x="product",
    y="total_amount",
    color="product",
    title="Revenue by Product",
    labels={
        "product": "Product",
        "total_amount": "Revenue (INR)"
    }
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# =====================================
# 8. DAILY SALES TREND
# =====================================

st.header("Daily Sales Trend")

daily_sales = filtered_df.groupby(
    "transaction_date",
    as_index=False
).agg(
    daily_revenue=("total_amount", "sum")
)

fig2 = px.line(
    daily_sales,
    x="transaction_date",
    y="daily_revenue",
    markers=True,
    title="Daily Revenue Trend",
    labels={
        "transaction_date": "Date",
        "daily_revenue": "Revenue (INR)"
    }
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================
# 9. MACHINE LEARNING ANOMALY DETECTION
# =====================================

st.header("Machine Learning - Anomaly Detection")

anomalies = anomaly_df[
    anomaly_df["anomaly"] == -1
].copy()

st.write(
    "Transactions identified as unusual "
    "by the Isolation Forest model:"
)

st.dataframe(
    anomalies[
        [
            "transaction_id",
            "product",
            "quantity",
            "total_amount",
            "anomaly_status"
        ]
    ],
    use_container_width=True
)

# =====================================
# 10. PROCESSED SALES DATASET
# =====================================

st.header("Processed Sales Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# =====================================
# 11. SUCCESS MESSAGE
# =====================================

st.success(
    "DataPulse AI Dashboard Loaded Successfully!"
)
