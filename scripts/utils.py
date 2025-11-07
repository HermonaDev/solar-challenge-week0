"""
Utility functions for solar data analysis and visualization.
Reusable components for data cleaning, analysis, and plotting.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class SolarDataCleaner:
    """
    Unified pipeline for cleaning solar farm data across countries.
    """
    
    def __init__(self):
        self.solar_columns = ['GHI', 'DNI', 'DHI', 'ModA', 'ModB']
    
    def load_and_clean(self, filepath, country_name):
        """
        Load and clean country-specific solar data.
        
        Args:
            filepath (str): Path to CSV file
            country_name (str): Country name for logging
            
        Returns:
            pandas.DataFrame: Cleaned dataset
        """
        print(f"🔄 Cleaning {country_name} data...")
        
        df = pd.read_csv(filepath)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Remove empty comments column
        if 'Comments' in df.columns and df['Comments'].isna().all():
            df = df.drop('Comments', axis=1)
        
        # Fix negative solar values
        for col in self.solar_columns:
            if col in df.columns:
                df[col] = df[col].clip(lower=0)
        
        print(f"✅ {country_name} cleaned: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

def setup_plot_style():
    """Set consistent plotting style for all visualizations."""
    plt.style.use('seaborn')
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['font.size'] = 12

def detect_outliers_zscore(df, columns, threshold=3):
    """
    Detect outliers using Z-score method.
    
    Args:
        df (pd.DataFrame): Input data
        columns (list): Columns to check
        threshold (float): Z-score threshold
        
    Returns:
        dict: Outlier counts per column
    """
    outliers = {}
    for col in columns:
        if col in df.columns:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            outlier_count = (z_scores > threshold).sum()
            outliers[col] = outlier_count
    return outliers