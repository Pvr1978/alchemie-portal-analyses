import requests
from datetime import datetime

print(f"Macro Report | {datetime.now()}")
print("=" * 30)

try:
    url = "https://api.coingecko.com/api/v3/global"
    r = requests.get(url, timeout=10)
    total_mcap = r.json()["data"]["total_market_cap"]["usd"]
    print(f"Total market cap: ${total_mcap:,.0f}")
except Exception as e:
    print(f"Error: {e}")
