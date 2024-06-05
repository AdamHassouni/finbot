from datetime import datetime, timedelta
import numpy as np
from scipy.stats import norm

def calculate_atr(api, symbol: str, period: int = 14) -> float:
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=period*2)).strftime('%Y-%m-%d')
    bars = api.get_bars(symbol, '1D', start=start_date, end=end_date, feed='iex').df

    high_low = bars['high'] - bars['low']
    high_close = np.abs(bars['high'] - bars['close'].shift())
    low_close = np.abs(bars['low'] - bars['close'].shift())
    ranges = np.column_stack([high_low, high_close, low_close])
    true_range = np.max(ranges, axis=1)
    atr = np.mean(true_range[-period:])
    return atr

def calculate_var(returns, confidence_level=0.95):
    """Calculate Value at Risk (VaR) using historical returns."""
    mean = np.mean(returns)
    std_dev = np.std(returns)
    var = norm.ppf(1 - confidence_level, mean, std_dev)
    return var

def calculate_cvar(returns, confidence_level=0.95):
    """Calculate Conditional Value at Risk (CVaR) using historical returns."""
    var = calculate_var(returns, confidence_level)
    cvar = np.mean(returns[returns < var])
    return cvar

def calculate_turbulence(api, symbol: str, lookback_period: int = 252) -> float:
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=lookback_period * 2)).strftime('%Y-%m-%d')
    bars = api.get_bars(symbol, '1D', start=start_date, end=end_date, feed='iex').df

    returns = bars['close'].pct_change().dropna()
    mean_returns = returns.mean()

    # Convert returns to a DataFrame to calculate the covariance matrix
    returns_df = returns.to_frame(name='returns')
    cov_matrix = returns_df.cov()

    # Calculate turbulence index
    turbulence_index = ((returns - mean_returns)**2) / cov_matrix.iloc[0, 0]
    turbulence = np.mean(turbulence_index)
    return turbulence

def advanced_position_sizing(returns, cash, last_price, atr, probability):
    """
    Advanced position sizing using Kelly Criterion, VaR, and CVaR.
    
    Parameters:
    - returns: Historical returns of the asset.
    - cash: Available cash.
    - last_price: Last price of the asset.
    - atr: Average True Range of the asset.
    - probability: Probability of the trade being successful.
    """
    # Calculate Kelly fraction
    b = 2  # Assume a risk/reward ratio of 2:1
    p = probability
    q = 1 - p
    f_star = (b * p - q) / b

    # Risk per trade using Kelly criterion
    risk_per_trade_kelly = cash * f_star
    
    # Ensure risk per trade does not exceed max loss per trade
    max_loss_dollar = 0.02 * cash  # 2% max loss per trade
    if risk_per_trade_kelly > max_loss_dollar:
        risk_per_trade_kelly = max_loss_dollar
    
    # Calculate VaR and CVaR
    var = calculate_var(returns)
    cvar = calculate_cvar(returns)
    
    # Adjust risk per trade based on VaR and CVaR
    adjusted_risk_per_trade = min(risk_per_trade_kelly, abs(var) * cash, abs(cvar) * cash)
    
    # Calculate stop loss price
    stop_loss_price = last_price - atr - (last_price * 0.02)  # Adding a 2% buffer to ATR-based stop loss
    risk_per_share = last_price - stop_loss_price
    
    # Calculate the number of shares to buy/sell
    max_shares = round((adjusted_risk_per_trade / risk_per_share).item(), 0)
    
    return cash, last_price, max_shares, atr

