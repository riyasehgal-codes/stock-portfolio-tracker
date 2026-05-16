import numpy as np
from sklearn.linear_model import LinearRegression
from fetcher import get_60day_history

def predict_next_7(ticker):
    prices = get_60day_history(ticker)
    
    X = np.arange(len(prices)).reshape(-1, 1)
    y = prices.values

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.arange(len(prices), len(prices) + 7).reshape(-1, 1)
    predictions = model.predict(future_X)

    return {
        "historical": list(round(float(p), 2) for p in y),
        "predicted": list(round(float(p), 2) for p in predictions),
        "dates_count": len(prices)
    }
    
print(predict_next_7("AAPL"))