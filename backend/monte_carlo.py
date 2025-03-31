import numpy as np
import pandas as pd
import yfinance as yf

def montecarlosim(ticker, days=100, sims=500):

    data = yf.download(ticker, period='5y', group_by='ticker')

    # Fix for MultiIndex issue
    close_col = (ticker, 'Close')

    if close_col not in data:
        raise KeyError(f"Column '{close_col}' not found in data. Available: {data.columns}")

    last_price = data[close_col].iloc[-1]

    # Calculate log returns
    log_returns = np.log(data[close_col] / data[close_col].shift(1))
    drift = log_returns.mean() - (0.5 * log_returns.var())
    volatility = log_returns.std()

    # store simulations
    simulated_prices = np.zeros((days, sims))
    simulated_prices[0] = last_price

    # Monte Carlo Simulation
    for day in range(1, days):
        random_shock = np.random.normal(0, 1, sims)
        simulated_prices[day] = simulated_prices[day - 1] * np.exp(drift + volatility * random_shock)

    return simulated_prices
