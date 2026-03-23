# Node.js Scripts – Live Exchange & ETF Data

Deze map bevat **Node.js scripts** voor real-time crypto market data scraping en snapshots, specifiek gebouwd voor de **Alchemie Portal** (@AlchemiePortal op X).

De scripts draaien dagelijks/uurlijks via GitHub Actions en genereren output voor whale tracking, ETF flows en orderbook depth visualisaties.

## Scripts overzicht

| Script                  | Doel                                                                 | Output bestand(en)                  | Frequentie (Actions) | Dependencies |
|-------------------------|----------------------------------------------------------------------|-------------------------------------|-----------------------|--------------|
| `fetch-orderbook.js`    | Haalt live orderbook depth van OKX, Bitvavo, Coinbase (BTC/USDT, ETH/USDT, etc.) | `orderbook_snapshot_YYYY-MM-DD.md` / JSON | Elke 2 uur           | axios       |
| `fetch-etf-flows.js`    | Scraped dagelijkse BTC/ETH/SOL spot ETF net flows van Farside Investors | `etf_flows_latest.md` / `etf_flows_YYYY-MM-DD.md` | Dagelijks            | axios, cheerio |

## Vereisten

- Node.js ≥ 20.0.0 (aanbevolen: 20.18+ via Volta of nvm)
- npm ≥ 10

## Installatie

```bash
# Clone de repo (als je dat nog niet hebt)
git clone https://github.com/Pvr1978/alchemie-portal-analyses.git
cd alchemie-portal-analyses/nodejs-scripts

# Installeer dependencies
npm install
# of met exacte lockfile (aanbevolen in CI)
npm ci
