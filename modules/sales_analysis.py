import pandas as pd

def monthly_sales(df):
    data = df.copy()
    data['Month'] = pd.to_datetime(data['InvoiceDate']).dt.to_period('M').astype(str)
    return data.groupby('Month', as_index=False).agg(Revenue=('Revenue','sum'), Orders=('Invoice','nunique'), Customers=('Customer ID','nunique'))
