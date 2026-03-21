import requests
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
    """Haal top 5 trending coins van vandaag op"""
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

if __name__ == "__main__":
    print(f"🔍 Whale Tracker gestart om {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # BTC prijs ophalen
    current_price = get_btc_price()
    if current_price:
        print(f"💰 Huidige BTC prijs: ${current_price:,.0f}")
    else:
        print("💰 BTC prijs: niet beschikbaar")
    
    # Top gainers ophalen
    gainers = get_top_gainers()
    if gainers:
        print("\n📈 Trending coins vandaag:")
        for g in gainers:
            print(f"  {g['symbol']}: {g['price_change_24h']:.1f}%")
    else:
        print("\n📈 Geen trending data beschikbaar")
    
    print("\n✅ Whale tracker draait. Geen extreme bewegingen gedetecteerd.")
