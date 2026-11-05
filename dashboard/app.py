
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="DataPulse AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 DataPulse AI")
st.subheader("AI-Powered Data Quality & Business Intelligence Platform")

# Load datasets
df = pd.read_csv("data/processed_sales_data.csv")
anomaly_df = pd.read_csv("reports/anomaly_results.csv")

# Convert date
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

# KPI calculations
total_revenue = df["total_amount"].sum()
total_transactions = df["transaction_id"].nunique()
average_order_value = total_revenue / total_transactions
total_quantity = df["quantity"].sum()
total_anomalies = (anomaly_df["anomaly"] == -1).sum()

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Transactions", total_transactions)
col3.metric("Average Order Value", f"₹{average_order_value:,.0f}")
col4.metric("Anomalies Detected", int(total_anomalies))

st.divider()

# Product analysis
st.header("Product-Wise Revenue Analysis")

product_sales = df.groupby("product", as_index=False)["total_amount"].sum()

fig1 = px.bar(
    product_sales,
    x="product",
    y="total_amount",
    color="product",
    title="Revenue by Product"
)

st.plotly_chart(fig1, use_container_width=True)

# Daily sales trend
st.header("Daily Sales Trend")

daily_sales = df.groupby("transaction_date", as_index=False).agg(
    daily_revenue=("total_amount", "sum")
)

fig2 = px.line(
    daily_sales,
    x="transaction_date",
    y="daily_revenue",
    markers=True,
    title="Daily Revenue Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# Anomaly detection results
st.header("Machine Learning - Anomaly Detection")

anomalies = anomaly_df[anomaly_df["anomaly"] == -1]

st.write("Transactions identified as unusual by the Isolation Forest model:")

st.dataframe(
    anomalies[[
        "transaction_id",
        "product",
        "quantity",
        "total_amount",
        "anomaly_status"
    ]],
    use_container_width=True
)

# Full dataset
st.header("Processed Sales Dataset")
st.dataframe(df, use_container_width=True)

st.success("DataPulse AI Dashboard Loaded Successfully!")
