import numpy as np

def clean_data(df):
    df = df.drop_duplicates()
    df.columns = df.columns.str.lower().str.strip()

    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.strip()
            df[col] = df[col].fillna(df[col].mode()[0])
            # df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            # df[col].fillna(df[col].median(), inplace=True)
            df[col] = df[col].fillna(df[col].median())

    return df