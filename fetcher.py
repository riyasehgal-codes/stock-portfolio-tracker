import yfinance as yf 

def get_current_price(ticker) : 
    stock = yf.Ticker(ticker)
    return round(stock.fast_info["last_price"], 2)

def get_history(ticker, start_date): 
    stock = yf.Ticker(ticker) 
    df = stock.history( start = start_date)
    return df['Close']

def get_60day_history(ticker) :
    stock = yf.Ticker(ticker)
    df = stock.history(period="60d")
    return df['Close']

print(get_current_price("AAPL"))