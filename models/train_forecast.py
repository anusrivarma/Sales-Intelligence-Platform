"""Train and compare baseline monthly revenue forecasting models.
Run from the project root: python models/train_forecast.py
"""
from modules.data_processing import load_clean_data
from modules.forecasting import monthly_revenue, compare_models

def main():
    df = load_clean_data()
    if df.empty:
        raise SystemExit('Dataset missing. Add data/raw/online_retail.csv first.')
    monthly = monthly_revenue(df)
    if len(monthly) < 8:
        raise SystemExit('At least 8 months of data are recommended.')
    print(compare_models(monthly).to_string(index=False))

if __name__ == '__main__':
    main()
