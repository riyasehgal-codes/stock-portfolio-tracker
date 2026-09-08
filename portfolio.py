import pandas as pd

from database import get_holdings
from fetcher import get_current_price


def get_portfolio_summary():
    holdings = get_holdings()

    if holdings.empty:
        return pd.DataFrame()

    results = []
    errors = []

    for _, row in holdings.iterrows():
        ticker = str(row["ticker"]).strip().upper()
        qty = float(row["qty"])
        buy_price = float(row["buy_price"])
        invested = buy_price * qty

        try:
            current_price = get_current_price(ticker)
        except Exception:
            errors.append(ticker)
            current_price = None
            current_val = 0.0
            pnl = -invested
            return_pct = -100.0 if invested else 0.0
        else:
            current_val = current_price * qty
            pnl = current_val - invested
            return_pct = (pnl / invested) * 100 if invested else 0.0

        results.append(
            {
                "ID": row["id"],
                "Ticker": ticker,
                "Qty": qty,
                "Buy Price": round(buy_price, 2),
                "Current Price": round(current_price, 2) if current_price is not None else None,
                "Invested": round(invested, 2),
                "Current Value": round(current_val, 2),
                "P&L": round(pnl, 2),
                "Return %": round(return_pct, 2),
                "Buy Date": row["buy_date"],
            }
        )

    df = pd.DataFrame(results)
    df.attrs["errors"] = errors
    return df
