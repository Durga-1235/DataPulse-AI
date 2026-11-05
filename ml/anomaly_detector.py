
import pandas as pd
from sklearn.ensemble import IsolationForest

print("========== ANOMALY DETECTION ==========")

# Load cleaned dataset
df = pd.read_csv("data/processed_sales_data.csv")

# Select numerical features
features = df[["quantity", "unit_price", "total_amount"]]

# Create Isolation Forest model
model = IsolationForest(
    contamination=0.05,
    random_state=42
)

# Train model and predict anomalies
df["anomaly"] = model.fit_predict(features)

# Convert predictions into readable labels
df["anomaly_status"] = df["anomaly"].map({
    1: "Normal",
    -1: "Anomaly"
})

# Display anomaly results
print("\nANOMALY DETECTION RESULTS:")
print(df[[
    "transaction_id",
    "product",
    "quantity",
    "total_amount",
    "anomaly_status"
]].to_string(index=False))

# Filter anomalies
anomalies = df[df["anomaly"] == -1]

print("\nTOTAL ANOMALIES DETECTED:", len(anomalies))

# Save results
df.to_csv("reports/anomaly_results.csv", index=False)

print("\nANOMALY REPORT SAVED SUCCESSFULLY!")
