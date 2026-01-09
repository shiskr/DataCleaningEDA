import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import skew

def numeric_summary(df):
    numeric_df = df.select_dtypes(include="number")
    return numeric_df.describe().T.reset_index()

def plot_correlation(df):
    corr = df.select_dtypes(include="number").corr()
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        title="Correlation Heatmap"
    )
    return fig.to_html(full_html=False, include_plotlyjs="cdn")

def histogram_boxplot_plotly(
    data,
    feature,
    violin=False,
    auto_bins=True,
    skew_threshold=1.0,
):
    """
    Advanced numeric distribution plot for EDA

    - Automatic bin selection (Freedman–Diaconis)
    - Skewness-based log scaling
    - Optional violin plot
    - Unified theme support
    """

    values = data[feature].dropna()
    if values.empty:
        return None

    # ---- Automatic bin selection (Freedman–Diaconis) ----
    bins = None
    if auto_bins:
        iqr = np.subtract(*np.percentile(values, [75, 25]))
        bin_width = 2 * iqr / (len(values) ** (1 / 3))
        if bin_width > 0:
            bins = int((values.max() - values.min()) / bin_width)

    # ---- Skewness-based log scaling ----
    skew_val = skew(values)
    log_scale = abs(skew_val) > skew_threshold and (values > 0).all()

    # ---- Subplots ----
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.25, 0.75],
        vertical_spacing=0.03,
    )

    # ---- Box or Violin ----
    if violin:
        fig.add_trace(
            go.Violin(
                x=values,
                name=feature,
                box_visible=True,
                meanline_visible=True,
                orientation="h",
            ),
            row=1,
            col=1,
        )
    else:
        fig.add_trace(
            go.Box(
                x=values,
                name=feature,
                boxmean=True,
                orientation="h",
            ),
            row=1,
            col=1,
        )

    # ---- Histogram ----
    fig.add_trace(
        go.Histogram(
            x=values,
            nbinsx=bins,
            opacity=0.75,
        ),
        row=2,
        col=1,
    )

    # ---- Mean & Median ----
    fig.add_vline(x=values.mean(), line_dash="dash", line_color="green")
    fig.add_vline(x=values.median(), line_color="black")

    # ---- Log scale if skewed ----
    if log_scale:
        fig.update_xaxes(type="log", row=2, col=1)

    fig.update_layout(
        title=f"{feature.replace('_',' ').title()} Distribution"
              f"{' (Log Scale)' if log_scale else ''}",
        showlegend=False,
        margin=dict(t=60, b=40, l=40, r=40),
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")

def categorical_summary(df, top_n=5):
    cat_cols = df.select_dtypes(include="object").columns
    summary = {}

    for col in cat_cols:
        summary[col] = df[col].value_counts().head(top_n).to_dict()

    return summary

def labeled_barplot_plotly(data, feature, perc=False):
    """
    Interactive Plotly barplot with labels

    data: dataframe
    feature: categorical column
    perc: show percentage instead of count
    n: top n categories (None = all)
    """

    # Value counts
    vc = data[feature].value_counts()

    df_plot = vc.reset_index()
    df_plot.columns = [feature, "count"]

    total = vc.sum()

    if perc:
        df_plot["value"] = (df_plot["count"] / total * 100).round(1)
        text = df_plot["value"].astype(str) + "%"
        y_col = "value"
        y_label = "Percentage (%)"
    else:
        df_plot["value"] = df_plot["count"]
        text = df_plot["value"].astype(str)
        y_col = "value"
        y_label = "Count"

    fig = px.bar(
        df_plot,
        x=feature,
        y=y_col,
        text=text,
        color=feature,
        color_discrete_sequence=px.colors.qualitative.Set1,
        title=f"Distribution of {feature.replace('_',' ').title()}",
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=f"{feature}: %{{x}}<br>{y_label}: %{{y}}<extra></extra>",
    )

    fig.update_layout(
        xaxis_title=feature.replace("_", " ").title(),
        yaxis_title=y_label,
        showlegend=False,
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        bargap=0.3,
        template="plotly_white",
        margin=dict(t=60, b=40, l=40, r=40),
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")

def univariate(df, col, flag):
    return labeled_barplot_plotly(df, col, flag) + histogram_boxplot_plotly(df, col, flag)