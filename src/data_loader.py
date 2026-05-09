import pandas as pd
import os

def load_data(filepath):
    """
    Load data from CSV file
    
    Parameters:
    -----------
    filepath : str
        Path to CSV file
    
    Returns:
    --------
    pd.DataFrame : Loaded and validated data
    """
    df = pd.read_csv(filepath)
    print(f"✅ Loaded: {os.path.basename(filepath)}")
    print(f"   Shape: {df.shape} rows × {df.shape[1]} columns")
    print(f"   Columns: {df.columns.tolist()}")
    return df