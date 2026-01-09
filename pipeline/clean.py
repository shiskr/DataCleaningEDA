import numpy as np

def clean_data(df, unique_threshold=0.95, exclude_unique_cols=None):
    df = df.drop_duplicates()
    df.columns = df.columns.str.lower().str.strip()

    # ---- Remove unique / ID-like columns ----
    unique_cols = get_unique_columns(
        df,
        threshold=unique_threshold,
        exclude=exclude_unique_cols,
    )

    df = df.drop(columns=unique_cols)

    # ---- Handle missing values ----
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip()
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

    return df, unique_cols


def get_unique_columns(df, threshold=0.95, exclude=None):
    """
    Identify columns with near-unique values (IDs)

    df: pandas DataFrame
    threshold: proportion of unique values to consider column unique
    exclude: list of columns to ignore (e.g., target)

    returns: list of column names
    """
    exclude = exclude or []
    n_rows = len(df)

    unique_cols = []

    for col in df.columns:
        if col in exclude:
            continue

        unique_ratio = df[col].nunique(dropna=False) / n_rows

        if unique_ratio >= threshold:
            unique_cols.append(col)

    return unique_cols