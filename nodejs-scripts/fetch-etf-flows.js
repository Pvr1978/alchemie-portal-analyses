const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs').promises;
const path = require('path');

async function fetchBitcoinEtfFlows() {
  const url = 'https://farside.co.uk/btc/';
  const headers = {
    'User-Agent': 'AlchemiePortal-ETFScraper/1.0 (github.com/Pvr1978/alchemie-portal-analyses)',
    'Accept': 'text/html,application/xhtml+xml',
  };

  try {
    console.log(`Fetching ETF flows from ${url}...`);
    const response = await axios.get(url, { headers, timeout: 15000 });
    if (response.status !== 200) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const $ = cheerio.load(response.data);
    const table = $('table').first();

    if (!table.length) {
      throw new Error('Geen tabel gevonden op de pagina. Site structuur gewijzigd?');
    }

    console.log('Tabel gevonden. Parsing laatste rijen...');

    let output = `# Bitcoin Spot ETF Flows Update - ${new Date().toISOString().split('T')[0]}\n\n`;
    output += `Bron: ${url} (live scrape)\n`;
    output += 'Opmerking: Flows in US$m. Negatieve waarden = outflows. Pending dagen vaak leeg of 0.\n\n';
    output += '| Date          | Total Net Flow (US$m) | Key Notes                  |\n';
    output += '|---------------|-----------------------|----------------------------|\n';

    let latestDate = '';
    let latestTotal = '0.0';

    // Neem de laatste 7 rijen (header + laatste 6 dagen)
    const rows = table.find('tr').slice(-7);
    rows.each((i, row) => {
      const cols = $(row).find('td, th');
      if (cols.length < 3) return; // skip lege rijen

      const dateCell = $(cols[0]).text().trim();
      const totalCell = $(cols).last().text().trim().replace(/[\(\),]/g, ''); // verwijder ( ) en ,

      if (dateCell && dateCell.match(/\d{1,2}\s[A-Za-z]+\s2026/)) { // flexibele datum match
        let note = '';
        if (totalCell === '0.0' || totalCell === '') {
          note = 'Pending / post-FOMC / holiday';
        } else if (parseFloat(totalCell) > 0) {
          note = 'Net inflow';
        } else if (parseFloat(totalCell) < 0) {
          note = 'Net outflow';
        }

        output += `| ${dateCell.padEnd(13)} | ${totalCell.padStart(21)} | ${note} |\n`;

        if (i > 0) { // skip header
          latestDate = dateCell;
          latestTotal = totalCell;
        }
      }
    });

    output += `\n**Meest recente:** ${latestDate || 'Geen recente data'} → **${latestTotal} US$m**\n`;
    output += 'Cumulatief historisch inflows: ~$56B+ (sterk positief langetermijn).\n';
    output += 'Run dagelijks voor updates. Voor auto: GitHub Actions cron.\n';

    console.log(output);

    // Optioneel opslaan (handig lokaal, in Actions kun je artifact maken)
    const outputPath = path.join(__dirname, 'etf_flows_latest.md');
    await fs.writeFile(outputPath, output, 'utf8');
    console.log(`Opgeslagen in: ${outputPath}`);

    return output;

  } catch (err) {
    console.error('Fout bij ophalen / parsen ETF flows:', err.message);
    console.error(err.stack);
    return `Error: ${err.message}. Check handmatig: https://farside.co.uk/btc/`;
  }
}

fetchBitcoinEtfFlows().catch(err => console.error('Unhandled error:', err));
