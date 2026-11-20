import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_processing import require_data
st.title('🔁 Cohort & Customer Retention'); df=require_data()
d=df[['Customer ID','InvoiceDate','Invoice']].copy(); d['InvoiceMonth']=d.InvoiceDate.dt.to_period('M'); d['CohortMonth']=d.groupby('Customer ID').InvoiceMonth.transform('min')
d['CohortIndex']=(d.InvoiceMonth.dt.year-d.CohortMonth.dt.year)*12+(d.InvoiceMonth.dt.month-d.CohortMonth.dt.month)+1
cohort=d.groupby(['CohortMonth','CohortIndex'])['Customer ID'].nunique().reset_index(name='Customers')
pivot=cohort.pivot(index='CohortMonth',columns='CohortIndex',values='Customers'); sizes=pivot.iloc[:,0]; retention=pivot.divide(sizes,axis=0)*100
st.metric('Unique Customers',f'{d["Customer ID"].nunique():,}'); st.caption('Retention is the share of a cohort that purchased again in each subsequent calendar month.')
fig=px.imshow(retention,labels=dict(x='Months Since First Purchase',y='Cohort Month',color='Retention %'),aspect='auto',color_continuous_scale='Blues',zmin=0,zmax=100,text_auto='.0f',title='Cohort Retention Heatmap'); st.plotly_chart(fig,use_container_width=True)
st.subheader('Cohort Customer Counts'); st.dataframe(pivot.fillna(0).astype(int),use_container_width=True)
st.download_button('Download retention matrix',retention.to_csv().encode(),'cohort_retention.csv','text/csv')
