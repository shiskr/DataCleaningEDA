import matplotlib.pyplot as plt

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