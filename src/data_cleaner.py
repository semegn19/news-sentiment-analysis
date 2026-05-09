import pandas as pd

def clean_stock_data(df, ticker_name=None):
    """
    Clean and validate stock data
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw stock data
    ticker_name : str, optional
        Ticker symbol for logging
    
    Returns:
    --------
    pd.DataFrame : Cleaned stock data
    """
    ticker_prefix = f"[{ticker_name}] " if ticker_name else ""
    
    print(f"\n{ticker_prefix}DATA CLEANING")
    print("-" * 50)
    
    # Convert Date to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print(f"✅ Date column converted to datetime")
    
    # Ensure numeric columns are float
    numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    print(f"✅ Numeric columns converted")
    
    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)
    print(f"✅ Sorted by date")
    
    # Handle missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(f"⚠️ Missing values found:\n{missing[missing > 0]}")
        df = df.dropna(subset=numeric_cols)
        print(f"✅ Dropped rows with missing values")
    else:
        print(f"✅ No missing values found")
    
    # Remove duplicate dates
    if 'Date' in df.columns:
        duplicates = df.duplicated(subset=['Date']).sum()
        if duplicates > 0:
            df = df.drop_duplicates(subset=['Date'], keep='last')
            print(f"✅ Removed {duplicates} duplicate dates")
        else:
            print(f"✅ No duplicate dates")
    
    # Check OHLC logic
    violations = (df['High'] < df['Low']).sum()
    if violations > 0:
        print(f"⚠️ {violations} rows where High < Low")
        df = df[df['High'] >= df['Low']]
        print(f"✅ Removed invalid rows")
    else:
        print(f"✅ High >= Low for all rows")
    
    # Check zero volume
    zero_vol = (df['Volume'] == 0).sum()
    if zero_vol > 0:
        print(f"⚠️ {zero_vol} rows with zero volume")
    else:
        print(f"✅ All rows have positive volume")
    
    print(f"\n{ticker_prefix}Cleaned data: {len(df)} rows")
    print(f"   Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"   Close price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
    
    return df