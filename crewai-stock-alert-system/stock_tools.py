import yfinance as yf

def get_latest_stock_price(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="2d")
    if len(hist) < 2:
        return None, None
    prev_close = hist['Close'].iloc[-2]
    latest = hist['Close'].iloc[-1]
    return prev_close, latest

def calculate_percent_change(prev, current):
    if prev == 0:
        return 0
    return ((current - prev) / prev) * 100
