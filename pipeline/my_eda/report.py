from statsmodels.multivariate import plots

from pipeline.my_eda.theme import THEMES, css

def build_html_report(
    overview,
    missing_df,
    numeric_df,
    categorical_dict,
    outliers_dict,
    feature_importance_df=None,
    plots=None,
    theme_name="light",
    output_path="output/eda_report.html"
):
    theme = THEMES[theme_name]

    html = f"""
    <html>
    <head>
        <title>EDA Report</title>
        <style>{css(theme)}</style>
    </head>
    <body>

    <h1>Exploratory Data Analysis</h1>

    <h2>Dataset Overview</h2>
    <pre>{overview}</pre>

    <h2>Missing Values</h2>
    {missing_df.to_html(index=False)}

    <h2>Numeric Summary</h2>
    {numeric_df.to_html(index=False)}

    <h2>Outliers</h2>
    <pre>{outliers_dict}</pre>
    """

    if plots:
        html += f"<h2>Univariate Analysis</h2>"
        for plot_html in plots:
            html += plot_html

    html += "</body></html>"

    with open(output_path, "w") as f:
        f.write(html)