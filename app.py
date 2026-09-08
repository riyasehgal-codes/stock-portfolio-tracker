import os

from flask import Flask, flash, redirect, render_template, request, url_for

from database import add_holding, delete_holding, get_holdings, init_db
from fetcher import ticker_exists
from portfolio import get_portfolio_summary
from prediction import predict_next_7

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "portfolio-tracker-dev-key")
init_db()


@app.route("/")
def index():
    holdings = get_holdings().to_dict("records")
    return render_template("index.html", holdings=holdings)


@app.route("/add", methods=["POST"])
def add():
    ticker = request.form.get("ticker", "").upper().strip()
    qty_raw = request.form.get("qty", "").strip()
    buy_price_raw = request.form.get("buy_price", "").strip()
    buy_date = request.form.get("buy_date", "").strip()

    try:
        qty = float(qty_raw)
        buy_price = float(buy_price_raw)
    except ValueError:
        flash("Quantity and buy price must be numbers.", "error")
        return redirect(url_for("index"))

    if not ticker or qty <= 0 or buy_price <= 0 or not buy_date:
        flash("Please fill in a valid ticker, quantity, price, and date.", "error")
        return redirect(url_for("index"))

    if not ticker_exists(ticker):
        flash(f"Could not find live market data for {ticker}. Check the symbol and try again.", "error")
        return redirect(url_for("index"))

    add_holding(ticker, qty, buy_price, buy_date)
    flash(f"{ticker} added to your portfolio.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:holding_id>", methods=["POST"])
def delete(holding_id):
    delete_holding(holding_id)
    flash("Holding removed.", "success")
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    df = get_portfolio_summary()
    if df.empty:
        flash("Add at least one stock before opening the dashboard.", "error")
        return redirect(url_for("index"))

    fetch_errors = df.attrs.get("errors", [])
    tickers = df["Ticker"].tolist()
    selected = request.args.get("ticker", tickers[0]).strip().upper()
    if selected not in tickers:
        selected = tickers[0]

    pred_data = None
    pred_error = None
    try:
        pred_data = predict_next_7(selected)
    except Exception as exc:
        pred_error = str(exc)

    total_invested = round(float(df["Invested"].sum()), 2)
    total_value = round(float(df["Current Value"].sum()), 2)
    total_pnl = round(float(df["P&L"].sum()), 2)
    total_return = round((total_pnl / total_invested) * 100, 2) if total_invested else 0.0

    if fetch_errors:
        flash(
            "Live prices could not be fetched for: " + ", ".join(sorted(set(fetch_errors))),
            "error",
        )

    return render_template(
        "dashboard.html",
        table=df.to_dict("records"),
        pie_labels=df["Ticker"].tolist(),
        pie_values=df["Current Value"].tolist(),
        bar_labels=df["Ticker"].tolist(),
        bar_values=df["Return %"].tolist(),
        total_invested=total_invested,
        total_value=total_value,
        total_pnl=total_pnl,
        total_return=total_return,
        pred_ticker=selected,
        pred_data=pred_data,
        pred_error=pred_error,
        tickers=tickers,
    )


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
