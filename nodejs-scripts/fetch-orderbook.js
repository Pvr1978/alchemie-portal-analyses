const https = require('https');

function getOrderbook(symbol = 'bitcoin') {
    const url = `https://api.coingecko.com/api/v3/order_book?symbol=${symbol}`;
    
    console.log(`\n Fetching orderbook for ${symbol.toUpperCase()}...`);
    
    https.get(url, (res) => {
        let data = '';
        
        res.on('data', (chunk) => {
            data += chunk;
        });
        
        res.on('end', () => {
            try {
                const json = JSON.parse(data);
                
                console.log(`\n ORDERBOOK: ${symbol.toUpperCase()}`);
                console.log(`Time: ${new Date().toISOString()}`);
                
                if (json.bids && json.asks) {
                    console.log(`Bids: ${json.bids.length} levels`);
                    console.log(`Asks: ${json.asks.length} levels`);
                    
                    console.log('\nTop bids:');
                    for (let i = 0; i < Math.min(3, json.bids.length); i++) {
                        console.log(`  ${json.bids[i][0]} -> ${json.bids[i][1]}`);
                    }
                    
                    console.log('\nTop asks:');
                    for (let i = 0; i < Math.min(3, json.asks.length); i++) {
                        console.log(`  ${json.asks[i][0]} -> ${json.asks[i][1]}`);
                    }
                } else {
                    console.log(' No orderbook data available');
                }
            } catch (e) {
                console.log(' Error parsing:', e.message);
            }
        });
    }).on('error', (err) => {
        console.log(' Request failed:', err.message);
    });
}

getOrderbook('bitcoin');
