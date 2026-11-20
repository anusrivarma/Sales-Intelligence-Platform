import streamlit as st
import plotly.express as px
from modules.data_processing import require_data
from modules.sales_analysis import monthly_sales
from modules.ai_insights import generate_basic_insights
st.title('📊 Executive Dashboard')
df=require_data(); rev=df.Revenue.sum(); a,b,c,d=st.columns(4)
a.metric('Revenue',f'£{rev:,.0f}'); b.metric('Orders',f'{df.Invoice.nunique():,}'); c.metric('Customers',f'{df["Customer ID"].nunique():,}'); d.metric('Countries',f'{df.Country.nunique():,}')
m=monthly_sales(df); st.plotly_chart(px.line(m,x='Month',y='Revenue',markers=True,title='Monthly Revenue'),use_container_width=True)
for x in generate_basic_insights(m): st.info(x)
