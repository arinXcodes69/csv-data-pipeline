import os
import webbrowser
import polars as pl
import polars.selectors as cs
import plotly.express as px
from plotly.subplots import make_subplots


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


def create_dashboard(df, corr_matrix, base_name):
    # Pick continuous number columns (skip 0/1 dummy columns) for cleaner charts
    num_cols = [col for col in df.select(cs.numeric()).columns if df[col].n_unique() > 2]
    cols_to_plot = num_cols[:4]

    # 1. Build a correlation heatmap
    corr_cols = [col for col in corr_matrix.columns if col != "column"]
    z_values = corr_matrix.select(corr_cols).to_numpy()

    heatmap = px.imshow(
        z_values,
        x=corr_cols,
        y=corr_cols,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Feature Correlation Heatmap",
    )
    heatmap.update_layout(height=600)
    # include_plotlyjs="cdn" loads the exact Plotly version needed for all charts
    heatmap_html = heatmap.to_html(full_html=False, include_plotlyjs="cdn")

    # 2. Build distribution histograms cleanly into a list
    chart_cards = []
    for col in cols_to_plot:
        fig = px.histogram(
            x=df[col].to_list(),
            nbins=25,
            title=f"Distribution of {col} (Normalized)",
            labels={"x": col, "y": "Count"},
        )
        fig.update_layout(height=350, margin=dict(l=30, r=30, t=40, b=30))
        chart_html = fig.to_html(full_html=False, include_plotlyjs=False)
        chart_cards.append(f'<div class="card">{chart_html}</div>')

    # 3. Combine everything into one clean HTML dashboard
    dashboard_file = f"output/{base_name}_dashboard.html"
    html_content = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>{base_name} - Data Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; background: #f8f9fa; }}
            h1 {{ color: #222; }}
            .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.08); margin-bottom: 25px; }}
            .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        </style>
    </head>
    <body>
        <h1>Data Analysis Dashboard: {base_name}</h1>
        <p>Total cleaned rows: <b>{df.height}</b> | Total features analyzed: <b>{df.width}</b></p>
        <div class="card">
            {heatmap_html}
        </div>
        <div class="grid">
            {"".join(chart_cards)}
        </div>
    </body>
    </html>
    """

    with open(dashboard_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    return dashboard_file


def save_results(summary, corr_matrix, dashboard_file, base_name):
    summary_file = f"output/{base_name}_summary.csv"
    corr_file = f"output/{base_name}_correlation.csv"

    summary.write_csv(summary_file)
    corr_matrix.write_csv(corr_file)

    print("\nDone! Your results are saved in the 'output' folder:")
    print(" -", summary_file)
    print(" -", corr_file)
    print(" -", dashboard_file)

    # Automatically open the dashboard in the user's web browser
    webbrowser.open("file://" + os.path.abspath(dashboard_file))


def run_pipeline():
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

    os.makedirs("output", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]

    dashboard_file = create_dashboard(df, corr_matrix, base_name)
    save_results(summary, corr_matrix, dashboard_file, base_name)


if __name__ == "__main__":
    run_pipeline()
