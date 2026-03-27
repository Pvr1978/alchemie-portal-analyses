#!/usr/bin/env python3
"""
Liquidations rapport generator.
Haalt data op van CoinGlass (gratis publieke endpoint) en slaat op als Markdown.
"""

import requests
import json
import os
from datetime import datetime

# Configuratie
COINGLASS_API_URL = "https://api.coinglass.com/api/pro/v1/futures/liquidation/chart"
# Optioneel: als je een gratis API key hebt, zet hem dan als omgevingsvariabele
API_KEY = os.environ.get("COINGLASS_API_KEY", "")

def fetch_liquidations():
    """Haal liquidatie-data op van CoinGlass (24h totaal)."""
    headers = {
        "accept": "application/json",
        "cg-api-key": API_KEY
    }
    params = {
        "symbol": "BTC",
        "time_type": "1d"
    }
    try:
        resp = requests.get(COINGLASS_API_URL, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # De structuur kan variëren; dit is een voorbeeld. Pas aan op basis van echte response.
        if "data" in data:
            # Vaak: data bevat lijst per exchange of totaal
            total_longs = data["data"].get("longSum", 0)
            total_shorts = data["data"].get("shortSum", 0)
            total = total_longs + total_shorts
        else:
            # Alternatieve parsing
            total = 0
            total_longs = 0
            total_shorts = 0
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
    """Genereer Markdown inhoud."""
    if not data:
        return f"# Liquidations Report - {datetime.now().strftime('%Y-%m-%d')}\n\nGeen data beschikbaar (API-fout)."
    total_m = data["total"] / 1_000_000
    longs_m = data["longs"] / 1_000_000
    shorts_m = data["shorts"] / 1_000_000
    long_pct = (data["longs"] / data["total"] * 100) if data["total"] else 0
    return f"""# Liquidations Report | {data['date']}
*Daily market liquidation snapshot*

## Total Liquidations (24h)
| Metric | Value |
|--------|-------|
| Total | **${total_m:.1f}M** |
| Longs | ${longs_m:.1f}M ({long_pct:.0f}%) |
| Shorts | ${shorts_m:.1f}M |

## Exchange Distribution
*(Data aggregated from CoinGlass)*

## Interpretation
- A high total indicates market-wide deleveraging.
- Long dominance suggests forced selling after a price drop.

## Sources
- CoinGlass (public API)

*Report generated automatically by GitHub Actions.*
"""

def main():
    data = fetch_liquidations()
    md = generate_markdown(data)
    os.makedirs("liquidations", exist_ok=True)
    filename = f"liquidations/liquidations_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, "w") as f:
        f.write(md)
    print(f"Rapport opgeslagen als {filename}")

if __name__ == "__main__":
    main()
