# Alchemie Portal Analyses

**Data-gedreven crypto-analyses** — whale tracking, ETF flows, orderbook snapshots, on-chain metrics & macro-overzichten.  
Alles gebouwd met **gratis / free-tier APIs** waar mogelijk, geautomatiseerd via GitHub Actions, en gevisualiseerd voor @AlchemiePortal op X.

Live demo's & daily updates: https://x.com/AlchemiePortal

## Kernfeatures

- **Dagelijkse / uurlijkse automatisering** via GitHub Actions
- Real-time & historische data scraping
- Schone Markdown outputs voor copy-paste naar X posts / portal
- Minimale dependencies + robuuste error handling
- Geen betaalde API-keys vereist voor basisfunctionaliteit

## Gebruikte gratis / free-tier data bronnen

| Categorie               | Bronnen                                      | Toegangstype          | Opmerkingen |
|-------------------------|----------------------------------------------|-----------------------|-------------|
| ETF flows & liquidations| CoinGlass public endpoints                   | Free public           | Dagelijkse BTC/ETH/SOL flows |
| Whale transacties       | Whale Alert public API                       | Free public           | Grote tx alerts |
| Orderbooks & spreads    | CCXT library (Binance, OKX, Bitvavo, Coinbase, etc.) | Public endpoints | Live depth snapshots |
| On-chain metrics        | Glassnode free tier / Messari free / Santiment free | Free tier API keys (optioneel) | Addresses, reserves, active wallets |
| Macro data              | FRED API / Alpha Vantage free                | Free API key          | Olie, rente, goud, dollar index |

**Opmerking**: Voor geavanceerde endpoints (bijv. Glassnode high-volume calls) kun je gratis API keys aanvragen, maar de core scripts werken zonder.

## Installatie (lokaal)

```bash
# 1. Clone de repo
git clone https://github.com/Pvr1978/alchemie-portal-analyses.git
cd alchemie-portal-analyses

# 2. Maak & activeer virtual environment
python -m venv venv
source venv/bin/activate          # Linux/Mac
# of op Windows:
# venv\Scripts\activate

# 3. Installeer dependencies
pip install -r requirements.txt

# 4. Optioneel: kopieer .env voorbeeld (meeste scripts werken zonder keys)
cp .env.example .env
# Open .env en vul keys in als je Glassnode/Alpha Vantage gebruikt
