import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

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

def histogram_boxplot_plotly(data, feature, kde=False, bins=None):
    """
    Combined boxplot and histogram using Plotly

    data: dataframe
    feature: numeric column
    kde: whether to show density curve (default False)
    bins: number of bins (default None)
    """

    values = data[feature].dropna()

    # Create subplots
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.25, 0.75],
        vertical_spacing=0.03,
    )

    # ---- Boxplot ----
    fig.add_trace(
        go.Box(
            x=values,
            name=feature,
            boxmean=True,  # shows mean marker
            marker_color="violet",
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
            name="Histogram",
            marker_color="#636EFA",
            opacity=0.75,
        ),
        row=2,
        col=1,
    )

    # ---- Optional KDE (Density Curve) ----
    if kde:
        from scipy.stats import gaussian_kde

        kde_estimator = gaussian_kde(values)
        x_range = np.linspace(values.min(), values.max(), 300)
        kde_values = kde_estimator(x_range)

        # Scale KDE to histogram height
        kde_values = kde_values * len(values) * (x_range[1] - x_range[0])

        fig.add_trace(
            go.Scatter(
                x=x_range,
                y=kde_values,
                mode="lines",
                name="KDE",
                line=dict(color="orange", width=2),
            ),
            row=2,
            col=1,
        )

    # ---- Mean & Median Lines ----
    fig.add_vline(
        x=values.mean(),
        line_dash="dash",
        line_color="green",
        annotation_text="Mean",
        annotation_position="top",
    )

    fig.add_vline(
        x=values.median(),
        line_color="black",
        annotation_text="Median",
        annotation_position="top",
    )

    # ---- Layout ----
    fig.update_layout(
        title=f"Distribution of {feature}",
        showlegend=False,
        template="plotly_white",
        margin=dict(t=60, b=40, l=40, r=40),
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")