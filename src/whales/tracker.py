```python
import os
import requests
import json
from datetime import datetime

# API keys uit .env (later instellen)
GLASSNODE_API_KEY = os.getenv("GLASSNODE_API_KEY")
NANSEN_API_KEY = os.getenv("NANSEN_API_KEY")

def get_large_transfers(asset="BTC", min_usd=1000000):
    """
    Haal grote transacties op via Glassnode of Nansen.
    Dit is een voorbeeldstructuur — je vult later de echte API calls in.
    """
    print(f"🔍 Checking {asset} transfers > ${min_usd}...")
    
    # Placeholder: hier komt later echte API call
    # data = requests.get(f"https://api.glassnode.com/...")
    
    # Voor nu: dummy data
    transfers = [
        {"hash": "0x123...", "from": "unknown", "to": "Binance", "value_usd": 152_000_000, "asset": "USDT"},
        {"hash": "0x456...", "from": "HTX", "to": "unknown", "value_usd": 163_000_000, "asset": "SOL"},
    ]
    
    return transfers

def check_if_alert_needed(transfers, threshold=50000000):
    """Alleen alerts bij transacties boven threshold."""
    alerts = [t for t in transfers if t["value_usd"] > threshold]
    return alerts

def format_alert(alert):
    """Maak een leesbaar bericht voor X."""
    return f"🐋 Whale Alert: {alert['value_usd']:,} {alert['asset']} moved from {alert['from']} to {alert['to']}\nTx: {alert['hash'][:20]}..."

if __name__ == "__main__":
    transfers = get_large_transfers()
    alerts = check_if_alert_needed(transfers)
    
    if alerts:
        for alert in alerts:
            print(format_alert(alert))
        # Later: hier komt code om naar X te posten
    else:
        print("✅ No whale alerts above threshold.")
