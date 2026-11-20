import streamlit as st
from modules.data_processing import require_data
st.title('🧮 What-if Analysis'); df=require_data(); base=float(df.Revenue.sum())
a,b=st.columns(2)
with a: price=st.slider('Price change (%)',-30,30,0)
with b: demand=st.slider('Demand change (%)',-50,100,0)
projected=base*(1+price/100)*(1+demand/100); delta=projected-base
x,y,z=st.columns(3); x.metric('Current Revenue',f'£{base:,.0f}'); y.metric('Scenario Revenue',f'£{projected:,.0f}'); z.metric('Revenue Change',f'£{delta:,.0f}',f'{delta/base*100:+.1f}%')
st.info('This is a simplified scenario model: it assumes price and demand changes combine multiplicatively and costs remain unchanged.')
