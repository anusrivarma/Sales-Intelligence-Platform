import streamlit as st
import plotly.express as px
from modules.data_processing import require_data
from modules.sales_analysis import monthly_sales
st.title('📈 Sales Analytics'); df=require_data(); m=monthly_sales(df)
st.plotly_chart(px.line(m,x='Month',y='Revenue',markers=True,title='Monthly Revenue'),use_container_width=True)
st.plotly_chart(px.bar(m,x='Month',y='Orders',title='Monthly Orders'),use_container_width=True)
country=df.groupby('Country',as_index=False).agg(Revenue=('Revenue','sum'),Orders=('Invoice','nunique')).sort_values('Revenue',ascending=False)
st.subheader('Country Performance'); st.dataframe(country,use_container_width=True)
st.download_button('Download sales summary',m.to_csv(index=False).encode(), 'monthly_sales.csv','text/csv')
