import streamlit as st
import pandas as pd
from io import BytesIO
from modules.data_processing import require_data
from modules.sales_analysis import monthly_sales
from modules.customer_segmentation import build_rfm
from modules.product_analysis import top_products
st.title('📄 Automated Reports'); df=require_data(); monthly=monthly_sales(df); rfm=build_rfm(df); products=top_products(df,50)
summary=pd.DataFrame([{'Metric':'Revenue','Value':df.Revenue.sum()},{'Metric':'Orders','Value':df.Invoice.nunique()},{'Metric':'Customers','Value':df['Customer ID'].nunique()},{'Metric':'Products','Value':df.StockCode.nunique()}])
st.subheader('Report Preview'); st.dataframe(summary,use_container_width=True)
buf=BytesIO()
with pd.ExcelWriter(buf,engine='openpyxl') as writer:
    summary.to_excel(writer,index=False,sheet_name='KPI Summary'); monthly.to_excel(writer,index=False,sheet_name='Monthly Sales'); rfm.to_excel(writer,index=False,sheet_name='Customer RFM'); products.to_excel(writer,index=False,sheet_name='Top Products')
st.download_button('📥 Download Excel Business Report',buf.getvalue(),'sales_intelligence_report.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
st.download_button('Download monthly sales CSV',monthly.to_csv(index=False).encode(),'monthly_sales.csv','text/csv')
