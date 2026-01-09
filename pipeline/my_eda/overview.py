def dataset_overview(df):
    return {
        "Number of Rows": int(df.shape[0]),
        "Number of Columns": int(df.shape[1]),
        "Memory in MB": str(round(df.memory_usage(deep=True).sum() / 1024**2, 2)) + " MB",
        "Duplicates": df.duplicated().sum()
    }