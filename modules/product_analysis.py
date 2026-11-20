def top_products(df, n=10):
    return (df.groupby('Description', as_index=False)['Revenue'].sum().sort_values('Revenue', ascending=False).head(n))
