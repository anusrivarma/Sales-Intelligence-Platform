import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from modules.data_processing import require_data
st.title('🔮 Sales Forecasting'); df=require_data()
m=df.set_index('InvoiceDate').resample('MS').Revenue.sum().reset_index(); m.columns=['Month','Revenue']; m=m.sort_values('Month')
if len(m)<8: st.warning('At least 8 months of data are recommended for a meaningful time-based evaluation.'); st.stop()
m['t']=np.arange(len(m)); m['month_num']=m.Month.dt.month
X=m[['t','month_num']]; y=m.Revenue; split=max(4,int(len(m)*.8)); Xtr,Xte=X.iloc[:split],X.iloc[split:]; ytr,yte=y.iloc[:split],y.iloc[split:]
models={'Linear Regression':LinearRegression(),'Random Forest':RandomForestRegressor(n_estimators=250,random_state=42),'Gradient Boosting':GradientBoostingRegressor(random_state=42)}
rows=[]; fitted={}
for name,model in models.items():
    model.fit(Xtr,ytr); pred=model.predict(Xte); fitted[name]=model
    rows.append({'Model':name,'MAE':mean_absolute_error(yte,pred),'RMSE':np.sqrt(mean_squared_error(yte,pred)),'R²':r2_score(yte,pred)})
metrics=pd.DataFrame(rows).sort_values('MAE'); st.subheader('Model Comparison'); st.dataframe(metrics,use_container_width=True)
best_name=metrics.iloc[0]['Model']; best=models[best_name]; st.success(f'Lowest holdout MAE in this comparison: {best_name}. This is not a guarantee of future accuracy.')
future_n=st.slider('Forecast horizon (months)',3,12,6); future_t=np.arange(len(m),len(m)+future_n); future_months=pd.date_range(m.Month.max()+pd.offsets.MonthBegin(1),periods=future_n,freq='MS'); fx=pd.DataFrame({'t':future_t,'month_num':future_months.month}); pred=np.maximum(best.predict(fx),0)
plot=pd.concat([m[['Month','Revenue']].assign(Type='Historical'),pd.DataFrame({'Month':future_months,'Revenue':pred,'Type':'Forecast'})]); st.plotly_chart(px.line(plot,x='Month',y='Revenue',color='Type',markers=True,title='Historical Sales and Forecast'),use_container_width=True)
st.caption('Evaluation uses a chronological holdout. Monthly retail revenue can be volatile; treat forecasts as planning estimates.')
out=pd.DataFrame({'Month':future_months,'Forecast Revenue':pred}); st.dataframe(out,use_container_width=True); st.download_button('Download forecast CSV',out.to_csv(index=False).encode(),'sales_forecast.csv','text/csv')
