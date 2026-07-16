from flask import Flask, render_template, request, redirect
from database import init_db, add_holding, delete_holding
from portfolio import get_portfolio_summary
from prediction import predict_next_7
from chart import make_bar_chart, make_pie_chart, make_prediction_chart

app = Flask(__name__)
init_db() 

@app.route("/")
def index() :
    from database import get_holdings
    holdings = get_holdings().to_dict("records")
    return render_template("index.html", holdings= holdings)

@app.route("/add", methods=['POST'])
def add() : 
    ticker = request.form["ticker"].upper().strip()
    qty = float(request.form["qty"])
    buy_price = float(request.form["buy_price"])
    buy_date = request.form["buy_date"]
    add_holding(ticker, qty, buy_price, buy_date)
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    delete_holding(id)
    return redirect("/")

@app.route("/dashboard")
def dashboard():
    df = get_portfolio_summary()
    if df.empty:
        return redirect("/")

    make_pie_chart(df)
    make_bar_chart(df)

    # prediction for first stock only 
    first_ticker = df["Ticker"].iloc[0]
    pred_data = predict_next_7(first_ticker)
    make_prediction_chart(first_ticker, pred_data)

    total_invested = round(df["Invested"].sum(), 2)
    total_value = round(df["Current Value"].sum(), 2)
    total_pnl = round(df["P&L"].sum(), 2)
    total_return = round((total_pnl / total_invested) * 100, 2)

    return render_template("dashboard.html",
        table=df.to_dict("records"),
        total_invested=total_invested,
        total_value=total_value,
        total_pnl=total_pnl,
        total_return=total_return,
        pred_ticker=first_ticker
    )

if __name__ == "__main__":
    app.run(debug=True) 
