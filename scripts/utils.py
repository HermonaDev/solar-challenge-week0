"""
Utility functions for solar data analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt

def load_country_data(country_name):
    """
    Load cleaned data for a specific country.
    
    Args:
        country_name (str): Name of country ('benin', 'sierra_leone', 'togo')
    
    Returns:
        pandas.DataFrame: Cleaned country data
    """
    filename = f"data/{country_name}_clean.csv"
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        print(f"File {filename} not found. Please run EDA first.")
        return None

def setup_plot_style():
    """Set consistent plotting style for all visualizations."""
    plt.style.use('seaborn-v0_8')
    plt.rcParams['figure.figsize'] = (10, 6)
EOF