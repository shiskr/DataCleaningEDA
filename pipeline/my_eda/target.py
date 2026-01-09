def detect_target_column(df):
    candidates = ["target", "label", "y", "outcome"]

    for col in df.columns:
        if col.lower() in candidates:
            return col

    # Binary classification heuristic
    for col in df.select_dtypes(include="number").columns:
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) == 2:
            return col

    # Regression fallback
    numeric_cols = df.select_dtypes(include="number")
    if not numeric_cols.empty:
        return numeric_cols.var().idxmax()

    return None