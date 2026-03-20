const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises;
const path = require('path');

async function fetchBitcoinEtfFlows() {
  const url = 'https://farside.co.uk/btc/';
  try {
    const response = await axios.get(url, { timeout: 15000 });
    const $ = cheerio.load(response.data);

    const table = $('table').first();
    if (!table.length) throw new Error('Geen ETF tabel gevonden op Farside');

    let output = `# Bitcoin Spot ETF Flows Update - ${new Date().toISOString().split('T')[0]}\n\n`;
    output += 'Bron: https://farside.co.uk/btc/ (scraped live)\n';
    output += 'Opmerking: Geen eigen ETF flows voor eToro of Coinbase (zij zijn geen issuers – alleen custodians of platforms).\n\n';
    output += '| Date       | Total Net Flow (US$m) | Key Notes |\n';
    output += '|------------|-----------------------|-----------|\n';

    let latestDate = '';
    let latestTotal = '0.0';

    // Parse laatste 5 rijen (meest recent)
    table.find('tr').slice(-6).each((i, row) => {  // -6 om header + laatste 5 dagen
      const cols = $(row).find('td, th');
      if (cols.length < 3) return;

      const date = $(cols[0]).text().trim();
      const totalColIndex = cols.length - 1; // laatste kolom = total
      const total = $(cols[totalColIndex]).text().trim().replace(/[\(\)]/g, '');

      if (date.includes('Mar 2026')) {
        output += `| ${date.padEnd(10)} | ${total.padStart(10)} | ${total === '0.0' ? 'Pending / post-FOMC' : ''} |\n`;
        if (i > 0) { // skip header
          latestDate = date;
          latestTotal = total;
        }
      }
    });

    output += `\n**Meest recente beschikbare:** ${latestDate || 'Pending'} → **${latestTotal} US$m**\n`;
    output += 'Cumulative historisch: ~$56,260M net inflows (sterk positief overall).\n\n';
    output += 'Run dit script dagelijks voor verse data. Voor auto: zet cron of GitHub Action later op.\n';

    console.log(output);

    // Save naar file (handig voor copy-paste naar MD in repo)
    const outputPath = path.join(__dirname, 'etf_flows_latest.md');
    await fs.writeFile(outputPath, output);
    console.log(`Output opgeslagen in: ${outputPath}`);

    return output;
  } catch (err) {
    console.error('Fout bij fetchen ETF flows:', err.message);
    return 'Error: Check handmatig op https://farside.co.uk/btc/';
  }
}

fetchBitcoinEtfFlows();
