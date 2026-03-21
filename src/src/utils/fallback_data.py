```python
# Fallback data voor wanneer APIs niet werken

FALLBACK_BTC_PRICE = 72400
FALLBACK_BTC_DOMINANCE = 58.5
FALLBACK_FEAR_GREED = {"value": 50, "classification": "Neutral"}

def get_fallback_btc_price():
    print("[FALLBACK] Using default BTC price")
    return FALLBACK_BTC_PRICE

def get_fallback_btc_dominance():
    print("[FALLBACK] Using default BTC dominance")
    return FALLBACK_BTC_DOMINANCE

def get_fallback_fear_greed():
    print("[FALLBACK] Using default Fear & Greed")
    return FALLBACK_FEAR_GREED
```
