import pandas as pd

def build_rfm(df):
    data = df.copy()
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    snapshot = data['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = data.groupby('Customer ID').agg(
        Recency=('InvoiceDate', lambda x: (snapshot - x.max()).days),
        Frequency=('Invoice', 'nunique'), Monetary=('Revenue', 'sum')
    ).reset_index()
    # Rank-based scores are robust to skewed retail distributions.
    for col, ascending in [('Recency', False), ('Frequency', True), ('Monetary', True)]:
        rfm[col + 'Score'] = pd.qcut(rfm[col].rank(method='first'), 4, labels=[1,2,3,4]).astype(int)
        if col == 'Recency':
            rfm[col + 'Score'] = 5 - rfm[col + 'Score']
    score = rfm[['RecencyScore','FrequencyScore','MonetaryScore']].sum(axis=1)
    rfm['Segment'] = 'Regular'
    rfm.loc[score >= 10, 'Segment'] = 'Champions'
    rfm.loc[(rfm.RecencyScore >= 3) & (rfm.FrequencyScore <= 2), 'Segment'] = 'Potential Loyalists'
    rfm.loc[(rfm.RecencyScore <= 2) & (rfm.FrequencyScore <= 2), 'Segment'] = 'At Risk'
    return rfm
