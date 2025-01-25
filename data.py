import yfinance as yf
import pandas as pd


def get_sp500_symbols():
    """Fetch S&P 500 stock symbols from Wikipedia."""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_table = tables[0]
    return sp500_table['Symbol'].tolist()


def get_stock_data(symbol):
    """Fetch current price and other data for a given stock symbol."""
    stock = yf.Ticker(symbol)
    info = stock.history(period="1d") # Get all available info
  
    # Extract relevant data
    data = {
        'Symbol': symbol,
        'Name': info.get('shortName', 'N/A'),
        'Current Price': info.get('currentPrice', 'N/A'),
        'Market Cap': info.get('marketCap', 'N/A'),
        'PE Ratio': info.get('trailingPE', 'N/A'),
        'Dividend Yield': info.get('dividendYield', 'N/A'),
        '52 Week High': info.get('fiftyTwoWeekHigh', 'N/A'),
        '52 Week Low': info.get('fiftyTwoWeekLow', 'N/A'),
    }
    return data


def get_sp500_stock_data():
    """Fetch data for all S&P 500 stocks."""
    symbols = get_sp500_symbols()
    stock_data = []

    for symbol in symbols:
        try:
            data = get_stock_data(symbol)
            stock_data.append(data)
            print(f"Fetched data for {symbol}")
        except Exception as e:
            print(f"Failed to fetch data for {symbol}: {e}")

    return stock_data
# a simple page that says hello


def stock():
    sp500_data = get_sp500_stock_data()
    # Convert to DataFrame for better visualization
    df = pd.DataFrame(sp500_data)
    return df.to_dict('records')


if __name__ == '__main__':
    stock = yf.Ticker('GOOG')
    info = stock.history(period="1d")
    print(info.to_dict('records'))
