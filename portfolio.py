import pandas as pd 
from database import get_holdings 
from fetcher import get_current_price 

def get_portfolio_summary() : 
    holdings = get_holdings() 
    
    if holdings.empty : 
        return pd.DataFrame() 
    results = [] 
    
    for _, row in holdings.iterrows() : 
        current_price = get_current_price(row["ticker"])
        invested = row["buy_price"] * row["qty"]
        current_val = current_price * row['qty']
        pnl = current_val - invested
        return_pct = ( pnl / invested ) * 100 
        
        results.append ( { 
                "ID" : row['id'],
                "Ticker" : row['ticeker'], 
                "Qty" : row['qty'],
                "Buy Price" : row['buy_price'],
                "Current Price" : current_price, 
                "Invested" : round(invested, 2) ,
                "current Value" : round( current_val , 2 ), 
                "P&L" : round(pnl,2),
                "Return %" : round( return_pct, 2 )
                
                })
    return pd.DataFrame(results)

print(get_portfolio_summary)