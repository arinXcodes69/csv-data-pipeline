# CSV Data Analysis Pipeline

A fast, simple Python tool built with **Polars** that cleans, transforms, and analyzes any CSV dataset. Just run the script, enter your CSV file path, and get summary statistics and a correlation matrix saved automatically.

## What It Does
- **Cleans Data**: Removes rows with missing values (`?`, `NA`, `null`, etc.) and converts text columns into numerical dummy columns (`0`s and `1`s).
- **Normalizes Numbers**: Standardizes numerical columns while leaving binary dummy columns untouched.
- **Generates Reports**: Creates two CSV files inside an `output/` folder:
  - `<your_file>_summary.csv` (count, mean, std, min, max, etc.)
  - `<your_file>_correlation.csv` (correlation matrix across all numerical features)

## How to Use

1. **Clone this repository**
   ```bash
   git clone https://github.com
   cd csv-data-pipeline
   ```

2. **Install Polars**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the pipeline**
   ```bash
   python pipeline.py
   ```
   When prompted, paste the path to your CSV file (or drag and drop the file straight into your terminal) and press **Enter**.

## Project Structure
```text
csv-data-pipeline/
├── pipeline.py        # Main data cleaning & analysis script
├── requirements.txt   # Required Python packages
├── .gitignore         # Ignores generated output files
└── README.md          # Project guide
```
