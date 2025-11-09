"""
End-to-End Solar Analysis Pipeline
Executes complete data processing and analysis workflow.
"""

from utils import SolarDataCleaner
import pandas as pd
import os

def main():
    """Execute complete solar data analysis pipeline."""
    print("🚀 Starting Solar Data Analysis Pipeline...")
    
    cleaner = SolarDataCleaner()
    countries = ['Benin', 'Sierra_leone', 'Togo']
    
    for country in countries:
        input_path = f'data/{country}.csv'
        output_path = f'data/{country}_clean.csv'
        
        if os.path.exists(input_path):
            # Clean data
            cleaned_data = cleaner.load_and_clean_country_data(input_path, country)
            
            # Save cleaned data
            cleaned_data.to_csv(output_path, index=False)
            print(f"✅ Saved cleaned data: {output_path}")
        else:
            print(f"⚠️  File not found: {input_path}")
    
    print("🎉 Pipeline execution completed!")

if __name__ == "__main__":
    main()