# src/test.py - simpele debug/test voor ETF flows of API calls

import requests
import datetime

print("Test script gestart op", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

url = "https://farside.co.uk/btc/"
print("Probeer pagina op te halen:", url)

try:
    response = requests.get(url, timeout=10)
    print("Status code:", response.status_code)
    print("Eerste 200 chars content:", response.text[:200])

    # Lijn ~21: voorbeeld van mogelijke fout (verander dit om te testen)
    data = response.json()  # <-- FOUT op lijn 21: dit is HTML, geen JSON → ValueError/JSONDecodeError
    print("JSON data:", data)

except Exception as e:
    print("Fout tijdens request:", str(e))

print("Script klaar")
