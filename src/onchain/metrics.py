import requests
from datetime import datetime

print(f"On-Chain Metrics | {datetime.now()}")
print("=" * 30)

try:
    url = "https://api.coingecko.com/api/v3/global"
    r = requests.get(url, timeout=10)
    dom = r.json()["data"]["market_cap_percentage"]["btc"]
    print(f"BTC dominance: {dom:.1f}%")
except Exception as e:
    print(f"Error: {e}")
