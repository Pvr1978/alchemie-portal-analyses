import requests
from datetime import datetime
import time
import sys

print("=" * 50)
print("ALCHEMIE PORTAL DAILY REPORT")
print(datetime.now().strftime('%Y-%m-%d %H:%M UTC'))
print("=" * 50)

# Helper voor requests met retry
def fetch_with_retry(url, max_retries=3, backoff=2):
    headers = {"User-Agent": "AlchemiePortal-DailyReport/1.0"}
    for attempt in range(max_retries):
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt+1}/{max_retries} failed for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(backoff * (2 ** attempt))  # exponential backoff
    print(f"Failed to fetch {url} after {max_retries} attempts.")
    return None

# BTC prijs
btc_data = fetch_with_retry("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
if btc_data and "bitcoin" in btc_data and "usd" in btc_data["bitcoin"]:
    btc = btc_data["bitcoin"]["usd"]
    print(f"\nBTC: ${btc:,.0f}")
else:
    btc = None
    print("\nBTC: Error - unable to fetch price")

# Fear & Greed
fng_data = fetch_with_retry("https://api.alternative.me/fng/?limit=1")
if fng_data and "data" in fng_data and len(fng_data["data"]) > 0:
    fg = fng_data["data"][0]["value"]
    fg_class = fng_data["data"][0]["value_classification"]
    print(f"Fear & Greed: {fg} ({fg_class})")
else:
    fg = None
    fg_class = None
    print("Fear & Greed: Error - unable to fetch index")

print("\nKEY LEVELS")
print("  BTC support: $70,000 / $68,400")
print("  BTC resistance: $72,800 / $75,000")

print("\nBOTTOM LINE")
print("  BTC holding $70K support. Watch for breakout or breakdown.")

# Write to file
report_content = f"ALCHEMIE PORTAL REPORT\n{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
if btc is not None:
    report_content += f"BTC: ${btc:,.0f}\n"
if fg is not None:
    report_content += f"Fear & Greed: {fg} ({fg_class})\n"

with open("daily_report.txt", "w") as f:
    f.write(report_content)

print("\nReport written to daily_report.txt")
print("Script completed.")
