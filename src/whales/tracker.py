import requests
from datetime import datetime
import sys  # voor sys.exit(1) bij fatale errors

def get_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        r.raise_for_status()          # gooit exception bij 4xx/5xx
        data = r.json()
        return data["bitcoin"]["usd"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching BTC price: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing BTC price response: {e}")
        return None

def get_whale_alerts():
    alerts = []
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        btc_change = data.get("bitcoin", {}).get("usd_24h_change")
        
        if btc_change is not None:
            if btc_change > 5:
                alerts.append(f"🐋 BTC: large buy pressure detected (+{btc_change:.2f}%)")
            elif btc_change < -5:
                alerts.append(f"🐋 BTC: large sell pressure detected ({btc_change:.2f}%)")
        else:
            print("Warning: usd_24h_change missing in response")
    except Exception as e:
        print(f"Error fetching BTC change: {e}")
    
    # Voor nu dummy – later echte whale data toevoegen
    alerts.append("🐋 XRP: 50M removed from Binance (bullish) – [placeholder]")
    
    return alerts

if __name__ == "__main__":
    print(f"Whale Tracker | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    
    btc = get_btc_price()
    if btc:
        print(f"BTC Price: ${btc:,.0f}")
    else:
        print("BTC Price: unavailable")
    
    alerts = get_whale_alerts()
    if alerts:
        print("\nAlerts:")
        for alert in alerts:
            print(alert)
    else:
        print("No alerts at this time.")
    
    # Optioneel: force exit 1 als kritieke data mist (voor Actions monitoring)
    # if not btc or not alerts:
    #     sys.exit(1)
