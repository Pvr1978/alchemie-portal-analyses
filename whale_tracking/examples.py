"""
Whale Tracking Examples
========================
Voorbeelden van verschillende use cases voor whale tracking.
"""

import asyncio
import csv
import json
from datetime import datetime
from whale_tracking import WhaleTracker


# ============================================================================
# VOORBEELD 1: Basic Whale Detection
# ============================================================================

async def example_basic_tracking():
    """Simpel voorbeeld: haal whales op en print ze."""
    print("\n" + "="*60)
    print("VOORBEELD 1: Basic Whale Tracking")
    print("="*60)
    
    tracker = WhaleTracker()
    
    # Bitcoin whales
    print("\n🔍 Ophalen Bitcoin whales...")
    btc_whales = await tracker.get_btc_whale_transactions(
        min_value_usd=1_000_000,
        limit=5
    )
    
    for whale in btc_whales:
        print("\n" + tracker.format_whale_alert(whale))


# ============================================================================
# VOORBEELD 2: Export naar CSV
# ============================================================================

async def example_export_csv():
    """Export whale data naar CSV file."""
    print("\n" + "="*60)
    print("VOORBEELD 2: Export naar CSV")
    print("="*60)
    
    tracker = WhaleTracker()
    
    # Haal data op
    btc_whales = await tracker.get_btc_whale_transactions(
        min_value_usd=500_000,
        limit=20
    )
    
    if not btc_whales:
        print("⚠️  Geen whale data beschikbaar")
        return
    
    # Export naar CSV
    filename = f"btc_whales_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=btc_whales[0].keys())
        writer.writeheader()
        writer.writerows(btc_whales)
    
    print(f"\n✅ {len(btc_whales)} whales geëxporteerd naar {filename}")


# ============================================================================
# VOORBEELD 3: Export naar JSON
# ============================================================================

async def example_export_json():
    """Export whale data naar JSON file."""
    print("\n" + "="*60)
    print("VOORBEELD 3: Export naar JSON")
    print("="*60)
    
    tracker = WhaleTracker()
    
    # Haal beide chains op
    btc_whales = await tracker.get_btc_whale_transactions(
        min_value_usd=1_000_000,
        limit=10
    )
    
    eth_whales = await tracker.get_eth_whale_transactions(
        min_value_usd=500_000,
        limit=10
    )
    
    # Combineer in één dataset
    data = {
        'timestamp': datetime.now().isoformat(),
        'bitcoin_whales': btc_whales,
        'ethereum_whales': eth_whales,
        'summary': {
            'btc_count': len(btc_whales),
            'eth_count': len(eth_whales),
            'total_btc_value': sum(w['value_usd'] for w in btc_whales),
            'total_eth_value': sum(w['value_usd'] for w in eth_whales)
        }
    }
    
    # Export naar JSON
    filename = f"whale_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✅ Whale report geëxporteerd naar {filename}")
    print(f"   - Bitcoin whales: {data['summary']['btc_count']}")
    print(f"   - Ethereum whales: {data['summary']['eth_count']}")
    print(f"   - Total BTC value: ${data['summary']['total_btc_value']:,.0f}")
    print(f"   - Total ETH value: ${data['summary']['total_eth_value']:,.0f}")


# ============================================================================
# VOORBEELD 4: Real-time Monitoring
# ============================================================================

async def example_realtime_monitoring():
    """Real-time whale monitoring met callback."""
    print("\n" + "="*60)
    print("VOORBEELD 4: Real-time Monitoring")
    print("="*60)
    print("\n⏰ Monitoring gestart... (druk Ctrl+C om te stoppen)")
    
    tracker = WhaleTracker()
    
    # Callback functie
    async def whale_callback(whale_data):
        print(f"\n🚨 NIEUWE WHALE GEDETECTEERD!")
        print(tracker.format_whale_alert(whale_data))
        
        # Optioneel: sla op in database, stuur alert, etc.
    
    try:
        # Start monitoring (draait oneindig)
        await tracker.monitor_whales(
            callback=whale_callback,
            check_interval=60  # Check elke minuut
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring gestopt")


# ============================================================================
# VOORBEELD 5: Custom Thresholds
# ============================================================================

async def example_custom_thresholds():
    """Gebruik custom whale thresholds."""
    print("\n" + "="*60)
    print("VOORBEELD 5: Custom Thresholds")
    print("="*60)
    
    tracker = WhaleTracker()
    
    # Verlaag threshold voor meer resultaten
    print("\n🔍 Low threshold ($100k+):")
    low_whales = await tracker.get_btc_whale_transactions(
        min_value_usd=100_000,
        limit=5
    )
    print(f"   Gevonden: {len(low_whales)} transactions")
    
    # Verhoog threshold voor only mega whales
    print("\n🔍 High threshold ($10M+):")
    high_whales = await tracker.get_btc_whale_transactions(
        min_value_usd=10_000_000,
        limit=5
    )
    print(f"   Gevonden: {len(high_whales)} transactions")


# ============================================================================
# VOORBEELD 6: Multi-Chain Comparison
# ============================================================================

async def example_multi_chain_comparison():
    """Vergelijk whale activity tussen chains."""
    print("\n" + "="*60)
    print("VOORBEELD 6: Multi-Chain Comparison")
    print("="*60)
    
    tracker = WhaleTracker()
    
    # Haal beide chains op met gelijke threshold
    threshold = 1_000_000
    
    print(f"\n📊 Vergelijking whale activity (>${threshold:,.0f} USD)")
    
    btc_whales = await tracker.get_btc_whale_transactions(
        min_value_usd=threshold,
        limit=10
    )
    
    eth_whales = await tracker.get_eth_whale_transactions(
        min_value_usd=threshold,
        limit=10
    )
    
    # Statistieken
    print(f"\n📈 Bitcoin:")
    print(f"   - Whales: {len(btc_whales)}")
    if btc_whales:
        print(f"   - Total value: ${sum(w['value_usd'] for w in btc_whales):,.0f}")
        print(f"   - Average: ${sum(w['value_usd'] for w in btc_whales) / len(btc_whales):,.0f}")
    
    print(f"\n📈 Ethereum:")
    print(f"   - Whales: {len(eth_whales)}")
    if eth_whales:
        print(f"   - Total value: ${sum(w['value_usd'] for w in eth_whales):,.0f}")
        print(f"   - Average: ${sum(w['value_usd'] for w in eth_whales) / len(eth_whales):,.0f}")


# ============================================================================
# MAIN MENU
# ============================================================================

async def main():
    """Hoofdmenu voor examples."""
    print("\n🐋 WHALE TRACKING EXAMPLES")
    print("=" * 60)
    print("\nKies een voorbeeld:")
    print("1. Basic Whale Tracking")
    print("2. Export naar CSV")
    print("3. Export naar JSON")
    print("4. Real-time Monitoring")
    print("5. Custom Thresholds")
    print("6. Multi-Chain Comparison")
    print("0. Alles uitvoeren (behalve real-time)")
    
    choice = input("\nKeuze (0-6): ").strip()
    
    examples = {
        '1': example_basic_tracking,
        '2': example_export_csv,
        '3': example_export_json,
        '4': example_realtime_monitoring,
        '5': example_custom_thresholds,
        '6': example_multi_chain_comparison,
    }
    
    if choice == '0':
        # Voer alles uit behalve real-time
        for key in ['1', '2', '3', '5', '6']:
            await examples[key]()
    elif choice in examples:
        await examples[choice]()
    else:
        print("❌ Ongeldige keuze")


if __name__ == "__main__":
    asyncio.run(main())
