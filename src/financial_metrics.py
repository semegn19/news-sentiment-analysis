import numpy as np

def calculate_returns(df):
    """
    Calculate daily and cumulative returns
    
    Parameters:
    -----------
    df : pd.DataFrame
        Stock data with 'Close' column
    
    Returns:
    --------
    pd.DataFrame : DataFrame with return columns added
    """
    print(f"\n📊 Return Calculations")
    
    df['Daily_Return'] = df['Close'].pct_change()
    df['Cumulative_Return'] = (1 + df['Daily_Return']).cumprod() - 1
    
    current_cum_return = df['Cumulative_Return'].iloc[-1]
    print(f"   Daily returns calculated")
    print(f"   Cumulative return: {current_cum_return*100:.2f}%")
    
    return df, current_cum_return


def calculate_volatility(df, window=None):
    """
    Calculate volatility metrics
    
    Parameters:
    -----------
    df : pd.DataFrame
        Stock data with 'Daily_Return' column
    window : int, optional
        Rolling window for volatility
    
    Returns:
    --------
    pd.DataFrame : DataFrame with volatility columns
    dict : Volatility metrics
    """
    if window is None:
        window = 30
    
    print(f"\n📊 Volatility Metrics")
    
    daily_volatility = df['Daily_Return'].std()
    annualized_volatility = daily_volatility * np.sqrt(252)
    
    df['Rolling_Volatility_30'] = df['Daily_Return'].rolling(window=window).std() * np.sqrt(252)
    
    metrics = {
        'daily_volatility': daily_volatility,
        'annualized_volatility': annualized_volatility,
        'annualized_volatility_pct': annualized_volatility * 100
    }
    
    print(f"   Daily volatility: {daily_volatility:.4f}")
    print(f"   Annualized volatility: {annualized_volatility*100:.2f}%")
    
    return df, metrics


def calculate_sharpe_ratio(df, risk_free_rate=None):
    """
    Calculate Sharpe ratio
    
    Parameters:
    -----------
    df : pd.DataFrame
        Stock data with 'Daily_Return' column
    risk_free_rate : float, optional
        Annual risk-free rate
    
    Returns:
    --------
    float : Sharpe ratio
    """
    if risk_free_rate is None:
        risk_free_rate = 0.02
    
    print(f"\n📊 Sharpe Ratio")
    
    daily_volatility = df['Daily_Return'].std()
    annualized_volatility = daily_volatility * np.sqrt(252)
    annual_return = df['Daily_Return'].mean() * 252
    
    sharpe_ratio = (annual_return - risk_free_rate) / annualized_volatility
    
    print(f"   Annual return: {annual_return*100:.2f}%")
    print(f"   Risk-free rate: {risk_free_rate*100:.1f}%")
    print(f"   Sharpe Ratio: {sharpe_ratio:.4f}")
    
    if sharpe_ratio > 1:
        print(f"   → Good risk-adjusted returns")
    elif sharpe_ratio > 0:
        print(f"   → Moderate risk-adjusted returns")
    else:
        print(f"   → Poor risk-adjusted returns")
    
    return sharpe_ratio


def calculate_max_drawdown(df):
    """
    Calculate maximum drawdown
    
    Parameters:
    -----------
    df : pd.DataFrame
        Stock data with 'Close' column
    
    Returns:
    --------
    float : Maximum drawdown percentage
    pd.DataFrame : DataFrame with drawdown column
    """
    print(f"\n📊 Maximum Drawdown")
    
    df['Rolling_Max'] = df['Close'].cummax()
    df['Drawdown'] = (df['Close'] - df['Rolling_Max']) / df['Rolling_Max']
    max_drawdown = df['Drawdown'].min()
    
    print(f"   Max Drawdown: {max_drawdown*100:.2f}%")
    
    return df, max_drawdown