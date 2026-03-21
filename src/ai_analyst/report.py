import requests
from datetime import datetime

print("=" * 50)
print("ALCHEMIE PORTAL DAILY REPORT")
print(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
print("=" * 50)

try:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    r = requests.get(url, timeout=10)
    btc = r.json()["bitcoin"]["usd"]
    print(f"\nBTC: ${btc:,.0f}")
except Exception as e:
    print(f"\nBTC: Error - {e}")

try:
    url = "https://api.alternative.me/fng/?limit=1"
    r = requests.get(url, timeout=10)
    fg = r.json()["data"][0]["value"]
    fg_class = r.json()["data"][0]["value_classification"]
    print(f"Fear & Greed: {fg} ({fg_class})")
except Exception as e:
    print(f"Fear & Greed: Error - {e}")

print("\nKEY LEVELS")
print("  BTC support: $70,000 / $68,400")
print("  BTC resistance: $72,800 / $75,000")

print("\nBOTTOM LINE")
print("  BTC holding $70K support. Watch for breakout or breakdown.")

with open("daily_report.txt", "w") as f:
    f.write(f"ALCHEMIE PORTAL REPORT\n")
    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n")
    if 'btc' in locals():
        f.write(f"BTC: ${btc:,.0f}\n")
    if 'fg' in locals():
        f.write(f"Fear & Greed: {fg} ({fg_class})\n")
