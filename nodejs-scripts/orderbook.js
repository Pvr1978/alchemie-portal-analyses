name: Node.js Orderbook - Debug

on:
  workflow_dispatch:

jobs:
  orderbook:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Debug folder & file
        run: |
          pwd
          ls -la nodejs-scripts || echo "Map nodejs-scripts ontbreekt!"
          ls -la nodejs-scripts/orderbook.js || echo "orderbook.js NIET gevonden!"
          echo "Node versie:"
          node --version

      - name: Run orderbook script met logging
        run: |
          node nodejs-scripts/orderbook.js > orderbook_output.log 2>&1 || echo "Script faalde met exit code $?"
          echo "\n=== Volledige output / error ==="
          cat orderbook_output.log || echo "Geen output log"

      - name: Upload log (ook bij falen)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: orderbook-debug-log
          path: orderbook_output.log
