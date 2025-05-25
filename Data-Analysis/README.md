# Overview

As a software engineer, my goal with this project is to deepen my data analysis skills using Python. I aim to practice the complete data workflow, from initial loading and cleaning to exploration and visualization, to extract meaningful insights and present them clearly. This exercise allows me to become more familiar with essential Python libraries for data science and improve my ability to transform raw data into actionable knowledge.

The dataset analyzed in this project is "Business Employment Data," which appears to contain information on employment across various industries over time, broken down by different series and adjustment types (e.g., actual, seasonally adjusted). The data includes columns such as Period, Data_value, Series_title_1 (e.g., "Filled jobs"), Series_title_2 (e.g., industry name), and Series_title_3 (e.g., adjustment type).
You can find the original dataset here: Statistics New Zealand - Business employment data (Please ensure this link is correct or update it).

The purpose of this software is to load, inspect, perform basic cleaning, and conduct exploratory data analysis of the employment data. Specifically, the script attempts to visualize trends over time for specific data subsets, such as the number of "Filled jobs" in the "Agriculture, Forestry and Fishing" sector using "Actual" data. This helps in understanding patterns and behaviors in the labor market based on the provided data.

[Software Demo Video](https://youtu.be/_RZVJeIo7cw)

# Data Analysis Results

Upon executing the script with the business-employment.csv dataset, the following questions are addressed through visualization:

* Question: What is the trend of "Filled jobs" in the "Agriculture, Forestry and Fishing" sector using "Actual" data over time, up to the last quarter recorded in the dataset?

* Answer: The script generates a line graph showing the evolution of the Data_value (representing the number of jobs) across periods (converted to quarterly dates). The shape of the graph (upward, downward, fluctuating) would reveal the specific trend. For example, if the line shows a general upward slope, it would indicate growth in jobs for that specific sector and data type over time.

**Initial Data Inspection:**

The script displays the first and last rows of the dataset, general information (data types, non-null counts), descriptive statistics for numerical columns, and the count of null values per column. This provides an initial understanding of the data's structure and quality.

# Development Environment

A standard Python development environment was used to develop this software. The main tools include:

* A code editor or IDE (e.g., VS Code, PyCharm, Jupyter Notebook).
* Python interpreter (version 3.x).
* Terminal or command line to run the script.
The programming language used is Python. The following key libraries were employed:

* **Pandas:** For loading, manipulating, and analyzing tabular data (DataFrames).
* **NumPy:** For efficient numerical operations (though its direct use is minimal in this script, Pandas relies on it).
* **Matplotlib:** For creating static graphs and visualizations.
* **Seaborn:** For creating more attractive and complex statistical visualizations, built on top of Matplotlib.
* **Pathlib:** For handling file paths in a more object-oriented and cross-platform manner.

# Useful Websites

During the development of this project and for a better understanding of the tools used, the following websites were very helpful:

* [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
* [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)
* [Seaborn Documentation](https://seaborn.pydata.org/)
* [Python Official Documentation](https://docs.python.org/3/)
* [Stack Overflow (For resolving specific programming queries)](https://stackoverflow.com/)
* [GeeksforGeeks (For Python tutorials and examples)](https://www.geeksforgeeks.org/)

# Future Work

Future Work
To improve and expand this data analysis project, the following points could be considered:

* **Enhance Data Cleaning:** The clean_data function is currently a placeholder. More robust cleaning could be implemented, such as specific handling of outliers, more intelligent imputation of missing data (instead of just dropna()), or correction of data types if necessary.
* **Expand Exploratory Data Analysis (EDA):**
    * Add more types of visualizations (histograms for distributions, box plots for group comparisons, heatmaps for correlations).
    * Allow the user to interactively select columns and filters for the graphs.
    * Analyze other combinations of Series_title_1, Series_title_2, and Series_title_3.
* **More Detailed Error Handling:** Although there's basic FileNotFoundError handling, more try-except blocks could be added for specific operations that might fail (e.g., data type conversions in specific columns).
* **Parameterization:** Make key column names (like Period, Data_value, Series_title_1, etc.) and filters configurable parameters instead of hardcoding them directly within the perform_exploratory_data_analysis function.
* **Unit Tests:** Add tests to ensure that functions (especially load_and_inspect_data, clean_data, and date conversion) behave as expected.
* **Modularization:** If the script grows significantly, it could be divided into smaller modules for better organization.
* **Report Generation:** Save the generated graphs to files and potentially create a summarized report (e.g., in PDF or HTML) with the findings.