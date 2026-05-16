import sqlite3 
import pandas as pd 

def init_db() : 
    conn = sqlite3.connect("portfolio.db")
    conn.execute( """
        CREATE TABLE IF NOT EXISTS holdings (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ticker TEXT NOT NULL, 
            qty REAL NOT NULL, 
            buy_price REAL NOT NULL, 
            buy_date TEXT NOT NULL
        )
            
    """)
    conn.commit() 
    conn.close() 
    
def add_holding( ticker, qty, buy_price, buy_date) : 
    conn = sqlite3.connect("portfolio.db")
    conn.execute( 
        " INSERT INTO holdings( ticker, qty, buy_price, buy_date) VALUES (?,?,?,?)",
        (ticker, qty, buy_price, buy_date)
    )
    conn.commit()
    conn.close() 
    
def get_holdings() : 
    conn = sqlite3.connect("portfolio.db")
    df = pd.read_sql("SELECT * FROM holdings", conn)
    conn.close() 
    return df 

def delete_holding(holding_id) : 
    conn = sqlite3.connect("portfolio.db") 
    conn.execute("DELETE FROM holdings WHERE id=?", (holding_id,))
    conn.commit() 
    conn.close() 
    
    
init_db() 
add_holding(" AAPL", 10, 150, "2024-01-01")
print(get_holdings())
# delete_holding(1)
# print(get_holdings())