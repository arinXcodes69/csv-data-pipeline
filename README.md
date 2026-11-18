# CSV Data Analysis Pipeline

A Python tool using **Polars** and **Plotly** to clean, transform, and analyze CSV datasets, generating summary reports, correlation matrices, and interactive browser dashboards.

## Features
- **Data Cleaning**: Drops rows with missing values (`?`, `NA`, `null`) and encodes text columns into binary dummy columns.
- **Normalization**: Scales numerical columns while preserving binary variables.
- **Output Files**: Generates an `output/` directory containing `<your_file>_summary.csv`, `<your_file>_correlation.csv`, and an interactive `<your_file>_dashboard.html`.

## Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com
   cd csv-data-pipeline
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script**
   ```bash
   python Pipeline.py
   ```
   Provide your CSV file path when prompted.

## Project Structure
```text
csv-data-pipeline/
├── Pipeline.py        # Main execution script
├── requirements.txt   # Python dependencies
├── .gitignore         # Excludes output files
├── LICENSE            # MIT License
└── README.md          # Documentation
```
