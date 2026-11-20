import streamlit as st
import plotly.express as px
from modules.data_processing import require_data
from modules.sales_analysis import monthly_sales
from modules.ai_insights import generate_basic_insights

st.set_page_config(page_title='Sales Intelligence Platform', page_icon='📊', layout='wide')
st.title('📊 Sales Intelligence Platform')
st.caption('Retail performance • Customer intelligence • Forecasting • Decision support')
df = require_data()
min_date, max_date = df.InvoiceDate.min().date(), df.InvoiceDate.max().date()
with st.sidebar:
    st.header('Dashboard Filters')
    countries = st.multiselect('Country', sorted(df.Country.dropna().unique()), default=[])
    date_range = st.date_input('Invoice date range', value=(min_date, max_date), min_value=min_date, max_value=max_date)
filtered = df.copy()
if countries: filtered = filtered[filtered.Country.isin(countries)]
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered.InvoiceDate.dt.date.between(date_range[0], date_range[1])]
if filtered.empty: st.warning('No rows match these filters.'); st.stop()
revenue = filtered.Revenue.sum(); orders = filtered.Invoice.nunique(); customers = filtered['Customer ID'].nunique(); products = filtered.StockCode.nunique()
a,b,c,d = st.columns(4)
a.metric('Total Revenue', f'£{revenue:,.0f}'); b.metric('Orders', f'{orders:,}'); c.metric('Customers', f'{customers:,}'); d.metric('Products', f'{products:,}')
monthly = monthly_sales(filtered)
left,right = st.columns(2)
with left: st.subheader('Monthly Revenue Trend'); st.plotly_chart(px.line(monthly, x='Month', y='Revenue', markers=True), use_container_width=True)
with right:
    st.subheader('Top 10 Countries')
    country = filtered.groupby('Country', as_index=False).Revenue.sum().nlargest(10,'Revenue')
    st.plotly_chart(px.bar(country, x='Revenue', y='Country', orientation='h'), use_container_width=True)
st.subheader('Business Insights')
for insight in generate_basic_insights(monthly): st.info(insight)
st.subheader('Recent Transactions')
st.dataframe(filtered.sort_values('InvoiceDate', ascending=False).head(100), use_container_width=True)
st.download_button('Download filtered data (CSV)', filtered.to_csv(index=False).encode('utf-8'), 'filtered_sales_data.csv', 'text/csv')
