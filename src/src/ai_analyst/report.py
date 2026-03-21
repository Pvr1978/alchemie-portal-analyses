```python
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.error_handler import retry, safe_request
from utils.fallback_data import get_fallback_btc_price, get_fallback_btc_dominance, get_fallback_fear_greed

COINGECKO_URL = "https://api.coingecko.com/api/v3"

@retry(max_attempts=3, delay=2, backoff=2)
def get_btc_price():
    url = f"{COINGECKO_URL}/simple/price?ids=bitcoin&vs_currencies=usd"
    data = safe_request(url)
    if data and "bitcoin" in data and "usd" in data["bitcoin"]:
        return data["bitcoin"]["usd"]
    return get_fallback_btc_price()

@retry(max_attempts=3, delay=2, backoff=2)
def get_btc_dominance():
    url = f"{COINGECKO_URL}/global"
    data = safe_request(url)
    if data and "data" in data and "market_cap_percentage" in data["data"]:
        return data["data"]["market_cap_percentage"]["btc"]
    return get_fallback_btc_dominance()

@retry(max_attempts=3, delay=2, backoff=2)
def get_fear_greed():
    url = "https://api.alternative.me/fng/?limit=1"
    data = safe_request(url)
    if data and "data" in data and len(data["data"]) > 0:
        return {
            "value": data["data"][0]["value"],
            "classification": data["data"][0]["value_classification"]
        }
    return get_fallback_fear_greed()

def generate_report():
    print(f"[INFO] Starting report at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    btc_price = get_btc_price()
    btc_dom = get_btc_dominance()
    fg = get_fear_greed()
    
    report = f"""
========================================
ALCHEMIE PORTAL – DAILY CRYPTO REPORT
{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
========================================

MARKET OVERVIEW
- BTC: ${btc_price:,.0f}
- BTC dominance: {btc_dom:.1f}%
- Fear & Greed: {fg['value']} ({fg['classification']})

KEY LEVELS
- BTC support: $70,000 / $68,400
- BTC resistance: $72,800 / $75,000
- ETH support: $2,150
- ETH resistance: $2,200

MACRO
- UK 10y yield: 5.0%
- Oil: $95–100
- Fed cuts 2026: 0% priced

========================================
BOTTOM LINE
BTC holding $70K support. If it breaks → $66K–68K.
If it holds → $75K next.
========================================
"""
    return report

if __name__ == "__main__":
    try:
        report = generate_report()
        print(report)
        with open("daily_report.txt", "w") as f:
            f.write(report)
        print("[SUCCESS] Report saved")
    except Exception as e:
        print(f"[CRITICAL] Failed: {e}")
        fallback = f"Fallback report {datetime.now()}\nData unavailable.\n"
        with open("daily_report.txt", "w") as f:
            f.write(fallback)
```
