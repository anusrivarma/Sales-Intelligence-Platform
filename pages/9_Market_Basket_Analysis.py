import streamlit as st
import pandas as pd
from itertools import combinations
from collections import Counter
from modules.data_processing import require_data
st.title('🧺 Market Basket Analysis'); df=require_data(); limit=st.slider('Maximum invoices to analyse',500,10000,3000,500)
orders=df[['Invoice','Description']].dropna().drop_duplicates('Invoice') if False else df[['Invoice','Description']].dropna().drop_duplicates()
invoice_ids=df.Invoice.drop_duplicates().head(limit); orders=df[df.Invoice.isin(invoice_ids)].groupby('Invoice').Description.apply(lambda x: sorted(set(x.astype(str))))
min_support=st.slider('Minimum support (%)',0.1,10.0,1.0,0.1)/100
pair_counts=Counter(); item_counts=Counter(); n=len(orders)
for items in orders:
    item_counts.update(items)
    if len(items)>1: pair_counts.update(combinations(items,2))
rows=[]
for (a,b),count in pair_counts.most_common(1000):
    support=count/n if n else 0
    if support>=min_support:
        conf_a=count/item_counts[a]; conf_b=count/item_counts[b]
        rows.append({'Product A':a,'Product B':b,'Orders Together':count,'Support %':support*100,'Confidence A→B %':conf_a*100,'Confidence B→A %':conf_b*100})
result=pd.DataFrame(rows)
st.caption(f'Analysed {n:,} invoices. Pair rules are exploratory associations, not causal recommendations.')
if result.empty: st.info('No product pairs meet this support threshold. Try lowering the minimum support or increasing invoices analysed.')
else:
    st.dataframe(result.head(100),use_container_width=True); st.download_button('Download basket rules',result.to_csv(index=False).encode(),'market_basket_rules.csv','text/csv')
