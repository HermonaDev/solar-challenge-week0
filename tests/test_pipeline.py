"""
Unit tests for solar data pipeline.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.utils import SolarDataCleaner
import pandas as pd

def test_cleaner_initialization():
    """Test that SolarDataCleaner initializes correctly."""
    cleaner = SolarDataCleaner()
    assert cleaner.z_threshold == 3.0
    print("✅ Cleaner initialization test passed!")

def test_negative_value_correction():
    """Test negative value clipping functionality."""
    cleaner = SolarDataCleaner()
    
    # Create test data
    test_df = pd.DataFrame({
        'GHI': [-1, 0, 100, -5, 200],
        'Timestamp': ['2021-01-01 00:00'] * 5
    })
    
    # Test the cleaning method directly
    test_df = cleaner._standardize_timestamps(test_df)
    test_df = cleaner._correct_negative_solar_values(test_df)
    
    assert (test_df['GHI'] >= 0).all()
    print("✅ Negative value correction test passed!")

if __name__ == "__main__":
    test_cleaner_initialization()
    test_negative_value_correction()
    print("🎉 All tests passed!")