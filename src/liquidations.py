#!/usr/bin/env python3
"""
Liquidations rapport generator voor Alchemie Portal.
Haalt data op van CoinGlass (gratis publieke API) en bouwt een Markdown-rapport.
Gebaseerd op de stijl van fomc_liquidations_march20_2026.md.
"""

import os
import json
import requests
from datetime import datetime

# -------------------------------
# Configuratie (pas aan indien nodig)
# -------------------------------
COINGLASS_API_URL = "https://api.coinglass.com/api/pro/v1/futures/liquidation/chart"
API_KEY = os.environ.get("COINGLASS_API_KEY", "")  # optioneel, gratis aan te vragen
SYMBOL = "BTC"          # kan ook "ALL" of "ETH" – pas aan naar wens

def fetch_liquidations():
    """Haal liquidatie-data op van CoinGlass (24h totaal)."""
    headers = {
        "accept": "application/json",
        "cg-api-key": API_KEY
    }
    params = {
        "symbol": SYMBOL,
        "time_type": "1d"
    }
    try:
        resp = requests.get(COINGLASS_API_URL, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # De API kan verschillende velden hebben. Dit is een veilige parsing.
        if "data" in data:
            # Meestal: data["longSum"] en data["shortSum"] zijn de totalen over alle exchanges.
            total_longs = float(data["data"].get("longSum", 0))
            total_shorts = float(data["data"].get("shortSum", 0))
            # Optioneel: exchange breakdown staat soms in data["exchangeList"]
            exchange_data = data["data"].get("exchangeList", [])
        else:
            # Alternatieve structuur (valt terug op 0)
            total_longs = 0.0
            total_shorts = 0.0
            exchange_data = []
        total = total_longs + total_shorts
        return {
            "total": total,
            "longs": total_longs,
            "shorts": total_shorts,
            "exchanges": exchange_data,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    except Exception as e:
        print(f"Fout bij ophalen data: {e}")
        return None

def generate_markdown(data):
    """Genereer Markdown in de stijl van het eerdere rapport."""
    if not data:
        return f"# Liquidations Report | {datetime.now().strftime('%Y-%m-%d')}\n\nGeen data beschikbaar (API-fout)."

    total_m = data["total"] / 1_000_000
    longs_m = data["longs"] / 1_000_000
    shorts_m = data["shorts"] / 1_000_000
    long_pct = (data["longs"] / data["total"] * 100) if data["total"] else 0

    # Exchange breakdown (indien aanwezig)
    exchange_table = ""
    if data["exchanges"]:
        exchange_table = "\n## By Exchange\n| Exchange | Liquidations | Dominance |\n|----------|--------------|-----------|\n"
        for ex in data["exchanges"]:
            ex_name = ex.get("exchangeName", "Unknown")
            ex_total = ex.get("total", 0) / 1_000_000
            ex_dom = (ex_total / total_m * 100) if total_m else 0
            exchange_table += f"| {ex_name} | ${ex_total:.1f}M | {ex_dom:.0f}% |\n"

    # Asset breakdown (schatting op basis van symbol)
    asset_table = f"""## By Asset (Estimated)
| Asset | Liquidations |
|-------|--------------|
| Bitcoin | ~${total_m * 0.7:.1f}M |
| Ethereum | ~${total_m * 0.2:.1f}M |
| Altcoins | ~${total_m * 0.1:.1f}M |"""

    # Interpretatie (kan dynamisch gemaakt worden op basis van longs/shorts)
    interpretation = f"""## Interpretation
- **{long_pct:.0f}% longs liquidated** = over‑levered speculators washed out.
- High total indicates market‑wide deleveraging.
- Weak hands removed, spot buyers absorbing supply."""

    # Historische context (statisch voorbeeld, kan later uitgebreid)
    history = """## Historical Context
- FOMC meetings in 2025: BTC fell after 7 of 8 meetings.
- Average decline: ~0.7% in 48 hours post‑announcement.
- Current move fits broader pattern."""

    # Bronvermelding
    sources = "## Sources\n- CoinGlass"

    md = f"""# Liquidations Report | {data['date']}
*Daily market liquidation snapshot*

## Total Liquidations (24h)
| Metric | Value |
|--------|-------|
| Total | **${total_m:.1f}M** |
| Longs | ${longs_m:.1f}M ({long_pct:.0f}%) |
| Shorts | ${shorts_m:.1f}M |
{exchange_table}
{asset_table}
{interpretation}
{history}
{sources}

*Report generated automatically by GitHub Actions.*
"""
    return md

def main():
    data = fetch_liquidations()
    md_content = generate_markdown(data)
    os.makedirs("liquidations", exist_ok=True)
    filename = f"liquidations/liquidations_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Rapport opgeslagen als {filename}")

if __name__ == "__main__":
    main()
