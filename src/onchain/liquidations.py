import requests
import json
from datetime import datetime
import os

def fetch_liquidations():
    """Haal liquidatie-data op van CoinGlass public API (voorbeeld)."""
    url = "https://api.coinglass.com/api/pro/v1/futures/liquidation/chart"
    headers = {
        "accept": "application/json",
        "cg-api-key": ""  # optioneel: gratis API key aanvragen
    }
    params = {
        "symbol": "BTC",
        "time_type": "1d"
    }
    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        # Verwerk data (vereenvoudigd)
        total_longs = data.get('data', {}).get('longSum', 0)
        total_shorts = data.get('data', {}).get('shortSum', 0)
        total = total_longs + total_shorts
        return {
            "total": total,
            "longs": total_longs,
            "shorts": total_shorts,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    except Exception as e:
        print(f"Fout bij ophalen data: {e}")
        return None

def generate_markdown(data):
    """Genereer Markdown rapport."""
    if not data:
        return "# Geen liquidatie-data beschikbaar vandaag\n\nControleer de bron of API-sleutel."
    date = data['date']
    total = data['total'] / 1_000_000  # naar miljoenen
    longs = data['longs'] / 1_000_000
    shorts = data['shorts'] / 1_000_000
    long_pct = (data['longs'] / data['total'] * 100) if data['total'] else 0

    md = f"""# Liquidations Report | {date}
*Daily market liquidation snapshot*

## Total Liquidations (24h)
| Metric | Value |
|--------|-------|
| Total | **${total:.1f}M** |
| Longs | ${longs:.1f}M ({long_pct:.0f}%) |
| Shorts | ${shorts:.1f}M |

## Exchange Distribution
*(Data gebaseerd op CoinGlass globale cijfers)*

## Interpretation
- Longs dominate liquidations if price dropped.
- High total indicates leveraged washout.

## Sources
- CoinGlass
"""
    return md

def main():
    data = fetch_liquidations()
    md_content = generate_markdown(data)
    filename = f"liquidations/liquidations_{datetime.now().strftime('%Y%m%d')}.md"
    os.makedirs("liquidations", exist_ok=True)
    with open(filename, "w") as f:
        f.write(md_content)
    print(f"Rapport opgeslagen als {filename}")

if __name__ == "__main__":
    main()
