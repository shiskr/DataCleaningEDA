import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

def compute_feature_importance(df, target_col):
    X = df.drop(columns=[target_col])
    y = df[target_col]

    X = X.select_dtypes(include="number")

    if y.nunique() <= 10:
        model = RandomForestClassifier(n_estimators=100, random_state=42)
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)

    model.fit(X, y)

    return (
        pd.DataFrame({
            "feature": X.columns,
            "importance": model.feature_importances_
        })
        .sort_values("importance", ascending=False)
    )