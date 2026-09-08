import os
import sqlite3

import pandas as pd

DB_PATH = os.environ.get("PORTFOLIO_DB", "portfolio.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            qty REAL NOT NULL,
            buy_price REAL NOT NULL,
            buy_date TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_holding(ticker, qty, buy_price, buy_date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO holdings (ticker, qty, buy_price, buy_date) VALUES (?, ?, ?, ?)",
        (ticker.strip().upper(), qty, buy_price, buy_date),
    )
    conn.commit()
    conn.close()


def get_holdings():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM holdings ORDER BY id DESC", conn)
    conn.close()
    return df


def delete_holding(holding_id):
    conn = get_connection()
    conn.execute("DELETE FROM holdings WHERE id=?", (holding_id,))
    conn.commit()
    conn.close()
