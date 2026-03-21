#Alchemie Portal Analyses

Data-gedreven crypto-analyses (whale tracking, ETF flows, orderbooks, on-chain, macro) — gebouwd met **gratis APIs** waar mogelijk.

## Gratis / free-tier data bronnen die gebruikt worden
- ETF flows & liquidations → CoinGlass public endpoints
- Whale transacties → Whale Alert public API
- Orderbooks & spreads → CCXT (public data van Binance, Bybit, OKX, etc.)
- On-chain basis metrics → Glassnode free tier of Messari/Santiment free
- Macro (olie, rente) → FRED API of Alpha Vantage free

## Installatie (lokaal)

```bash
git clone https://github.com/Pvr1978/alchemie-portal-analyses.git
cd alchemie-portal-analyses

python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Optioneel: maak .env aan (meeste calls werken zonder keys)
cp .env.example .env
