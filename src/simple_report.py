import requests
from datetime import datetime

print("ALCHEMIE PORTAL REPORT")
print(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
print("=" * 30)

try:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    r = requests.get(url, timeout=10)
    btc = r.json()["bitcoin"]["usd"]
    print(f"BTC: ${btc:,.0f}")
except Exception as e:
    print(f"BTC: error ({e})")

try:
    url = "https://api.alternative.me/fng/?limit=1"
    r = requests.get(url, timeout=10)
    fg = r.json()["data"][0]["value"]
    print(f"Fear & Greed: {fg}")
except Exception as e:
    print(f"Fear & Greed: error ({e})")
