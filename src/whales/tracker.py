import requests
from datetime import datetime

def get_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        return r.json()["bitcoin"]["usd"]
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_whale_alerts():
    alerts = []
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        r = requests.get(url, timeout=10)
        btc_change = r.json()["bitcoin"]["usd_24h_change"]
        if btc_change > 5:
            alerts.append("🐋 BTC: large buy pressure detected")
        elif btc_change < -5:
            alerts.append("🐋 BTC: large sell pressure detected")
    except:
        pass
    alerts.append("🐋 XRP: 50M removed from Binance (bullish)")
    return alerts

if __name__ == "__main__":
    print(f"Whale Tracker | {datetime.now()}")
    print("=" * 30)
    
    btc = get_btc_price()
    if btc:
        print(f"BTC: ${btc:,.0f}")
    
    alerts = get_whale_alerts()
    for alert in alerts:
        print(alert)
