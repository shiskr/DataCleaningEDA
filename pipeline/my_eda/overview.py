def dataset_overview(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 2),
        "duplicates": df.duplicated().sum()
    }