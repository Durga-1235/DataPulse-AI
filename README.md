
# DataPulse AI

AI-Powered Data Quality, Anomaly Detection & Business Intelligence Platform.

## Overview

DataPulse AI is a data analytics platform that cleans raw sales data, identifies data quality issues, generates business insights, detects unusual transactions using Machine Learning, and presents results through an interactive dashboard.

## Features

- Data quality analysis
- Missing value handling and duplicate removal
- Business KPI analysis
- Product-wise revenue analysis
- Daily sales trend visualization
- Machine Learning anomaly detection using Isolation Forest
- Interactive Streamlit dashboard
- REST APIs using FastAPI

## Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- Plotly
- Streamlit
- FastAPI
- Uvicorn

## Project Structure

```text
DataPulse-AI/
├── backend/
│   ├── main.py
│   └── data_processor.py
├── data/
│   ├── sales_data.csv
│   └── processed_sales_data.csv
├── ml/
│   └── anomaly_detector.py
├── dashboard/
│   └── app.py
├── reports/
├── .gitignore
├── requirements.txt
└── README.md
```

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run data processing:

```bash
python backend/data_processor.py
```

Run anomaly detection:

```bash
python ml/anomaly_detector.py
```

Run dashboard:

```bash
streamlit run dashboard/app.py
```

Run API:

```bash
uvicorn backend.main:app --reload --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

## Machine Learning

Isolation Forest is used to identify unusual sales transactions.

## Project Results

- 50 cleaned transactions
- ₹12,85,800 total revenue
- 5 product categories
- 3 detected anomalies

## Author

Durga T
B.Tech – Artificial Intelligence and Data Science
