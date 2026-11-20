import streamlit as st
import plotly.express as px
from modules.data_processing import require_data
from modules.product_analysis import top_products
st.title('🛍️ Product Analytics'); df=require_data(); top=top_products(df,20)
st.plotly_chart(px.bar(top.head(10),x='Revenue',y='Description',orientation='h',title='Top 10 Products by Revenue'),use_container_width=True)
st.dataframe(top,use_container_width=True)
st.download_button('Download product report',top.to_csv(index=False).encode(),'product_report.csv','text/csv')
