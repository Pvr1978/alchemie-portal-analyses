#!/usr/bin/env python3
"""
Macro‑rapport generator voor Alchemie Portal.
Haalt marktdata op van CoinGecko en bouwt een Markdown‑rapport.
"""

import requests
import os
from datetime import datetime

COINGECKO_GLOBAL_URL = "https://api.coingecko.com/api/v3/global"

def fetch_macro_data():
    """Haal globale crypto‑marktdata op."""
    try:
        resp = requests.get(COINGECKO_GLOBAL_URL, timeout=15)
        resp.raise_for_status()
        data = resp.json()["data"]
        return {
            "total_mcap_usd": data["total_market_cap"]["usd"],
            "total_volume_usd": data["total_volume"]["usd"],
            "mcap_change_24h": data["market_cap_change_percentage_24h_usd"],
            "volume_change_24h": data["volume_change_percentage_24h_usd"],
            "market_percentage": data["market_cap_percentage"],
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    except Exception as e:
        print(f"Fout bij ophalen data: {e}")
        return None

def generate_markdown(data):
    if not data:
        return f"# Macro Report | {datetime.now().strftime('%Y-%m-%d')}\n\nGeen data beschikbaar (API-fout)."

    total_mcap = data["total_mcap_usd"] / 1_000_000_000_000  # triljoenen
    total_vol = data["total_volume_usd"] / 1_000_000_000     # miljarden
    mcap_change = data["mcap_change_24h"]
    vol_change = data["volume_change_24h"]

    # Top 5 marktaandelen
    top_coins = list(data["market_percentage"].items())[:5]
    mcap_table = "| Coin | Market Share (%) |\n|------|------------------|\n"
    for coin, pct in top_coins:
        mcap_table += f"| {coin.upper()} | {pct:.2f}% |\n"

    md = f"""# Macro Report | {data['date']}
*Global crypto market snapshot*

## Total Market Cap
| Metric | Value |
|--------|-------|
| Total Market Cap | **${total_mcap:.2f} T** |
| 24h Change | {mcap_change:+.2f}% |

## Trading Volume
| Metric | Value |
|--------|-------|
| 24h Volume | ${total_vol:.1f} B |
| 24h Volume Change | {vol_change:+.2f}% |

## Market Cap Distribution (Top 5)
{mcap_table}

## Interpretation
- A positive market cap change indicates overall growth.
- Volume increase often signals heightened activity.
- Bitcoin dominance {data['market_percentage'].get('btc', 0):.1f}% – a key macro indicator.

## Sources
- [CoinGecko](https://www.coingecko.com/)
"""
    return md

def main():
    data = fetch_macro_data()
    md_content = generate_markdown(data)
    os.makedirs("macro", exist_ok=True)
    filename = f"macro/macro_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Rapport opgeslagen als {filename}")

if __name__ == "__main__":
    main()
