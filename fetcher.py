import time

import pandas as pd
import yfinance as yf

_PRICE_CACHE = {}
_CACHE_TTL = 300


def get_current_price(ticker):
    ticker = ticker.strip().upper()
    cached = _PRICE_CACHE.get(ticker)
    if cached and time.time() - cached[1] < _CACHE_TTL:
        return cached[0]

    stock = yf.Ticker(ticker)
    price = None

    try:
        info = stock.fast_info
        price = info.get("last_price") or info.get("lastPrice") or info.get("regularMarketPrice")
    except Exception:
        price = None

    if price is None:
        hist = stock.history(period="5d")
        if hist is None or hist.empty:
            raise ValueError(f"Could not fetch a live price for {ticker}.")
        price = hist["Close"].iloc[-1]

    price = round(float(price), 2)
    _PRICE_CACHE[ticker] = (price, time.time())
    return price


def get_60day_history(ticker):
    ticker = ticker.strip().upper()
    stock = yf.Ticker(ticker)
    df = stock.history(period="60d")
    if df is None or df.empty:
        return pd.Series(dtype=float)
    return df["Close"].dropna()


def ticker_exists(ticker):
    try:
        get_current_price(ticker)
        return True
    except Exception:
        return False
