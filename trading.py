import pandas as pd
import numpy as np
import yfinance as yf
from post_trade_analysis import PostTradeAnalysis

# Function to build the trading strategy based on Simple Moving Averages (SMA)
def strategy_build(df):
    # Calculate the 9-day SMA
    df['SMA_9'] = df['Close'].rolling(window=9).mean()
    # Calculate the 20-day SMA
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    
    # Initialize the signal column to 0 (no action)
    df['signal'] = 0
    
    # Generate buy signals (1) when SMA_9 crosses above SMA_20
    df['signal'][9:] = np.where(df['SMA_9'][9:] > df['SMA_20'][9:], 1, 0)
    
    # Generate sell signals (-1) when SMA_9 crosses below SMA_20
    df['signal'][9:] = np.where(df['SMA_9'][9:] < df['SMA_20'][9:], -1, df['signal'][9:])
    
    return df

# Class to execute trades based on the generated signals
class TradingExecution:
    def __init__(self, df):
        self.df = df  # DataFrame containing stock data and signals
        self.position = 0  # Variable to track current position (0 = no position, 1 = holding stock)
        self.buy_price = 0  # Variable to store the price at which the stock was bought
        self.df['returns'] = 0.0  # Column to track returns from trades

    # Method to run the trading strategy over the given time period
    def run(self, symbol, start_date, end_date):
        for i in range(len(self.df)):
            # Execute a buy if the signal is 1 and no stock is currently held
            if self.df['signal'].iloc[i] == 1 and self.position == 0:
                self.position = 1
                self.buy_price = self.df['Close'].iloc[i]
                print(f"Buy at {self.buy_price} on {self.df.index[i]}")
            
            # Execute a sell if the signal is -1 and the stock is currently held
            elif self.df['signal'].iloc[i] == -1 and self.position == 1:
                sell_price = self.df['Close'].iloc[i]
                returns = (sell_price - self.buy_price) / self.buy_price
                self.df['returns'].iloc[i] = returns
                print(f"Sell at {sell_price} on {self.df.index[i]} with return {returns}")
                self.position = 0

            # Execute a sell if the stop-loss condition is met (price falls below 95% of buy price)
            elif self.position == 1 and (self.df['Close'].iloc[i] < self.buy_price * 0.95):
                sell_price = self.df['Close'].iloc[i]
                returns = (sell_price - self.buy_price) / self.buy_price
                self.df['returns'].iloc[i] = returns
                print(f"Sell at {sell_price} on {self.df.index[i]} with return {returns} (stop loss)")
                self.position = 0
        
        # Return the series of non-zero returns
        returns_series = self.df[self.df['returns'] != 0]['returns']
        return returns_series

# Function to fetch historical stock data using yfinance
def fetch_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Main block to run the entire process
if __name__ == "__main__":
    # Define stock symbol and date range
    symbol = 'RELIANCE.NS'
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    # Fetch historical data for the defined stock and date range
    df = fetch_data(symbol, start_date, end_date)
    
    # Build the strategy signals
    df = strategy_build(df)
    
    # Initialize the trading execution class and run the strategy
    trader = TradingExecution(df)
    returns_series = trader.run(symbol, start_date, end_date)
    
    # Perform post-trade analysis on the returns
    analysis = PostTradeAnalysis(returns_series)
    analysis.generate_plots()  # Generate plots of the trading performance
    analysis.generate_monthly_returns_heatmap()  # Generate a heatmap of monthly returns
