import matplotlib.pyplot as plt

def plot_closing_prices(data, title='Closing Prices'):
    
    plt.figure(figsize=(10,5))
    plt.plot(data.index, data['Close'], label='Close Price')
    plt.scatter(data.index, data['Close'], color='red', s=10,)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Closing Price (INR)')
    plt.legend()
    plt.grid(True)
    plt.show()



