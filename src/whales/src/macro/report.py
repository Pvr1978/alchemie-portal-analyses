```python
import requests
from datetime import datetime

def get_oil_price():
    try:
        url = "https://api.oilprice.com/api/v1/prices?key=free&code=brent"
        response = requests.get(url)
        data = response.json()
        return data.get("price", "N/A")
    except:
        return "N/A"

def get_uk_yield():
    try:
        url = "https://api.tradingeconomics.com/markets/yield?c=GB10Y&format=json"
        response = requests.get(url)
        data = response.json()
        return data[0].get("last", "N/A")
    except:
        return "N/A"

if __name__ == "__main__":
    print(f"Macro Report | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Brent crude: ${get_oil_price()}")
    print(f"UK 10Y yield: {get_uk_yield()}%")
    print("Macro data verzameld")
```
