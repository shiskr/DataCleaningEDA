import pandas as pd
from pipeline.my_eda.theme import THEMES, css

def build_html_report(
        overview,
        missing_df,
        numeric_df,
        categorical_dict,
        outliers_dict,
        feature_importance_df=None,
        uni_plots=None,
        bi_plots=None,
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
    {pd.DataFrame.from_dict(overview, orient="index")
    .reset_index()
    .rename(columns={"index": "Metric", 0: "Value"})
    .to_html(index=False)}
    
    <hr>

    <h2>Missing Values</h2>
    {missing_df.to_html(index=False)}
    
    <hr>

    <h2>Numeric Summary</h2>
    {numeric_df.to_html(index=False)}
    
    <hr>

    <h2>Outliers</h2>
    <pre>{outliers_dict}</pre>
    
    <hr>
    """

    if uni_plots:
        html += f"<h2>Univariate Analysis</h2>"
        for plot_html in uni_plots:
            html += plot_html + "<hr>"

    if bi_plots:
        html += f"<h2>Bivariate Analysis</h2>"
        for plot_html in bi_plots:
            html += plot_html + "<hr>"

    html += "</body></html>"

    with open(output_path, "w") as f:
        f.write(html)
