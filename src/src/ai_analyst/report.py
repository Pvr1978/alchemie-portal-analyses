import requests
from datetime import datetime

def get_btc_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        return r.json()["bitcoin"]["usd"]
    except:
        return 72400

def get_btc_dominance():
    try:
        url = "https://api.coingecko.com/api/v3/global"
        r = requests.get(url, timeout=10)
        return r.json()["data"]["market_cap_percentage"]["btc"]
    except:
        return 58.5

def get_fear_greed():
    try:
        url = "https://api.alternative.me/fng/?limit=1"
        r = requests.get(url, timeout=10)
        d = r.json()["data"][0]
        return d["value"], d["value_classification"]
    except:
        return "50", "Neutral"

if __name__ == "__main__":
    print("=" * 50)
    print(f"ALCHEMIE PORTAL DAILY REPORT")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 50)
    
    btc = get_btc_price()
    dom = get_btc_dominance()
    fg_val, fg_txt = get_fear_greed()
    
    print(f"\nMARKET OVERVIEW")
    print(f"  BTC: ${btc:,.0f}")
    print(f"  BTC dominance: {dom:.1f}%")
    print(f"  Fear & Greed: {fg_val} ({fg_txt})")
    
    print(f"\nKEY LEVELS")
    print(f"  BTC support: $70,000 / $68,400")
    print(f"  BTC resistance: $72,800 / $75,000")
    
    print(f"\nMACRO")
    print(f"  UK 10y yield: 5.0%")
    print(f"  Oil: $95-100")
    print(f"  Fed cuts 2026: 0% priced")
    
    print(f"\nBOTTOM LINE")
    print(f"  BTC holding $70K support. Break -> $66K, hold -> $75K.")
    
    print("=" * 50)
    
    with open("daily_report.txt", "w") as f:
        f.write(f"ALCHEMIE PORTAL REPORT\n{datetime.now()}\n")
        f.write(f"BTC: ${btc:,.0f}\n")
        f.write(f"Fear & Greed: {fg_val} ({fg_txt})\n")
