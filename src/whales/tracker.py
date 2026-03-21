```python
import sys
import os
from datetime import datetime

# Voeg utils toe aan path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_handler import retry, safe_request
from utils.fallback_data import get_fallback_btc_price

COINGECKO_URL = "https://api.coingecko.com/api/v3"

@retry(max_attempts=3, delay=2, backoff=2)
def get_btc_price():
    url = f"{COINGECKO_URL}/simple/price?ids=bitcoin&vs_currencies=usd"
    data = safe_request(url)
    if data and "bitcoin" in data and "usd" in data["bitcoin"]:
        return data["bitcoin"]["usd"]
    return get_fallback_btc_price()

@retry(max_attempts=2, delay=2, backoff=2)
def get_top_gainers():
    url = f"{COINGECKO_URL}/search/trending"
    data = safe_request(url)
    gainers = []
    if data and "coins" in data:
        for item in data["coins"][:5]:
            try:
                gainers.append({
                    "symbol": item["item"]["symbol"].upper(),
                    "change": item["item"]["data"].get("price_change_percentage_24h", {}).get("usd", 0)
                })
            except:
                continue
    return gainers

if __name__ == "__main__":
    print(f"Whale Tracker | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    price = get_btc_price()
    if price:
        print(f"BTC: ${price:,.0f}")
    
    gainers = get_top_gainers()
    if gainers:
        print("\nTrending coins:")
        for g in gainers:
            print(f"  {g['symbol']}: {g['change']:.1f}%")
```
