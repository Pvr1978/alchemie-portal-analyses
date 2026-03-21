# Alchemie Portal Analyses

Crypto data-analyse met on-chain metrics, whale tracking, ETF flows en macro-economische correlaties.

## Wat deze repo doet

- **ETF Flows:** Dagelijkse instroom/uitstroom van Bitcoin en Ethereum ETF's
- **Whale Tracking:** Detectie van grote transacties (>$50M) op blockchain
- **On-Chain Metrics:** Exchange flows, supply distributie, NUPL (via Glassnode)
- **Orderbook Liquidity:** Bid/ask spreads en diepte (via CoinGlass)
- **Macro Data:** Olieprijzen, rentes, Fed verwachtingen

## Automatische Workflows

| Workflow | Frequentie | Wat |
|----------|------------|-----|
| `daily-etf-update.yml` | Dagelijks 08:00 UTC | ETF flow data ophalen |
| `hourly-whale-tracker.yml` | Elke 2 uur | Grote transacties detecteren |
| `daily-onchain-metrics.yml` | Dagelijks 08:00 UTC | Glassnode metrics verzamelen |
| `weekly-macro-report.yml` | Wekelijks maandag | Macro analyse (olie, rente, geopolitiek) |

## Installatie

1. Clone de repo:
```bash
git clone https://github.com/Pvr1978/alchemie-portal-analyses.git
cd alchemie-portal-analyses
