import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io


def data_summary(data):
    buffer = io.StringIO()
    data.info(buf=buffer)
    html_data_str = buffer.getvalue()

    lines = html_data_str.split("\n")
    columns = []
    counts = []
    non_nulls = []
    dtypes = []

    for line in lines:
        parts = line.split()
        if len(parts) >= 2 and parts[0].isdigit():
            columns.append(parts[1])
            counts.append(parts[2])
            non_nulls.append(parts[3])
            dtypes.append(parts[4])

    html_data_info = pd.DataFrame({
        'Column': columns,
        'Count': counts,
        'Non-Null': non_nulls,
        'Dtype': dtypes
    })

    return data.head(5), html_data_info


def descriptive_statistics(data):
    return data.describe()


def correlation_matrix(training_data, image_save_path):
    corr_matrix = training_data.corr()

    plt.figure(figsize=(12, 8))
    plt.suptitle('Correlation between each features', fontsize=25)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

    plt.savefig(image_save_path)



