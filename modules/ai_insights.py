def generate_basic_insights(monthly_df):
    if monthly_df.empty:
        return ['No sales data available yet.']
    data = monthly_df.sort_values('Month')
    latest = data.iloc[-1]
    insights = [f"Latest period revenue: £{latest['Revenue']:,.2f}", f"Latest period orders: {int(latest['Orders']):,}"]
    if len(data) > 1:
        prev = data.iloc[-2]
        change = (latest['Revenue'] - prev['Revenue']) / prev['Revenue'] * 100 if prev['Revenue'] else 0
        insights.append(f"Revenue changed {change:+.1f}% versus the previous month.")
    best = data.loc[data['Revenue'].idxmax()]
    insights.append(f"Highest-revenue month in the selected data: {best['Month']} (£{best['Revenue']:,.2f}).")
    return insights
