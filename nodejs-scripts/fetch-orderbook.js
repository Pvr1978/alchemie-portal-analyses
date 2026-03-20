```javascript
// fetch-orderbook.js
// Live orderbook data from OKX and Bitvavo

const axios = require('axios');

async function fetchOKXOrderbook() {
  try {
    const response = await axios.get('https://www.okx.com/api/v5/market/books?instId=BTC-USDT&sz=10');
    const data = response.data.data[0];
    
    const bids = data.bids.slice(0, 5).map(bid => ({ price: bid[0], size: bid[1] }));
    const asks = data.asks.slice(0, 5).map(ask => ({ price: ask[0], size: ask[1] }));
    
    console.log('=== OKX BTC-USDT Orderbook ===');
    console.log('Bids (buy):', bids);
    console.log('Asks (sell):', asks);
    
    const bidVolume = data.bids.reduce((sum, bid) => sum + parseFloat(bid[1]), 0);
    const askVolume = data.asks.reduce((sum, ask) => sum + parseFloat(ask[1]), 0);
    console.log(`\nTotal Bids: ${bidVolume.toFixed(4)} BTC`);
    console.log(`Total Asks: ${askVolume.toFixed(4)} BTC`);
    console.log(`Bid/Ask Ratio: ${(bidVolume / askVolume).toFixed(2)}`);
    
  } catch (error) {
    console.error('Error fetching OKX data:', error.message);
  }
}

async function fetchBitvavoOrderbook() {
  try {
    const response = await axios.get('https://api.bitvavo.com/v2/orderbook?market=BTC-EUR&depth=10');
    const data = response.data;
    
    const bids = data.bids.slice(0, 5).map(bid => ({ price: bid.price, amount: bid.amount }));
    const asks = data.asks.slice(0, 5).map(ask => ({ price: ask.price, amount: ask.amount }));
    
    console.log('\n=== Bitvavo BTC-EUR Orderbook ===');
    console.log('Bids (buy):', bids);
    console.log('Asks (sell):', asks);
    
  } catch (error) {
    console.error('Error fetching Bitvavo data:', error.message);
  }
}

fetchOKXOrderbook();
fetchBitvavoOrderbook();
```
