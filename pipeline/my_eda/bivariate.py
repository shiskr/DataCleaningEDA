import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde

def correlation_plot(df, output_dir):
    corr = df.select_dtypes(include="number").corr()

    plt.figure(figsize=(10, 8))
    plt.imshow(corr, cmap="coolwarm")
    plt.colorbar()
    plt.xticks(range(len(corr)), corr.columns, rotation=90)
    plt.yticks(range(len(corr)), corr.columns)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation.png")
    plt.close()

# def distribution_plot_wrt_target_plotly(data, predictor, target):
#     """
#     Interactive bivariate analysis using Plotly
#     data: dataframe
#     predictor: numeric column
#     target: binary categorical target
#     """
#     target_vals = data[target].dropna().unique()
#     if len(target_vals) != 2:
#         raise ValueError("Target must be binary for this plot")
#
#     t0, t1 = target_vals
#
#     v0 = data.loc[data[target] == t0, predictor].dropna()
#     v1 = data.loc[data[target] == t1, predictor].dropna()
#
#     fig = make_subplots(
#         rows=2,
#         cols=2,
#         subplot_titles=[
#             f"Distribution of {predictor} (target = {t0})",
#             f"Distribution of {predictor} (target = {t1})",
#             "Boxplot w.r.t Target",
#             "Boxplot w.r.t Target (No Outliers)",
#         ],
#     )
#
#     # -------- Histogram + KDE (Target = t0) --------
#     fig.add_trace(
#         go.Histogram(x=v0, histnorm="probability density", opacity=0.75),
#         row=1, col=1
#     )
#
#     kde0 = gaussian_kde(v0)
#     x0 = np.linspace(v0.min(), v0.max(), 300)
#     fig.add_trace(
#         go.Scatter(x=x0, y=kde0(x0), mode="lines"),
#         row=1, col=1
#     )
#
#     # -------- Histogram + KDE (Target = t1) --------
#     fig.add_trace(
#         go.Histogram(x=v1, histnorm="probability density", opacity=0.75),
#         row=1, col=2
#     )
#
#     kde1 = gaussian_kde(v1)
#     x1 = np.linspace(v1.min(), v1.max(), 300)
#     fig.add_trace(
#         go.Scatter(x=x1, y=kde1(x1), mode="lines"),
#         row=1, col=2
#     )
#
#     # -------- Boxplot with Outliers --------
#     fig.add_trace(
#         go.Box(x=data[target], y=data[predictor], boxmean=True),
#         row=2, col=1
#     )
#
#     # -------- Boxplot without Outliers --------
#     fig.add_trace(
#         go.Box(
#             x=data[target],
#             y=data[predictor],
#             boxmean=True,
#             boxpoints=False
#         ),
#         row=2, col=2
#     )
#
#     fig.update_layout(
#         title=f"Bivariate Analysis: {predictor} vs {target}",
#         template="plotly_white",
#         showlegend=False,
#         height=800,
#         margin=dict(t=80, b=40, l=40, r=40),
#     )
#
#     return fig.to_html(full_html=False, include_plotlyjs="cdn")


# ------------------- Generalized Bivariate Plotting Methods -------------------

def infer_column_type(series, cat_threshold=15):
    if series.dtype == "object" or series.nunique() <= cat_threshold:
        return "categorical"
    return "numeric"


def numeric_numeric_bivariate_plot(data, col1, col2):
    df = data[[col1, col2]].dropna()

    fig = make_subplots(
        rows=2, cols=2,
        shared_xaxes=True,
        shared_yaxes=True,
        row_heights=[0.2, 0.8],
        column_widths=[0.8, 0.2],
        specs=[[{}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "histogram"}]],
        subplot_titles=[None, f"{col2} Distribution", f"{col1} vs {col2}", f"{col1} Distribution"]
    )

    fig.add_trace(
        go.Scatter(
            x=df[col1],
            y=df[col2],
            mode="markers",
            opacity=0.6
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Histogram(x=df[col1], nbinsx=30),
        row=2, col=2
    )

    fig.add_trace(
        go.Histogram(y=df[col2], nbinsy=30),
        row=1, col=1
    )

    fig.update_layout(
        title=f"Bivariate Analysis (Numeric vs Numeric): {col1} vs {col2}",
        template="plotly_white",
        showlegend=False,
        height=700
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def numeric_categorical_bivariate_plot(data, numeric_col, categorical_col):
    df = data[[numeric_col, categorical_col]].dropna()

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[
            f"Boxplot of {numeric_col} by {categorical_col}",
            f"Violin Plot of {numeric_col} by {categorical_col}"
        ]
    )

    fig.add_trace(
        go.Box(
            x=df[categorical_col],
            y=df[numeric_col],
            boxmean=True
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Violin(
            x=df[categorical_col],
            y=df[numeric_col],
            box_visible=True,
            meanline_visible=True
        ),
        row=1, col=2
    )

    fig.update_layout(
        title=f"Bivariate Analysis (Numeric vs Categorical): {numeric_col} vs {categorical_col}",
        template="plotly_white",
        height=500
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def categorical_categorical_bivariate_plot(data, col1, col2):
    df = data[[col1, col2]].dropna()
    ct = df.groupby([col1, col2]).size().reset_index(name="count")

    fig = go.Figure()

    for val in ct[col2].unique():
        subset = ct[ct[col2] == val]
        fig.add_trace(
            go.Bar(
                x=subset[col1],
                y=subset["count"],
                name=str(val)
            )
        )

    fig.update_layout(
        title=f"Bivariate Analysis (Categorical vs Categorical): {col1} vs {col2}",
        barmode="stack",
        template="plotly_white",
        height=500
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def bivariate_plot_auto(data, col1, col2):
    t1 = infer_column_type(data[col1])
    t2 = infer_column_type(data[col2])

    if t1 == "numeric" and t2 == "numeric":
        return numeric_numeric_bivariate_plot(data, col1, col2)
    elif t1 == "numeric" and t2 == "categorical":
        return numeric_categorical_bivariate_plot(data, col1, col2)
    elif t1 == "categorical" and t2 == "numeric":
        return numeric_categorical_bivariate_plot(data, col2, col1)
    else:
        return categorical_categorical_bivariate_plot(data, col1, col2)