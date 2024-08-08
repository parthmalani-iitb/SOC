
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import seaborn as sns

# Class for handling stock data, including fetching, processing, and analyzing
class DataHandler:
    def __init__(self, symbol, start_date, end_date, timeframe='1d'):
        self.symbol = symbol  # Stock symbol
        self.start_date = start_date  # Start date for fetching data
        self.end_date = end_date  # End date for fetching data
        self.timeframe = timeframe  # Time interval (daily by default)
        self.data = self.fetch_data()  # Fetch the data upon initialization
    
    # Method to fetch historical data using yfinance
    def fetch_data(self):
        ticker = yf.Ticker(self.symbol)
        data = ticker.history(start=self.start_date, end=self.end_date, interval=self.timeframe)
        data.reset_index(inplace=True)  # Reset the index to include the date as a column
        return data

    # Method to generate a summary of the data
    def data_summary(self):
        summary = {
            'Data Size': self.data.shape,  # Size of the data (rows, columns)
            'Missing Values': self.data.isnull().sum(),  # Count of missing values
            'Mean': self.data.mean(),  # Mean of each column
            'Median': self.data.median(),  # Median of each column
            'Standard Deviation': self.data.std()  # Standard deviation of each column
        }
        return summary

    # Method to handle missing data
    def handle_missing_values(self, method='ffill'):
        # Forward fill (ffill), backward fill (bfill), or drop missing values
        if method == 'ffill':
            self.data.fillna(method='ffill', inplace=True)
        elif method == 'bfill':
            self.data.fillna(method='bfill', inplace=True)
        elif method == 'drop':
            self.data.dropna(inplace=True)
        else:
            raise ValueError("Method should be one of 'ffill', 'bfill', or 'drop'")
        return self.data

    # Method to compare stock performance against the Nifty 50 index
    def performance_analysis(self):
        # Fetch Nifty 50 index data for the same period
        nifty = yf.Ticker('^NSEI')  # Nifty 50 Index
        nifty_data = nifty.history(start=self.start_date, end=self.end_date, interval=self.timeframe)
        
        # Calculate cumulative returns for the stock
        self.data['Cumulative Return'] = (1 + self.data['Close'].pct_change()).cumprod() - 1
        # Calculate cumulative returns for Nifty 50
        nifty_data['Cumulative Return'] = (1 + nifty_data['Close'].pct_change()).cumprod() - 1
        
        # Plot cumulative returns of the stock and Nifty 50
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Date'], self.data['Cumulative Return'], label=f'{self.symbol} Cumulative Return')
        plt.plot(nifty_data.index, nifty_data['Cumulative Return'], label='Nifty 50 Cumulative Return', color='orange')
        plt.title(f'Performance of {self.symbol} vs Nifty 50')  # Plot title
        plt.xlabel('Date')  # X-axis label
        plt.ylabel('Cumulative Return')  # Y-axis label
        plt.legend()  # Show legend
        plt.grid(True)  # Enable grid lines
        plt.show()

# Main block to run the data handling and analysis
if __name__ == "__main__":
    symbol = 'RELIANCE.NS'  # Stock symbol for Reliance
    start_date = '2020-01-01'  # Start date for fetching data
    end_date = '2023-06-30'  # End date for fetching data
    
    data_handler = DataHandler(symbol, start_date, end_date)  # Initialize the DataHandler class
    print(data_handler.data_summary())  # Print the summary of the data
    data_handler.handle_missing_values(method='ffill')  # Handle missing values using forward fill
    data_handler.performance_analysis()  # Perform and visualize the performance analysis

