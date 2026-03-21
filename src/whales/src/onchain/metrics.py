```python
import requests
from datetime import datetime

COINGECKO_URL = "https://api.coingecko.com/api/v3"

def get_market_data():
    try:
        url = f"{COINGECKO_URL}/global"
        response = requests.get(url)
        data = response.json()
        return data["data"]
    except Exception as e:
        print(f"Fout: {e}")
        return None

def get_btc_dominance():
    data = get_market_data()
    if data:
        return data.get("market_cap_percentage", {}).get("btc", 0)
    return None

if __name__ == "__main__":
    print(f"On-Chain Metrics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    btc_dom = get_btc_dominance()
    if btc_dom:
        print(f"BTC dominantie: {btc_dom:.1f}%")
    
    print("On-chain metrics verzameld")
```
