import streamlit as st
import plotly.express as px
from modules.data_processing import require_data
from modules.customer_segmentation import build_rfm
st.title('👥 Customer Intelligence'); df=require_data(); rfm=build_rfm(df)
a,b,c=st.columns(3); a.metric('Customers',f'{len(rfm):,}'); b.metric('Average Customer Value',f'£{rfm.Monetary.mean():,.2f}'); c.metric('At-Risk Customers',f'{(rfm.Segment=="At Risk").sum():,}')
seg=rfm.groupby('Segment',as_index=False).size(); st.plotly_chart(px.pie(seg,names='Segment',values='size',title='RFM Customer Segments'),use_container_width=True)
st.dataframe(rfm.sort_values('Monetary',ascending=False),use_container_width=True)
st.download_button('Download RFM report',rfm.to_csv(index=False).encode(),'customer_rfm_report.csv','text/csv')
