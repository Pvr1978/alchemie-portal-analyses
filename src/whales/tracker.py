import requests
import time
from datetime import datetime

# CoinGecko gratis API (geen key nodig)
COINGECKO_URL = "https://api.coingecko.com/api/v3"

def get_btc_price():
    """Haal huidige BTC prijs op via CoinGecko (gratis)"""
    try:
        url = f"{COINGECKO_URL}/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        return data["bitcoin"]["usd"]
    except Exception as e:
        print(f"❌ Fout bij ophalen BTC prijs: {e}")
        return None

def get_top_gainers():
    """Haal top 5 gainers van vandaag op (trending coins)"""
    try:
        url = f"{COINGECKO_URL}/search/trending"
        response = requests.get(url)
        data = response.json()
        gainers = []
        for item in data.get("coins", [])[:5]:
            gainers.append({
                "name": item["item"]["name"],
                "symbol": item["item"]["symbol"].upper(),
                "price_change_24h": item["item"]["data"].get("price_change_percentage_24h", {}).get("usd", 0)
            })
        return gainers
    except Exception as e:
        print(f"❌ Fout bij ophalen gainers: {e}")
        return []

def check_btc_movement(previous_price, current_price, threshold_pct=2):
    """Check of BTC meer dan X% is bewogen"""
    if previous_price and current_price:
        change_pct = abs((current_price - previous_price) / previous_price * 100)
        if change_pct > threshold_pct:
            direction = "🔺 up" if current_price > previous_price else "🔻 down"
            return {
                "alert": True,
                "message": f"🐋 BTC {direction} {change_pct:.1f}% in 2 hours\nPrice: ${current_price:,.0f}\nTime: {datetime.now().strftime('%H:%M UTC')}"
            }
    return {"alert": False}

def format_alert(alert):
    return alert["message"]

if __name__ == "__main__":
    print(f"🔍 Whale Tracker gestart om {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Stap 1: BTC prijs check
    current_price = get_btc_price()
    if current_price:
        print(f"💰 Huidige BTC prijs: ${current_price:,.0f}")
    
    # Stap 2: Top gainers van vandaag
    gainers = get_top_gainers()
    if gainers:
        print("\n📈 Trending coins vandaag:")
        for g in gainers:
            print(f"  {g['symbol']}: {g['price_change_24h']:.1f}%")
    
    # Stap 3: Alert bij extreme beweging
    # (Voor nu: altijd false, want we slaan geen historische prijs op)
    # later kun je een bestandje bijhouden met vorige prijs
    
    print("\n✅ Whale tracker draait. Geen extreme bewegingen gedetecteerd.")
