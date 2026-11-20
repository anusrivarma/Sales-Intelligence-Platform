import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_processing import require_data
st.title('🔍 Sales Anomaly Detection'); df=require_data()
m=df.set_index('InvoiceDate').resample('MS').Revenue.sum().reset_index(); m.columns=['Month','Revenue']
q1,q3=m.Revenue.quantile([.25,.75]); iqr=q3-q1; low=q1-1.5*iqr; high=q3+1.5*iqr
m['Status']='Normal'; m.loc[m.Revenue>high,'Status']='Revenue Spike'; m.loc[m.Revenue<low,'Status']='Revenue Drop'
avg=m.Revenue.mean(); m['Difference from Average (%)']=(m.Revenue-avg)/avg*100
an=m[m.Status!='Normal'].copy(); a,b,c=st.columns(3); a.metric('Months Analysed',len(m)); b.metric('Anomalies',len(an)); c.metric('Average Monthly Revenue',f'£{avg:,.0f}')
fig=px.line(m,x='Month',y='Revenue',markers=True,title='Monthly Revenue with Anomalies');
if not an.empty: fig.add_scatter(x=an.Month,y=an.Revenue,mode='markers',name='Anomaly',marker={'size':12,'symbol':'x'})
fig.add_hline(y=high,line_dash='dash',annotation_text='Upper threshold'); fig.add_hline(y=low,line_dash='dash',annotation_text='Lower threshold'); st.plotly_chart(fig,use_container_width=True)
st.subheader('Detected Anomalies')
if an.empty: st.success('No unusual months detected by the IQR rule.')
else:
    for _,r in an.iterrows():
        direction='above' if r.Status=='Revenue Spike' else 'below'; st.warning(f"{r.Month:%B %Y}: {r.Status}. Revenue £{r.Revenue:,.2f}, {abs(r['Difference from Average (%)']):.1f}% {direction} the average.")
    st.dataframe(an,use_container_width=True); st.download_button('Download anomaly report',an.to_csv(index=False).encode(),'sales_anomaly_report.csv','text/csv')
st.caption('Anomalies are statistical flags, not proof of fraud or a business problem. Review promotions, stock, seasonality and data quality.')
