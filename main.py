import os
from pipeline.clean import clean_data
from pipeline.feature_engineering import feature_engineering
from pipeline.load import load_data
from pipeline.my_eda.categorical import categorical_summary, labeled_barplot_plotly
from pipeline.my_eda.feature_importance import compute_feature_importance
from pipeline.my_eda.missing import missing_analysis
from pipeline.my_eda.numeric import numeric_summary, plot_numeric_distribution, plot_correlation, histogram_boxplot_plotly
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

    plots = []
    for col in df.select_dtypes(include="number").columns:
        plots.append(labeled_barplot_plotly(df, col, True))
        plots.append(histogram_boxplot_plotly(df,col, True))

    plots.append(plot_correlation(df))

    build_html_report(
        overview=dataset_overview(df),
        missing_df=missing_analysis(df),
        numeric_df=numeric_summary(df),
        categorical_dict=categorical_summary(df),
        outliers_dict=outlier_summary(df),
        # feature_importance_df=fi_df,
        plots=plots,
        theme_name="light"
    )
    # df = validate_data(df)
    # df = clean_data(df)
    # df = feature_engineering(df)
    save_outputs(df)

if __name__ == "__main__":
    main()