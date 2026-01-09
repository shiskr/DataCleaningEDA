def validate_data(df):
    if df.empty:
        raise ValueError("Input CSV is empty")

    if df.isnull().mean().max() > 0.7:
        raise ValueError("Too many missing values")

    return df