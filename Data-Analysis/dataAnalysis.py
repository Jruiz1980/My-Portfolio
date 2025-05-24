#Analyze the behavior of business work in the last quarter of 2024

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set a style for seaborn plots for better aesthetics
sns.set_style("whitegrid")

def load_and_inspect_data(csv_file_path):
    """
    Loads data from a CSV file and performs initial inspection.
    """
    try:
        df = pd.read_csv(csv_file_path)
        print("Data loaded successfully!")
        print("\nFirst 5 rows of the dataset:")
        print(df.head())
        print("\nDataset information:")
        df.info()
        print("\nDescriptive statistics for numerical columns:")
        print(df.describe())
        print("\nMissing values per column:")
        print(df.isnull().sum())
        return df
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading or inspecting the data: {e}")
        return None

def clean_data(df):
    """
    Performs basic data cleaning.
    This is a placeholder and should be customized.
    """
    if df is None:
        return None
    
    print("\nCleaning data...")
    # Example: Fill missing numerical values with the mean
    # Replace 'numerical_column_name' with actual column names from your CSV
    # for col in df.select_dtypes(include=np.number).columns:
    #     if df[col].isnull().any():
    #         df[col].fillna(df[col].mean(), inplace=True)
    #         print(f"Filled missing values in '{col}' with its mean.")

    # Example: Fill missing categorical values with the mode
    # Replace 'categorical_column_name' with actual column names
    # for col in df.select_dtypes(include='object').columns:
    #     if df[col].isnull().any():
    #         df[col].fillna(df[col].mode()[0], inplace=True) # mode() can return multiple values if they have same frequency
    #         print(f"Filled missing values in '{col}' with its mode.")
            
    # Or, you might decide to drop rows with any missing values
    # df_cleaned = df.dropna()
    # print(f"Original rows: {len(df)}, Rows after dropping NA: {len(df_cleaned)}")
    # return df_cleaned
    
    print("Data cleaning step placeholder. Customize as needed.")
    return df # Return the original df if no specific cleaning is applied here

def perform_exploratory_data_analysis(df):
    """
    Performs exploratory data analysis (EDA) with visualizations.
    This should be customized based on your dataset's columns.
    """
    if df is None:
        print("DataFrame is None, skipping EDA.")
        return

    print("\nPerforming Exploratory Data Analysis (EDA)...")

    # --- Customize these examples based on your actual column names and data types ---

    # Example 1: Distribution of a numerical column
    # Replace 'numerical_column' with a relevant column name from your CSV
    # if 'numerical_column' in df.columns:
    #     plt.figure(figsize=(10, 6))
    #     sns.histplot(df['numerical_column'], kde=True, bins=30)
    #     plt.title('Distribution of Numerical Column')
    #     plt.xlabel('Value')
    #     plt.ylabel('Frequency')
    #     plt.show()
    # else:
    #     print("Skipping histogram: 'numerical_column' not found.")

    # Example 2: Count plot for a categorical column
    # Replace 'categorical_column' with a relevant column name
    # if 'categorical_column' in df.columns:
    #     plt.figure(figsize=(10, 6))
    #     sns.countplot(y=df['categorical_column'], order = df['categorical_column'].value_counts().index)
    #     plt.title('Count of Categorical Column')
    #     plt.xlabel('Count')
    #     plt.ylabel('Category')
    #     plt.tight_layout() # Adjust layout to prevent labels from overlapping
    #     plt.show()
    # else:
    #     print("Skipping count plot: 'categorical_column' not found.")

    # Example 3: Relationship between two numerical columns
    # Replace 'numerical_column1' and 'numerical_column2'
    # if 'numerical_column1' in df.columns and 'numerical_column2' in df.columns:
    #     plt.figure(figsize=(10, 6))
    #     sns.scatterplot(x=df['numerical_column1'], y=df['numerical_column2'])
    #     plt.title('Relationship between Numerical Column 1 and Numerical Column 2')
    #     plt.xlabel('Numerical Column 1')
    #     plt.ylabel('Numerical Column 2')
    #     plt.show()
    # else:
    #     print("Skipping scatter plot: One or both numerical columns not found.")
        
    # Example 4: Correlation heatmap for numerical features
    # numerical_df = df.select_dtypes(include=np.number)
    # if not numerical_df.empty:
    #     plt.figure(figsize=(12, 8))
    #     correlation_matrix = numerical_df.corr()
    #     sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    #     plt.title('Correlation Heatmap of Numerical Features')
    #     plt.show()
    # else:
    #     print("Skipping correlation heatmap: No numerical columns found or left after cleaning.")

    print("\nEDA examples are placeholders. Please uncomment and customize them with your actual column names.")
    print("Consider what business questions you want to answer to guide your EDA.")


def main():
    """
    Main function to run the data analysis pipeline.
    """
    # --- IMPORTANT: Replace 'your_data.csv' with the path to your CSV file ---
    csv_file_path = './emp-data-dec-2024-q/business-employment.csv'
    
    # 1. Load and Inspect Data
    df = load_and_inspect_data(csv_file_path)
    
    if df is not None:
        # 2. Clean Data (customize this function based on your needs)
        df_cleaned = clean_data(df.copy()) # Use .copy() to avoid modifying the original DataFrame directly in cleaning
        
        # 3. Perform Exploratory Data Analysis (customize this function)
        perform_exploratory_data_analysis(df_cleaned)
        
        # Further analysis can be added here:
        # - Feature engineering
        # - Statistical testing
        # - More advanced visualizations
        # - Answering specific business questions
        
        print("\nData analysis script finished.")
        print("Remember to customize the cleaning and EDA sections for your specific dataset and objectives.")

if __name__ == '__main__':
    main()