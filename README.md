# Sales Intelligence Platform

A multipage Streamlit portfolio project for retail business intelligence, customer analytics, sales forecasting and decision support.

## Features

1. Executive dashboard with revenue, order, customer and product KPIs
2. Sales analytics: monthly trends, country performance and CSV exports
3. Customer intelligence: RFM scoring and customer segments
4. Product analytics: top products by revenue
5. Sales forecasting: chronological holdout comparison (Linear Regression, Random Forest and Gradient Boosting), plus a configurable future forecast
6. What-if analysis for price and demand scenarios
7. Sales anomaly detection using an interpretable IQR rule
8. Cohort retention heatmap by first-purchase month
9. Market basket analysis with pair support and directional confidence
10. Automated Excel report with KPI, monthly sales, RFM and product sheets

## Requirements

- Python 3.10 or newer
- VS Code (recommended)
- Online Retail II-style CSV dataset

## Dataset setup

The dataset is not included in this ZIP because it is a large third-party data file. Place your CSV at:

`data/raw/online_retail.csv`

Required columns:

`Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country`

The loader also recognizes common alternatives such as `CustomerID` and `UnitPrice`. It removes cancelled invoices, invalid dates, missing required values and non-positive quantity/price rows, then calculates `Revenue = Quantity × Price`.

## Run on Windows PowerShell

Open PowerShell in the project root folder and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, you can skip activation and run:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

## Forecast model evaluation

The forecasting page uses a chronological train/test split rather than random shuffling. MAE and RMSE are error measures; R² may be negative when a model performs worse than predicting the test-set mean. The lowest MAE model is only the best among the candidates tested, not a guarantee of strong future accuracy. Review forecast values alongside business context.

## Notes and limitations

- Anomaly flags are statistical signals, not proof of fraud or a business issue.
- Market basket analysis uses product pairs from a configurable invoice sample; results depend on the sample size and support threshold.
- Cohort retention measures customers with a purchase in each subsequent calendar month after their first observed purchase.
- What-if analysis is a simplified scenario and does not model costs, elasticity or inventory constraints.
- PostgreSQL helper is optional and requires a `DATABASE_URL` environment variable; the app works without a database.

## GitHub hygiene

Do not commit private credentials, `.env` files or database passwords. The raw CSV is ignored by `.gitignore`; keep the dataset local or use an authorized data-hosting method.
