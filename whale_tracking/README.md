# 🐋 Alchemie Whale Tracking

Advanced cryptocurrency whale transaction tracker and analyzer for Bitcoin and Ethereum.

## 📊 Features

- **Multi-Chain Support**: Bitcoin & Ethereum whale detection
- **Multi-API Fallback**: Automatic failover between Etherscan, Blockchain.com, and Blockchair
- **Configurable Thresholds**: Customize whale detection levels per cryptocurrency
- **Real-time Monitoring**: Continuous tracking with deduplication
- **Export Functions**: CSV, JSON data export for further analysis
- **Standalone & Modular**: Can be used as library or standalone script

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/Pvr1978/alchemie-portal-analyses.git
cd alchemie-portal-analyses/whale_tracking
pip install -r requirements.txt
```

### Basic Usage

```python
from whale_tracking import WhaleTracker
import asyncio

async def main():
    tracker = WhaleTracker()
    
    # Get Bitcoin whales (transactions > $1M)
    btc_whales = await tracker.get_btc_whale_transactions(
        min_value_usd=1_000_000,
        limit=10
    )
    
    # Get Ethereum whales (transactions > $500k)
    eth_whales = await tracker.get_eth_whale_transactions(
        min_value_usd=500_000,
        limit=10,
        etherscan_key="YOUR_KEY"  # Optional but recommended
    )
    
    # Print results
    for whale in btc_whales:
        print(tracker.format_whale_alert(whale))

asyncio.run(main())
```

### Command Line Usage

```bash
# Test whale tracking
python whale_tracking.py

# With custom parameters
python whale_tracking.py --btc-threshold 2000000 --eth-threshold 1000000 --limit 20
```

## 🔑 API Keys

### Etherscan (Recommended for ETH)
1. Create free account at [etherscan.io](https://etherscan.io/apis)
2. Generate API key
3. Set environment variable: `export ETHERSCAN_API_KEY=your_key`

### No Keys Required
- Blockchain.com API (Bitcoin)
- Blockchair API (Bitcoin fallback)

## 📈 Data Output Format

```python
{
    'hash': 'abc123...',
    'value_btc': 25.5432,
    'value_usd': 2425000.00,
    'timestamp': '2025-04-09T15:30:00',
    'blockchain': 'Bitcoin',
    'source': 'Blockchain.com',
    'inputs': 3,
    'outputs': 2
}
```

## ⚙️ Configuration

Edit thresholds in `whale_tracking.py`:

```python
whale_thresholds = {
    'BTC': 1_000_000,  # $1M+
    'ETH': 500_000,    # $500k+
    'XRP': 100_000     # $100k+
}
```

## 🔄 API Fallback Chain

### Bitcoin
1. **Blockchain.com** → Unconfirmed transactions
2. **Blockchair** → Historical queries with USD filtering

### Ethereum  
1. **Etherscan** → Best data quality (requires key)
2. **Blockchain.com** → Limited fallback

## 📊 Use Cases

- **Market Research**: Analyze large holder movements
- **Trading Signals**: Detect significant capital flows
- **Network Analysis**: Study transaction patterns
- **Academic Research**: Cryptocurrency movement studies
- **Alert Systems**: Real-time whale notifications

## 🛠️ Development

### Project Structure
```
whale_tracking/
├── whale_tracking.py    # Main module
├── requirements.txt     # Dependencies
├── README.md           # This file
├── examples/           # Usage examples
└── etf_flows/         # ETF flow analysis (separate)
```

### Dependencies
```
aiohttp>=3.9.0
asyncio
```

### Testing
```bash
python whale_tracking.py
```

## 📝 Advanced Usage

### Export to CSV

```python
import csv
from whale_tracking import WhaleTracker

tracker = WhaleTracker()
whales = await tracker.get_btc_whale_transactions(limit=50)

with open('whale_data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=whales[0].keys())
    writer.writeheader()
    writer.writerows(whales)
```

### Continuous Monitoring

```python
async def alert_callback(whale):
    print(f"🚨 New whale detected: ${whale['value_usd']:,.0f}")
    # Add your custom logic here

await tracker.monitor_whales(
    callback=alert_callback,
    check_interval=60
)
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📜 License

MIT License - see LICENSE file for details

## 🔗 Related Projects

- [Alchemie Bot](https://github.com/Pvr1978/alchemie-bot) - Telegram trading bot
- [ETF Flows Tracker](./etf_flows/) - Bitcoin/Ethereum ETF monitoring

## 📧 Contact

Patrick - [@Pvr1978](https://github.com/Pvr1978)

Project Link: [https://github.com/Pvr1978/alchemie-portal-analyses](https://github.com/Pvr1978/alchemie-portal-analyses)

---

**Disclaimer**: This tool is for research and educational purposes. Not financial advice.
