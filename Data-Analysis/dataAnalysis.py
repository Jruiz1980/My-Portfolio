#Analyze the behavior of business work until the last quarter of 2024

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set a style for seaborn plots for better aesthetics
sns.set_style("whitegrid")

def load_and_inspect_data(csv_file_path):
    """
    Loads data from a CSV file and performs initial inspection.
    """
    print(f"Attempting to load CSV file from: {csv_file_path}")
    try:
        df = pd.read_csv(csv_file_path)
        print("Success! The CSV file was loaded correctly.")
        print("\nFirst 5 rows of the dataset:")
        print(df.head())
        print("\nLast 5 rows of the dataset:")
        print(df.tail())
        print("\nDataset information:")
        df.info()
        print("\nDescriptive statistics for numerical columns:")
        print(df.describe())
        print("\nNull values per column:")
        print(df.isnull().sum())
        return df
    except FileNotFoundError:
        print(f"Error: The file could not be found at the path: {csv_file_path}")
        print("Please verify that the 'data' folder exists in the same directory as your script, and that the CSV file is inside 'data' with the correct name and extension.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the file: {e}")
        return None

def clean_data(df):
    """
    Performs basic data cleaning.
    This is a placeholder and should be customized.
    """
    if df is None:
        return None
    print("\nCleaning data... (placeholder)")
    # Cleaning steps would go here, for example:
    df_cleaned = df.dropna() # Example: remove rows with null values
    print("Data after cleaning (example: dropna):")
    print(df_cleaned.head())
    print(f"Original rows: {len(df)}, Rows after dropna: {len(df_cleaned)}")
    return df # For now, return the original df

def perform_exploratory_data_analysis(df):
    """
    Performs exploratory data analysis (EDA) with visualizations.
    This should be customized based on your dataset's columns.
    """
    if df is None:
        print("DataFrame is None, skipping EDA.")
        return
    
    print("\nPerforming Exploratory Data Analysis (EDA)...")

    # --- EXAMPLE: TREND GRAPH VS TIME ---
    # Replace 'date_column_name' with the actual name of your date/time column.
    # Replace 'value_column_name' with the actual name of the numerical column you want to analyze.

    date_column_name = 'Period' # Time/date column
    value_column_name = 'Data_value'   # Column with numerical values

    if date_column_name in df.columns and value_column_name in df.columns:
        print(f"\nGenerating trend graph for '{value_column_name}' vs '{date_column_name}'...")
        
        # Copy to avoid modifying the original DataFrame in this function
        df_temp = df.copy()

        # --- Optional: Filter data before plotting ---
        # Example: Analyze "Filled jobs" for "Agriculture, Forestry and Fishing" with "Actual" data
        series_filter = "Filled jobs"
        industry_filter = "Agriculture, Forestry and Fishing"
        adjustment_filter = "Actual" # Could also be "Seasonally adjusted" or "Trend"

        if 'Series_title_1' in df_temp.columns and 'Series_title_2' in df_temp.columns and 'Series_title_3' in df_temp.columns:
            df_temp = df_temp[
                (df_temp['Series_title_1'] == series_filter) &
                (df_temp['Series_title_2'] == industry_filter) &
                (df_temp['Series_title_3'] == adjustment_filter)
            ]
            print(f"Data filtered for: Series='{series_filter}', Industry='{industry_filter}', Adjustment='{adjustment_filter}'")
            if df_temp.empty:
                print("Warning: The DataFrame is empty after applying filters. The graph will not be generated.")
                return
        else:
            print("Warning: Not all filter columns (Series_title_1, Series_title_2, Series_title_3) were found. All data will be plotted if 'Period' and 'Data_value' exist.")

        # Step 1: Ensure the date column is datetime
        # The 'Period' column (e.g., 2011.06) needs special conversion.
        # .03 -> Month 3 (March), .06 -> Month 6 (June), .09 -> Month 9 (September), .12 -> Month 12 (December)
        try:
            # Convert 'Period' (e.g., 2011.06) to an end-of-quarter date
            def convert_period_to_date(period_val):
                year_val = int(period_val)
                month_map_val = {'.03': 3, '.06': 6, '.09': 9, '.12': 12}
                # month_str = str(period_val - year_val)[:3] # Get the decimal part as a string (e.g., ".06") # This line is not strictly necessary for the logic below
                month_val = month_map_val.get(f"{period_val - year_val:.2f}"[-3:], 1) # Get the decimal part as a string (e.g., ".06") and map
                return pd.Timestamp(year=year_val, month=month_val, day=1) + pd.offsets.MonthEnd(0)
            df_temp[date_column_name] = df_temp[date_column_name].apply(convert_period_to_date)
            print(f"Column '{date_column_name}' converted to datetime (or was already).")
        except Exception as e:
            print(f"Error converting column '{date_column_name}' to datetime: {e}")
            print("Ensure the column contains valid dates and consider specifying the 'format' argument in pd.to_datetime() if necessary.")
            return # Exit if date conversion fails

        # Optional: Sort by date if not already sorted
        df_temp = df_temp.sort_values(by=date_column_name)

        # Step 2: Create the graph
        plt.figure(figsize=(12, 6)) # Graph size
        sns.lineplot(x=date_column_name, y=value_column_name, data=df_temp, marker='o')
        
        plt.title(f'Trend of {series_filter} in {industry_filter} ({adjustment_filter})')
        plt.xlabel('Time / Date')
        plt.ylabel(value_column_name)
        plt.xticks(rotation=45) # Rotate X-axis labels for better readability if there are many dates
        plt.tight_layout() # Adjust layout to make sure everything fits well
        plt.show() # Show the graph
    else:
        print(f"Warning: Columns '{date_column_name}' or '{value_column_name}' not found for the trend graph.")

    # Other analyses and visualizations could go here...
    # Histogram example (if you already had it):
    if 'numerical_column_name' in df.columns: # Replace 'numerical_column_name' with an actual column name
        plt.figure(figsize=(10, 6))
        sns.histplot(df['numerical_column_name'], kde=True) # Replace 'numerical_column_name'
        plt.title('Distribution of My Numerical Column') # Example title
        plt.show()


def main():
    script_dir = Path(__file__).resolve().parent
    csv_file_name = 'business-employment.csv' # Make sure this is the correct name
    csv_file_path = script_dir / 'data' / csv_file_name
    
    # 1. Load and Inspect Data
    df = load_and_inspect_data(csv_file_path)
    
    if df is not None:
        # 2. Clean Data (customize this function according to your needs)
        df_cleaned = clean_data(df.copy()) # Use .copy() to avoid modifying the original DataFrame directly
        
        # 3. Perform Exploratory Data Analysis (customize this function)
        perform_exploratory_data_analysis(df_cleaned)
        
        print("\nData analysis script finished.")

if __name__=='__main__':
    main()