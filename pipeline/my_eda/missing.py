def missing_analysis(df):
    return (
        df.isnull()
        .mean()
        .mul(100)
        .round(2)
        .reset_index()
        .rename(columns={"index": "column", 0: "missing_percent"})
    )