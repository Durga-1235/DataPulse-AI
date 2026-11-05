
from fastapi import FastAPI
import pandas as pd

app = FastAPI(
    title="DataPulse AI API",
    description="Data Quality, Analytics and Anomaly Detection API",
    version="1.0.0"
)

# Load processed data
df = pd.read_csv("data/processed_sales_data.csv")
anomaly_df = pd.read_csv("reports/anomaly_results.csv")


@app.get("/")
def home():
    return {
        "message": "Welcome to DataPulse AI API",
        "status": "Running"
    }


@app.get("/summary")
def get_summary():
    total_revenue = float(df["total_amount"].sum())
    total_transactions = int(df["transaction_id"].nunique())

    return {
        "total_revenue": total_revenue,
        "total_transactions": total_transactions,
        "average_order_value": total_revenue / total_transactions,
        "total_quantity": float(df["quantity"].sum())
    }


@app.get("/products")
def get_products():
    result = df.groupby("product").agg(
        total_quantity=("quantity", "sum"),
        total_revenue=("total_amount", "sum"),
        total_transactions=("transaction_id", "count")
    ).reset_index()

    return result.to_dict(orient="records")


@app.get("/anomalies")
def get_anomalies():
    anomalies = anomaly_df[anomaly_df["anomaly"] == -1]

    return anomalies[[
        "transaction_id",
        "product",
        "quantity",
        "total_amount",
        "anomaly_status"
    ]].to_dict(orient="records")
