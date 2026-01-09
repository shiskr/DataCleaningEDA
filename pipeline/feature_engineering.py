import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def feature_engineering(df):
    # Date features
    for col in df.select_dtypes(include="datetime").columns:
        df[f"{col}_year"] = df[col].dt.year
        df[f"{col}_month"] = df[col].dt.month
        df[f"{col}_day"] = df[col].dt.day

    # Normalize numeric columns
    numeric_cols = df.select_dtypes(include="number").columns
    scaler = MinMaxScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # Encode categorical columns
    cat_cols = df.select_dtypes(include="object").columns
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    return df