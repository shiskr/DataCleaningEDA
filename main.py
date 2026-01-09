import os
from pipeline.clean import clean_data
from pipeline.feature_engineering import feature_engineering
from pipeline.load import load_data
from pipeline.my_eda.bivariate import bivariate_plot_auto
from pipeline.my_eda.missing import missing_analysis
from pipeline.my_eda.univariate import numeric_summary, plot_correlation, histogram_boxplot_plotly, categorical_summary, \
    labeled_barplot_plotly, univariate
from pipeline.my_eda.outliers import outlier_summary
from pipeline.my_eda.overview import dataset_overview
from pipeline.my_eda.report import build_html_report
from pipeline.my_eda.target import detect_target_column
from pipeline.save import save_outputs
from pipeline.validate import validate_data
from pipeline.my_eda.theme import apply_eda_theme

def main():
    os.makedirs("output/plots", exist_ok=True)
    apply_eda_theme()
    df = load_data("input/flight_customer_data.xlsx")

    # target_col = detect_target_column(df)
    # fi_df = compute_feature_importance(df, target_col) if target_col else None

    univariate_plots = []
    for col in df.select_dtypes(include="number").columns:
        univariate_plots.append(univariate(df, col, True))
        # plots.append(distribution_plot_wrt_target_plotly(df,col))

    bivariate_plots = [plot_correlation(df)]
    cols = df.columns.tolist()
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            try:
                bivariate_plots.append(bivariate_plot_auto(df, cols[i], cols[j]))
            except Exception:
                pass

    build_html_report(
        overview=dataset_overview(df),
        missing_df=missing_analysis(df),
        numeric_df=numeric_summary(df),
        categorical_dict=categorical_summary(df),
        outliers_dict=outlier_summary(df),
        # feature_importance_df=fi_df,
        uni_plots=univariate_plots,
        bi_plots=bivariate_plots,
        theme_name="light"
    )
    # df = validate_data(df)
    df, unique_cols = clean_data(df)
    # df = feature_engineering(df)
    save_outputs(df)

if __name__ == "__main__":
    main()