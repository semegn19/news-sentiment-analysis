import pandas as pd
import talib

def calculate_moving_averages(df, windows=[5, 10, 20, 50, 200]):
    """
    Calculate SMA and EMA for multiple windows
    
    Parameters:
    -----------
    df : pd.DataFrame
        Stock data with 'Close' column
    windows : list, optional
        List of window periods
    
    Returns:
    --------
    pd.DataFrame : DataFrame with SMA and EMA columns added
    """
    if windows is None:
        windows = windows
    
    print(f"\n📊 Moving Averages (windows: {windows})")
    
    for window in windows:
        df[f'SMA_{window}'] = talib.SMA(df['Close'], timeperiod=window)
        df[f'EMA_{window}'] = talib.EMA(df['Close'], timeperiod=window)
        print(f"   ✅ SMA_{window} and EMA_{window} calculated")

    # Current SMA values (most recent)
    print(f"\n📊 Current Moving Averages (as of {df['Date'].iloc[-1].date()}):")
    print("-" * 50)
    print(f"   Close Price: ${df['Close'].iloc[-1]:.2f}")
    for window in windows:
        sma_val = df[f'SMA_{window}'].iloc[-1]
        ema_val = df[f'EMA_{window}'].iloc[-1]
        print(f"   SMA_{window}: ${sma_val:.2f}  |  EMA_{window}: ${ema_val:.2f}")

    # Price vs Moving Average signals
    print(f"\n📊 Price vs MA Signals:")
    for window in windows:
        current_price = df['Close'].iloc[-1]
        sma = df[f'SMA_{window}'].iloc[-1]
        
        if current_price > sma:
            print(f"   Price ABOVE SMA_{window} → Bullish signal")
        else:
            print(f"   Price BELOW SMA_{window} → Bearish signal")
    
    return df


def calculate_rsi(df, period=None, overbought=None, oversold=None):
    """
    Calculate RSI and generate signals
    
    Parameters:
    -----------
    df : pd.DataFrame
        Stock data with 'Close' column
    period : int, optional
        RSI period
    overbought : int, optional
        Overbought threshold
    oversold : int, optional
        Oversold threshold
    
    Returns:
    --------
    pd.DataFrame : DataFrame with RSI column added
    dict : RSI summary statistics
    """
    if period is None:
        period = 14
    if overbought is None:
        overbought = 70
    if oversold is None:
        oversold = 30
    
    print(f"\n📊 RSI (period={period})")
    
    df['RSI'] = talib.RSI(df['Close'], timeperiod=period)
    print(f"   ✅ RSI calculated")
    
    current_rsi = df['RSI'].iloc[-1]
    
    if current_rsi > overbought:
        signal = f"OVERBOUGHT (>{overbought}) → Sell signal"
    elif current_rsi < oversold:
        signal = f"OVERSOLD (<{oversold}) → Buy signal"
    else:
        signal = f"NEUTRAL (between {oversold} and {overbought})"
    
    print(f"   Current RSI: {current_rsi:.2f} → {signal}")
    
    summary = {
        'current_rsi': current_rsi,
        'overbought_days': (df['RSI'] > overbought).sum(),
        'oversold_days': (df['RSI'] < oversold).sum(),
        'neutral_days': len(df) - ((df['RSI'] > overbought).sum() + (df['RSI'] < oversold).sum()),
        'signal': signal
    }
    
    print(f"   Historical: {summary['overbought_days']} overbought, {summary['oversold_days']} oversold days")
    
    return df, summary


def calculate_macd(df, fast=None, slow=None, signal=None):
    """
    Calculate MACD and generate signals
    
    Parameters:
    -----------
    df : pd.DataFrame
        Stock data with 'Close' column
    fast, slow, signal : int, optional
        MACD parameters
    
    Returns:
    --------
    pd.DataFrame : DataFrame with MACD columns added
    dict : MACD summary statistics
    """
    if fast is None:
        fast = 12
    if slow is None:
        slow = 26
    if signal is None:
        signal = 9
    
    print(f"\n📊 MACD (fast={fast}, slow={slow}, signal={signal})")
    
    df['MACD'], df['MACD_signal'], df['MACD_histogram'] = talib.MACD(
        df['Close'], fastperiod=fast, slowperiod=slow, signalperiod=signal
    )
    print(f"   ✅ MACD calculated")
    
    current_macd = df['MACD'].iloc[-1]
    current_signal = df['MACD_signal'].iloc[-1]
    current_hist = df['MACD_histogram'].iloc[-1]
    
    # Detect crossovers
    bullish_crossover = False
    bearish_crossover = False
    
    if len(df) > 2:
        prev_macd = df['MACD'].iloc[-2]
        prev_signal = df['MACD_signal'].iloc[-2]
        bullish_crossover = (prev_macd <= prev_signal and current_macd > current_signal)
        bearish_crossover = (prev_macd >= prev_signal and current_macd < current_signal)
    
    summary = {
        'current_macd': current_macd,
        'current_signal': current_signal,
        'current_histogram': current_hist,
        'bullish_crossover': bullish_crossover,
        'bearish_crossover': bearish_crossover,
        'momentum': 'Bullish' if current_macd > current_signal else 'Bearish',
        'histogram_trend': 'Increasing' if current_hist > 0 else 'Decreasing'
    }
    
    print(f"   MACD Line: {current_macd:.4f} | Signal: {current_signal:.4f} | Histogram: {current_hist:.4f}")
    print(f"   Momentum: {summary['momentum']} | Histogram: {summary['histogram_trend']}")
    
    if bullish_crossover:
        print(f"   🔥 BULLISH CROSSOVER detected!")
    elif bearish_crossover:
        print(f"   ⚠️ BEARISH CROSSOVER detected!")
    
    return df, summary

def generate_signal_summary(df):
    """
    Generate overall technical signals summary.
    """

    print("\nTECHNICAL SIGNALS SUMMARY")
    print("=" * 60)

    signals = {
        'Indicator': [
            'SMA_20',
            'SMA_50',
            'RSI',
            'MACD'
        ],

        'Signal': [

            'Bullish'
            if df['Close'].iloc[-1] > df['SMA_20'].iloc[-1]
            else 'Bearish',

            'Bullish'
            if df['Close'].iloc[-1] > df['SMA_50'].iloc[-1]
            else 'Bearish',

            'Overbought'
            if df['RSI'].iloc[-1] > 70
            else (
                'Oversold'
                if df['RSI'].iloc[-1] < 30
                else 'Neutral'
            ),

            'Bullish'
            if df['MACD'].iloc[-1] > df['MACD_signal'].iloc[-1]
            else 'Bearish'
        ]
    }

    signals_df = pd.DataFrame(signals)

    print(signals_df.to_string(index=False))

    return signals_df
