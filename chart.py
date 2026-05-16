import matplotlib.pyplot as plt 
import seaborn as sns 
import os 

os.makedirs("static/plot", exist_ok=True)

def make_pie_chart(df) : 
    plt.figure(figsize=(6,6))
    plt.pie(df["current Value"], labels= df['Ticker'], autopct="%1.1f%%")
    plt.title("Portfolio Allocation")
    plt.savefig("static/plots/pie.png")
    
def make_bar_chart(df) : 
    plt.figure(figsize=(6,6)) 
    colors = ["green" if x > 0 else "red" for x in df["Return %"]]
    sns.barplot(x="Ticker", y="Return %", data=df, palette=colors)
    plt.title("Return % per Stock")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.savefig("static/plots/bar.png")
    plt.close() 
    
def make_prediction_chart(ticker, data):
    plt.figure(figsize=(10, 5))
    
    historical = data["historical"]
    predicted = data["predicted"]
    
    plt.plot(range(len(historical)), historical, 
        label="Historical", color="blue")
    plt.plot(range(len(historical), len(historical) + 7), predicted,
        label="7-day Forecast", color="orange", linestyle="--", marker="o")
    
    plt.axvline(x=len(historical)-1, color="gray", linestyle=":", label="Today")
    plt.title(f"{ticker} — Price Forecast")
    plt.xlabel("Days")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.savefig(f"static/plots/pred_{ticker}.png")
    plt.close()
    
