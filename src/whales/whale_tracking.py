#!/usr/bin/env python3
"""
Whale Tracking rapport generator voor Alchemie Portal.
Haalt grote transacties op van Whale Alert (gratis publieke API).
"""

import requests
import os
from datetime import datetime

WHALE_ALERT_URL = "https://api.whale-alert.io/v1/transactions"
API_KEY = os.environ.get("WHALE_ALERT_API_KEY", "")  # optioneel, gratis key kan worden aangevraagd
MIN_VALUE = 500000   # minimale waarde in USD

def fetch_whale_transactions():
    """Haal de laatste 10 whale transacties op."""
    params = {
        "api_key": API_KEY,
        "min_value": MIN_VALUE,
        "limit": 10
    }
    try:
        resp = requests.get(WHALE_ALERT_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("transactions", [])
    except Exception as e:
        print(f"Fout bij ophalen data: {e}")
        return None

def generate_markdown(transactions):
    """Genereer Markdown rapport."""
    if not transactions:
        return f"# Whale Tracking Report | {datetime.now().strftime('%Y-%m-%d')}\n\nGeen transacties gevonden (API-fout of geen grote transfers)."

    lines = [
        f"# Whale Tracking Report | {datetime.now().strftime('%Y-%m-%d')}",
        "*Top 10 grote transacties (≥ $500k) volgens Whale Alert*",
        "",
        "| Timestamp | From | To | Amount | Symbol | USD Value |",
        "|-----------|------|----|--------|--------|-----------|"
    ]
    for tx in transactions:
        timestamp = datetime.fromtimestamp(tx.get("timestamp", 0)).strftime("%Y-%m-%d %H:%M")
        from_addr = tx.get("from", {}).get("address", "Unknown")[:10] + "..."
        to_addr = tx.get("to", {}).get("address", "Unknown")[:10] + "..."
        amount = f"{tx.get('amount', 0):,.0f}"
        symbol = tx.get("symbol", "?")
        usd = f"${tx.get('amount_usd', 0):,.0f}"
        lines.append(f"| {timestamp} | {from_addr} | {to_addr} | {amount} | {symbol} | {usd} |")

    lines.extend([
        "",
        "## Interpretation",
        "- Large transfers often indicate whale accumulation or exchange movements.",
        "- Monitor for sudden spikes in activity.",
        "",
        "## Sources",
        "- [Whale Alert](https://whale-alert.io/)"
    ])
    return "\n".join(lines)

def main():
    transactions = fetch_whale_transactions()
    md_content = generate_markdown(transactions)
    os.makedirs("whale_tracking", exist_ok=True)
    filename = f"whale_tracking/whale_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Rapport opgeslagen als {filename}")

if __name__ == "__main__":
    main()
