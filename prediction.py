import numpy as np
from sklearn.linear_model import LinearRegression

from fetcher import get_60day_history


def predict_next_7(ticker):
    prices = get_60day_history(ticker)

    if prices is None or len(prices) < 5:
        raise ValueError(f"Not enough price history to forecast {ticker}.")

    X = np.arange(len(prices)).reshape(-1, 1)
    y = prices.values.astype(float)

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.arange(len(prices), len(prices) + 7).reshape(-1, 1)
    predictions = model.predict(future_X)
    last = float(y[-1])
    forecast_end = float(predictions[-1])
    change_pct = ((forecast_end - last) / last) * 100 if last else 0.0

    return {
        "historical": [round(float(p), 2) for p in y],
        "predicted": [round(float(p), 2) for p in predictions],
        "dates_count": int(len(prices)),
        "change_pct": round(change_pct, 2),
    }
