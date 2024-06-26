import yfinance as yf

def download_historical_data(symbol, start_date, end_date, timeframe):
    stock_data = yf.download(symbol, start=start_date, end=end_date, interval=timeframe)
    return stock_data

 

