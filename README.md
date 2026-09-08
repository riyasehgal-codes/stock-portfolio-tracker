# Aurelia — Stock Portfolio Tracker

Flask app for tracking stock holdings, live P&L, allocation, and a simple 7-day linear forecast.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Deploy on Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/riyasehgal-codes/stock-portfolio-tracker)

1. Open the button above (or create a **Web Service** from this GitHub repo).
2. Render will pick up `render.yaml` / `Procfile`.
3. Set `SECRET_KEY` if it is not generated automatically.

The app binds to `0.0.0.0` and uses the `PORT` environment variable, which Render provides.

## Notes

- Prices come from Yahoo Finance via `yfinance`.
- The 7-day forecast is a linear trend on recent closes, not investment advice.
- SQLite storage is local to the instance unless you attach a persistent disk.
