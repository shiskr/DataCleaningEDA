import plotly.express as px

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