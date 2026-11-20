from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'online_retail.csv'

@st.cache_data(show_spinner='Loading and cleaning retail data...')
def load_clean_data(path: str = str(DATA_PATH)) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        return pd.DataFrame()
    df = pd.read_csv(p, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    # Standardize common dataset variants.
    aliases = {'CustomerID': 'Customer ID', 'Customer Id': 'Customer ID',
               'UnitPrice': 'Price', 'Invoice Date': 'InvoiceDate'}
    df = df.rename(columns={k: v for k, v in aliases.items() if k in df.columns and v not in df.columns})
    required = ['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'Country']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError('Dataset is missing required columns: ' + ', '.join(missing))
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna(subset=['Invoice', 'StockCode', 'InvoiceDate', 'Quantity', 'Price'])
    df = df[(df['Quantity'] > 0) & (df['Price'] > 0) & (~df['Invoice'].astype(str).str.startswith('C'))].copy()
    df['Revenue'] = df['Quantity'] * df['Price']
    df['Customer ID'] = df['Customer ID'].astype(str).str.replace(r'\.0$', '', regex=True)
    df = df[df['Customer ID'].str.lower().ne('nan')]
    return df

def load_retail_data(path):
    return pd.read_csv(path, low_memory=False)

def clean_retail_data(df):
    df = df.copy()
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df.dropna(subset=['Invoice', 'InvoiceDate', 'Quantity', 'Price'])
    df = df[(df['Quantity'] > 0) & (df['Price'] > 0) & (~df['Invoice'].astype(str).str.startswith('C'))]
    df['Revenue'] = df['Quantity'] * df['Price']
    return df

def require_data():
    df = load_clean_data()
    if df.empty:
        st.error('Dataset not found. Add online_retail.csv to data/raw/ and refresh the app.')
        st.code('data/raw/online_retail.csv')
        st.stop()
    return df
