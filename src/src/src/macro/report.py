```python
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_handler import safe_request

COINGECKO_URL = "https://api.coingecko.com/api/v3"

def get_market_data():
    url = f"{COINGECKO_URL}/global"
    data = safe_request(url)
    if data and "data" in data:
        return data["data"]
    return None

if __name__ == "__main__":
    print(f"Macro Report | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    data = get_market_data()
    if data:
        total_mcap = data.get("total_market_cap", {}).get("usd", 0)
        btc_dom = data.get("market_cap_percentage", {}).get("btc", 0)
        print(f"Total market cap: ${total_mcap:,.0f}")
        print(f"BTC dominance: {btc_dom:.1f}%")
    else:
        print("Macro data not available (using fallback)")
        print("Total market cap: $2.8T (estimate)")
        print("BTC dominance: 58.5% (estimate)")
```
