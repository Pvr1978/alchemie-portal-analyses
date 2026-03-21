# Alchemie Portal Analyses

Data-gedreven crypto-analyses: whale tracking, ETF flows, orderbook liquidity, on-chain metrics & macro correlaties.

**Geen hype. Alleen data.**

## Wat deze repo doet

- **ETF Flows** — dagelijkse Bitcoin & Ethereum instroom/uitstroom  
- **Whale Tracking** — detectie grote transacties (>$50M)  
- **On-Chain Metrics** — exchange flows, supply distributie, NUPL (Glassnode)  
- **Orderbook Liquidity** — bid/ask spreads & diepte (CoinGlass / exchanges)  
- **Macro Data** — olieprijzen, rentes, Fed verwachtingen

## Automatische Workflows

| Workflow                  | Frequentie          | Wat het doet                              |
|---------------------------|---------------------|-------------------------------------------|
| daily-etf-update.yml      | Dagelijks 08:00 UTC | ETF flow data ophalen                     |
| hourly-whale-tracker.yml  | Elke 2 uur          | Grote transacties detecteren              |
| daily-onchain-metrics.yml | Dagelijks 08:00 UTC | Glassnode metrics verzamelen              |
| weekly-macro-report.yml   | Wekelijks maandag   | Macro analyse (olie, rente, geopolitiek)  |

## Installatie & gebruik

```bash
# 1. Clone
git clone https://github.com/Pvr1978/alchemie-portal-analyses.git
cd alchemie-portal-analyses

# 2. Python dependencies (meeste scripts zijn Python)
pip install -r requirements.txt

# 3. Optioneel: Node.js scripts (als je die gebruikt)
# cd nodejs-scripts
# npm install
