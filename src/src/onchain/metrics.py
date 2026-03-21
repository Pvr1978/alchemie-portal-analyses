```python
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_handler import retry, safe_request
from utils.fallback_data import get_fallback_btc_dominance

COINGECKO_URL = "https://api.coingecko.com/api/v3"

@retry(max_attempts=3, delay=2, backoff=2)
def get_btc_dominance():
    url = f"{COINGECKO_URL}/global"
    data = safe_request(url)
    if data and "data" in data and "market_cap_percentage" in data["data"]:
        return data["data"]["market_cap_percentage"]["btc"]
    return get_fallback_btc_dominance()

if __name__ == "__main__":
    print(f"On-Chain Metrics | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    dom = get_btc_dominance()
    if dom:
        print(f"BTC dominance: {dom:.1f}%")
```
