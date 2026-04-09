"""
Alchemie Whale Tracking Module
===============================
Track grote crypto transacties (whales) met multi-API fallback.
Ondersteunt Bitcoin en Ethereum whale detection.

Author: Patrick (Pvr1978)
Created: 2025
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class WhaleTracker:
    """
    Whale transaction tracker met fallback APIs.
    Ondersteunt Ethereum en Bitcoin whale tracking.
    """
    
    def __init__(self):
        """Initialize whale tracker met API configuratie."""
        self.eth_apis = [
            {
                'name': 'Etherscan',
                'url': 'https://api.etherscan.io/api',
                'key_required': True
            },
            {
                'name': 'Blockchain.com',
                'url': 'https://blockchain.info',
                'key_required': False
            }
        ]
        
        self.btc_apis = [
            {
                'name': 'Blockchain.com',
                'url': 'https://blockchain.info',
                'key_required': False
            },
            {
                'name': 'Blockchair',
                'url': 'https://api.blockchair.com',
                'key_required': False
            }
        ]
        
        # Whale thresholds (in USD)
        self.whale_thresholds = {
            'BTC': 1_000_000,  # $1M+
            'ETH': 500_000,    # $500k+
            'XRP': 100_000     # $100k+
        }
        
        # Cache voor seen transactions
        self.seen_hashes = set()
    
    async def get_eth_whale_transactions(
        self,
        min_value_usd: float = 500_000,
        limit: int = 10,
        etherscan_key: Optional[str] = None
    ) -> List[Dict]:
        """
        Haal recente Ethereum whale transactions op.
        
        Args:
            min_value_usd: Minimum transactie waarde in USD
            limit: Maximaal aantal transacties
            etherscan_key: Etherscan API key (optioneel)
            
        Returns:
            List van whale transaction dictionaries
        """
        try:
            # Probeer eerst Etherscan (beste data)
            if etherscan_key:
                logger.info("Probeer Etherscan API voor ETH whales...")
                transactions = await self._fetch_etherscan_whales(
                    etherscan_key,
                    min_value_usd,
                    limit
                )
                if transactions:
                    logger.info(f"✅ {len(transactions)} ETH whales gevonden via Etherscan")
                    return transactions
            
            # Fallback: Blockchain.com API
            logger.info("Fallback naar Blockchain.com voor ETH whales...")
            transactions = await self._fetch_blockchain_eth_whales(
                min_value_usd,
                limit
            )
            
            if transactions:
                logger.info(f"✅ {len(transactions)} ETH whales gevonden via Blockchain.com")
            else:
                logger.warning("Geen ETH whale data beschikbaar")
            
            return transactions
            
        except Exception as e:
            logger.error(f"❌ Fout bij ophalen ETH whale transactions: {e}")
            return []
    
    async def get_btc_whale_transactions(
        self,
        min_value_usd: float = 1_000_000,
        limit: int = 10
    ) -> List[Dict]:
        """
        Haal recente Bitcoin whale transactions op.
        
        Args:
            min_value_usd: Minimum transactie waarde in USD
            limit: Maximaal aantal transacties
            
        Returns:
            List van whale transaction dictionaries
        """
        try:
            # Probeer Blockchain.com
            logger.info("Probeer Blockchain.com API voor BTC whales...")
            transactions = await self._fetch_blockchain_btc_whales(
                min_value_usd,
                limit
            )
            
            if transactions:
                logger.info(f"✅ {len(transactions)} BTC whales gevonden via Blockchain.com")
                return transactions
            
            # Fallback: Blockchair
            logger.info("Fallback naar Blockchair voor BTC whales...")
            transactions = await self._fetch_blockchair_btc_whales(
                min_value_usd,
                limit
            )
            
            if transactions:
                logger.info(f"✅ {len(transactions)} BTC whales gevonden via Blockchair")
            else:
                logger.warning("Geen BTC whale data beschikbaar")
            
            return transactions
            
        except Exception as e:
            logger.error(f"❌ Fout bij ophalen BTC whale transactions: {e}")
            return []
    
    async def _fetch_etherscan_whales(
        self,
        api_key: str,
        min_value_usd: float,
        limit: int
    ) -> List[Dict]:
        """
        Fetch Ethereum whales via Etherscan API.
        
        Args:
            api_key: Etherscan API key
            min_value_usd: Minimum waarde in USD
            limit: Max aantal resultaten
            
        Returns:
            List van whale transactions
        """
        url = "https://api.etherscan.io/api"
        
        # Haal recent blocks op voor whale scanning
        params = {
            'module': 'proxy',
            'action': 'eth_blockNumber',
            'apikey': api_key
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get latest block
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status != 200:
                        logger.warning(f"Etherscan API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    latest_block = int(data.get('result', '0x0'), 16)
                
                # Get transactions from recent blocks
                params = {
                    'module': 'account',
                    'action': 'txlist',
                    'startblock': latest_block - 1000,  # Last ~1000 blocks
                    'endblock': latest_block,
                    'page': 1,
                    'offset': limit * 3,
                    'sort': 'desc',
                    'apikey': api_key
                }
                
                async with session.get(url, params=params, timeout=15) as response:
                    if response.status != 200:
                        return []
                    
                    data = await response.json()
                    
                    if data.get('status') != '1':
                        logger.warning(f"Etherscan API response: {data.get('message', 'Unknown error')}")
                        return []
                    
                    transactions = data.get('result', [])
                    
                    # Filter op waarde en format
                    whale_txs = []
                    eth_price = 3500  # Placeholder - integreer met je price API
                    
                    for tx in transactions:
                        try:
                            value_eth = int(tx.get('value', 0)) / 1e18
                            
                            if value_eth < 100:  # Skip kleine amounts
                                continue
                            
                            value_usd = value_eth * eth_price
                            
                            if value_usd >= min_value_usd:
                                whale_txs.append({
                                    'hash': tx.get('hash'),
                                    'from': tx.get('from'),
                                    'to': tx.get('to'),
                                    'value_eth': round(value_eth, 4),
                                    'value_usd': round(value_usd, 2),
                                    'timestamp': datetime.fromtimestamp(
                                        int(tx.get('timeStamp', 0))
                                    ).isoformat(),
                                    'blockchain': 'Ethereum',
                                    'source': 'Etherscan',
                                    'block': tx.get('blockNumber')
                                })
                                
                                if len(whale_txs) >= limit:
                                    break
                        except Exception as e:
                            logger.debug(f"Fout bij verwerken tx: {e}")
                            continue
                    
                    return whale_txs[:limit]
                    
        except asyncio.TimeoutError:
            logger.warning("Etherscan API timeout")
            return []
        except Exception as e:
            logger.error(f"Etherscan API error: {e}")
            return []
    
    async def _fetch_blockchain_eth_whales(
        self,
        min_value_usd: float,
        limit: int
    ) -> List[Dict]:
        """
        Fetch Ethereum whales via Blockchain.com (fallback).
        
        Note: Blockchain.com heeft beperkte ETH whale support.
        """
        logger.info("⚠️  Blockchain.com ETH API heeft beperkte whale tracking")
        # Blockchain.com focus is Bitcoin, geen goede ETH whale data
        return []
    
    async def _fetch_blockchain_btc_whales(
        self,
        min_value_usd: float,
        limit: int
    ) -> List[Dict]:
        """
        Fetch Bitcoin whales via Blockchain.com.
        
        Args:
            min_value_usd: Minimum waarde in USD
            limit: Max aantal resultaten
            
        Returns:
            List van whale transactions
        """
        url = "https://blockchain.info/unconfirmed-transactions?format=json"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        logger.warning(f"Blockchain.com API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    transactions = data.get('txs', [])
                    
                    whale_txs = []
                    btc_price = 95000  # Placeholder - integreer met je price API
                    
                    for tx in transactions:
                        try:
                            # Bereken totale output waarde
                            value_satoshi = sum(
                                out.get('value', 0) for out in tx.get('out', [])
                            )
                            value_btc = value_satoshi / 1e8  # Satoshi naar BTC
                            
                            if value_btc < 1:  # Skip kleine amounts
                                continue
                            
                            value_usd = value_btc * btc_price
                            
                            if value_usd >= min_value_usd:
                                whale_txs.append({
                                    'hash': tx.get('hash'),
                                    'value_btc': round(value_btc, 8),
                                    'value_usd': round(value_usd, 2),
                                    'timestamp': datetime.fromtimestamp(
                                        tx.get('time', 0)
                                    ).isoformat(),
                                    'blockchain': 'Bitcoin',
                                    'source': 'Blockchain.com',
                                    'inputs': len(tx.get('inputs', [])),
                                    'outputs': len(tx.get('out', []))
                                })
                                
                                if len(whale_txs) >= limit:
                                    break
                        except Exception as e:
                            logger.debug(f"Fout bij verwerken BTC tx: {e}")
                            continue
                    
                    return whale_txs[:limit]
                    
        except asyncio.TimeoutError:
            logger.warning("Blockchain.com API timeout")
            return []
        except Exception as e:
            logger.error(f"Blockchain.com API error: {e}")
            return []
    
    async def _fetch_blockchair_btc_whales(
        self,
        min_value_usd: float,
        limit: int
    ) -> List[Dict]:
        """
        Fetch Bitcoin whales via Blockchair (fallback).
        
        Args:
            min_value_usd: Minimum waarde in USD
            limit: Max aantal resultaten
            
        Returns:
            List van whale transactions
        """
        url = "https://api.blockchair.com/bitcoin/transactions"
        
        params = {
            'limit': limit * 2,
            'q': f'output_total_usd({int(min_value_usd)}..)' 
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status != 200:
                        logger.warning(f"Blockchair API error: {response.status}")
                        return []
                    
                    data = await response.json()
                    
                    if 'data' not in data:
                        logger.warning("Blockchair: geen data in response")
                        return []
                    
                    transactions = data.get('data', [])
                    
                    whale_txs = []
                    
                    for tx in transactions:
                        try:
                            value_btc = tx.get('output_total', 0) / 1e8
                            value_usd = tx.get('output_total_usd', 0)
                            
                            whale_txs.append({
                                'hash': tx.get('hash'),
                                'value_btc': round(value_btc, 8),
                                'value_usd': round(value_usd, 2),
                                'timestamp': tx.get('time', ''),
                                'blockchain': 'Bitcoin',
                                'source': 'Blockchair',
                                'inputs': tx.get('input_count', 0),
                                'outputs': tx.get('output_count', 0)
                            })
                            
                            if len(whale_txs) >= limit:
                                break
                        except Exception as e:
                            logger.debug(f"Fout bij verwerken Blockchair tx: {e}")
                            continue
                    
                    return whale_txs[:limit]
                    
        except asyncio.TimeoutError:
            logger.warning("Blockchair API timeout")
            return []
        except Exception as e:
            logger.error(f"Blockchair API error: {e}")
            return []
    
    def format_whale_alert(self, transaction: Dict) -> str:
        """
        Format een whale transaction voor Telegram output.
        
        Args:
            transaction: Transaction dictionary
            
        Returns:
            Geformatteerde Markdown string voor Telegram
        """
        blockchain = transaction.get('blockchain', 'Unknown')
        
        if blockchain == 'Bitcoin':
            msg = "🐋 **BTC WHALE ALERT**\n\n"
            msg += f"💰 **Waarde:** {transaction['value_btc']:.4f} BTC\n"
            msg += f"💵 **USD:** ${transaction['value_usd']:,.0f}\n"
            msg += f"📊 **I/O:** {transaction.get('inputs', 0)}/{transaction.get('outputs', 0)}\n"
            msg += f"🔗 **Hash:** `{transaction['hash'][:16]}...`\n"
        else:  # Ethereum
            msg = "🐋 **ETH WHALE ALERT**\n\n"
            msg += f"💰 **Waarde:** {transaction['value_eth']:.4f} ETH\n"
            msg += f"💵 **USD:** ${transaction['value_usd']:,.0f}\n"
            msg += f"📤 **From:** `{transaction['from'][:10]}...`\n"
            msg += f"📥 **To:** `{transaction['to'][:10]}...`\n"
            msg += f"🔗 **Hash:** `{transaction['hash'][:16]}...`\n"
        
        msg += f"⏰ **Time:** {transaction['timestamp'][:19].replace('T', ' ')}\n"
        msg += f"📡 **Source:** {transaction.get('source', 'Unknown')}"
        
        return msg
    
    async def monitor_whales(
        self,
        callback,
        check_interval: int = 60,
        etherscan_key: Optional[str] = None
    ):
        """
        Continuous whale monitoring met callback functie.
        
        Args:
            callback: Async functie die aangeroepen wordt bij nieuwe whale
            check_interval: Check interval in seconden
            etherscan_key: Etherscan API key (optioneel)
        """
        logger.info(f"🐋 Whale monitoring gestart (check interval: {check_interval}s)")
        
        while True:
            try:
                # Check Bitcoin whales
                btc_whales = await self.get_btc_whale_transactions(
                    min_value_usd=self.whale_thresholds['BTC'],
                    limit=5
                )
                
                for whale in btc_whales:
                    if whale['hash'] not in self.seen_hashes:
                        self.seen_hashes.add(whale['hash'])
                        logger.info(f"🆕 Nieuwe BTC whale: ${whale['value_usd']:,.0f}")
                        await callback(whale)
                
                # Check Ethereum whales
                eth_whales = await self.get_eth_whale_transactions(
                    min_value_usd=self.whale_thresholds['ETH'],
                    limit=5,
                    etherscan_key=etherscan_key
                )
                
                for whale in eth_whales:
                    if whale['hash'] not in self.seen_hashes:
                        self.seen_hashes.add(whale['hash'])
                        logger.info(f"🆕 Nieuwe ETH whale: ${whale['value_usd']:,.0f}")
                        await callback(whale)
                
                # Cleanup seen hashes (houd laatste 1000)
                if len(self.seen_hashes) > 1000:
                    self.seen_hashes = set(list(self.seen_hashes)[-1000:])
                
                # Wacht tot volgende check
                await asyncio.sleep(check_interval)
                
            except Exception as e:
                logger.error(f"❌ Fout in whale monitoring loop: {e}")
                await asyncio.sleep(check_interval)


# ============================================================================
# TELEGRAM BOT INTEGRATIE
# ============================================================================

async def whale_alert_callback(whale_data: Dict, bot, channel_id: str):
    """
    Callback functie voor whale alerts naar Telegram.
    
    Args:
        whale_data: Whale transaction data
        bot: Telegram bot instance
        channel_id: Telegram channel ID
    """
    try:
        tracker = WhaleTracker()
        message = tracker.format_whale_alert(whale_data)
        
        await bot.send_message(
            chat_id=channel_id,
            text=message,
            parse_mode='Markdown'
        )
        
        logger.info(f"✅ Whale alert verzonden naar {channel_id}")
        
    except Exception as e:
        logger.error(f"❌ Fout bij versturen whale alert: {e}")


async def start_whale_monitoring_service(
    bot,
    channel_id: str,
    etherscan_key: Optional[str] = None,
    check_interval: int = 60
):
    """
    Start whale monitoring service als background task.
    
    Args:
        bot: Telegram bot instance
        channel_id: Telegram channel ID voor alerts
        etherscan_key: Etherscan API key (optioneel)
        check_interval: Check interval in seconden
    """
    tracker = WhaleTracker()
    
    # Wrapper callback die bot en channel_id meeneemt
    async def callback_wrapper(whale_data):
        await whale_alert_callback(whale_data, bot, channel_id)
    
    # Start monitoring
    await tracker.monitor_whales(
        callback=callback_wrapper,
        check_interval=check_interval,
        etherscan_key=etherscan_key
    )


# ============================================================================
# STANDALONE TEST
# ============================================================================

async def main():
    """Test whale tracking standalone."""
    tracker = WhaleTracker()
    
    print("=" * 60)
    print("🐋 ALCHEMIE WHALE TRACKER TEST")
    print("=" * 60)
    
    # Test BTC whales
    print("\n📊 Ophalen Bitcoin whales...")
    btc_whales = await tracker.get_btc_whale_transactions(
        min_value_usd=1_000_000,
        limit=5
    )
    
    if btc_whales:
        print(f"✅ {len(btc_whales)} BTC whales gevonden:\n")
        for whale in btc_whales:
            print(tracker.format_whale_alert(whale))
            print("-" * 60)
    else:
        print("⚠️  Geen BTC whales gevonden")
    
    # Test ETH whales
    print("\n📊 Ophalen Ethereum whales...")
    eth_whales = await tracker.get_eth_whale_transactions(
        min_value_usd=500_000,
        limit=5,
        etherscan_key=None  # Voeg je key toe voor betere resultaten
    )
    
    if eth_whales:
        print(f"✅ {len(eth_whales)} ETH whales gevonden:\n")
        for whale in eth_whales:
            print(tracker.format_whale_alert(whale))
            print("-" * 60)
    else:
        print("⚠️  Geen ETH whales gevonden")
    
    print("\n✅ Test compleet!")


if __name__ == "__main__":
    # Setup logging voor standalone test
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(main())
