from data_fetch import download_historical_data
from performance import plot_closing_prices

data = download_historical_data('RELIANCE.NS', '2024-06-18', '2024-06-19','1m')
plot_closing_prices(data, title='Reliance closing prices')
