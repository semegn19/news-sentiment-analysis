from datetime import timedelta

def align_to_trading_day(date, trading_dates_set, max_lookahead=5):
    """
    Align a news date to the next available trading day.
    
    Parameters:
    -----------
    date : datetime or date
        The publication date of the news article
    trading_dates_set : set
        Set of available trading dates
    max_lookahead : int
        Maximum days to look ahead for next trading day
    
    Returns:
    --------
    aligned_date : date or None
        The aligned trading day, or None if not found
    """
    input_date = date.date() if hasattr(date, 'date') else date
    
    # Check if it's a trading day
    if input_date in trading_dates_set:
        return input_date
    
    # Look ahead for next trading day
    for offset in range(1, max_lookahead + 1):
        next_day = input_date + timedelta(days=offset)
        if next_day in trading_dates_set:
            return next_day
    
    # Also check previous day (for very late publishing)
    for offset in range(1, 3):
        prev_day = input_date - timedelta(days=offset)
        if prev_day in trading_dates_set:
            return prev_day
    
    return None