"""Small, explainable time-based forecasting utilities."""
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def monthly_revenue(df):
    out = df.set_index('InvoiceDate').resample('MS').Revenue.sum().reset_index()
    out.columns = ['Month', 'Revenue']
    return out.sort_values('Month')

def compare_models(monthly):
    data = monthly.copy().reset_index(drop=True)
    data['t'] = np.arange(len(data))
    data['month_num'] = pd.to_datetime(data['Month']).dt.month
    features = ['t', 'month_num']
    split = max(4, int(len(data) * .8))
    if len(data) - split < 1:
        raise ValueError('Not enough monthly observations for a chronological holdout.')
    models = {'Linear Regression': LinearRegression(), 'Random Forest': RandomForestRegressor(n_estimators=250, random_state=42), 'Gradient Boosting': GradientBoostingRegressor(random_state=42)}
    results = []
    for name, model in models.items():
        model.fit(data.loc[:split-1, features], data.loc[:split-1, 'Revenue'])
        pred = model.predict(data.loc[split:, features])
        actual = data.loc[split:, 'Revenue']
        results.append({'Model': name, 'MAE': mean_absolute_error(actual, pred), 'RMSE': np.sqrt(mean_squared_error(actual, pred)), 'R²': r2_score(actual, pred)})
    return pd.DataFrame(results).sort_values('MAE')
