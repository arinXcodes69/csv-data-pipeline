import os
import polars as pl
import polars.selectors as cs


def clean_data(df):
    # Remove rows with missing values
    df = df.drop_nulls()

    # Convert text columns into 1s and 0s
    text_cols = df.select(cs.string()).columns
    if len(text_cols) > 0:
        df = df.to_dummies(columns=text_cols, drop_first=True)

    return df


def transform_data(df):
    # Normalize number columns (skip 0/1 dummy columns)
    num_cols = df.select(cs.numeric()).columns

    for col in num_cols:
        if df[col].n_unique() > 2:
            mean = df[col].mean()
            std = df[col].std()
            if std != 0 and std is not None:
                df = df.with_columns(((pl.col(col) - mean) / std).alias(col))

    return df


def analyze_data(df):
    summary = df.describe()

    # Build a correlation table for all number columns
    num_df = df.select(cs.numeric())
    cols = num_df.columns
    rows = []

    for col1 in cols:
        row_data = {"column": col1}
        for col2 in cols:
            row_data[col2] = num_df.select(pl.corr(col1, col2)).item()
        rows.append(row_data)

    corr_matrix = pl.DataFrame(rows)
    return summary, corr_matrix


def save_results(summary, corr_matrix, base_name):
    os.makedirs("output", exist_ok=True)

    summary_file = f"output/{base_name}_summary.csv"
    corr_file = f"output/{base_name}_correlation.csv"

    summary.write_csv(summary_file)
    corr_matrix.write_csv(corr_file)

    print("\nDone! Your results are saved in the 'output' folder:")
    print(" -", summary_file)
    print(" -", corr_file)


def run_pipeline():
    # Ask the user for their CSV file path (strip quotes in case they drag-and-drop)
    file_path = input("Enter the path to your CSV file: ").strip().strip('"').strip("'")

    if not os.path.exists(file_path):
        print("File not found! Please check the path and try again.")
        return

    print("Reading file...")
    df = pl.read_csv(file_path, null_values=["?", "NA", "N/A", "null", ""])

    df = clean_data(df)
    if df.is_empty():
        print("No data left after removing rows with missing values.")
        return

    df = transform_data(df)
    summary, corr_matrix = analyze_data(df)

    # Get just the user's file name without .csv
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    save_results(summary, corr_matrix, base_name)


if __name__ == "__main__":
    run_pipeline()
