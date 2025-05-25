#Analyze the behavior of business work in the last quarter of 2024

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def main():

    dir = Path(__file__).resolve().parent
    csv_file = dir / 'data' / 'bussines-employment.cvs'
    print(f'Charging csv file from:{csv_file}')
    df = pd.read_csv(csv_file)    
    print(df.head())

    if df is not None:
        print("Success! File charged!")
        print("\n First 5 rows from dataset")
        print(df.head())
        print("\n Last 5 rows from dataset")
        print(df.tail())
    else:
        print("Error! File not charged!")

if __name__=='__main__':
    main()

