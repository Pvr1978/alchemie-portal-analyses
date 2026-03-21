const https = require('https');

console.log("Node.js Orderbook");
console.log(new Date().toISOString());
console.log("=".repeat(30));

const url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd";

https.get(url, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        try {
            const json = JSON.parse(data);
            console.log(`BTC: $${json.bitcoin.usd.toLocaleString()}`);
        } catch (e) {
            console.log("Error:", e.message);
        }
    });
}).on('error', (err) => {
    console.log("Request failed:", err.message);
});
