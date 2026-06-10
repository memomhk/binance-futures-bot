#!/usr/bin/env python3
"""
Binance Futures Trading Bot
Automated trading with technical analysis
"""

import time
import schedule
from datetime import datetime
import config
from binance_client import BinanceClient
from trade_manager import TradeManager

class TradingBot:
    """Main trading bot class"""
    
    def __init__(self):
        self.client = BinanceClient()
        self.trade_manager = TradeManager()
        self.running = True
    
    def check_market(self):
        """Check all trading symbols and execute trades"""
        print(f"\n{'='*60}")
        print(f"Market Check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        balance = self.client.get_account_balance()
        print(f"💰 Account Balance: ${balance:.2f}")
        
        # Check open positions
        positions = self.client.get_open_positions()
        print(f"📊 Open Positions: {len(positions)}")
        
        for symbol in config.TRADING_SYMBOLS:
            try:
                # Get 24h volume
                volume = self.client.get_24h_volume(symbol)
                print(f"\n🔍 Analyzing {symbol}")
                print(f"   24h Volume: ${volume:,.0f}")
                
                # Skip if volume too low
                if volume < 50000000:  # $50M minimum
                    print(f"   ⚠️  Volume too low, skipping...")
                    continue
                
                # Analyze and trade
                self.trade_manager.analyze_and_trade(symbol)
            
            except Exception as e:
                print(f"❌ Error analyzing {symbol}: {e}")
    
    def schedule_tasks(self):
        """Schedule trading checks"""
        # Check market every hour
        schedule.every(1).hours.do(self.check_market)
        
        print("✅ Bot started successfully!")
        print(f"Trading Symbols: {', '.join(config.TRADING_SYMBOLS)}")
        print(f"Risk per trade: {config.RISK_PERCENTAGE}%")
        print(f"Leverage: {config.LEVERAGE}x")
        print(f"Stop Loss: {config.STOP_LOSS_PERCENT}%")
        print(f"Take Profit Levels: {config.TAKE_PROFIT_1_PERCENT}%, {config.TAKE_PROFIT_2_PERCENT}%, {config.TAKE_PROFIT_3_PERCENT}%")
    
    def run(self):
        """Run the bot"""
        try:
            self.schedule_tasks()
            
            # First check
            self.check_market()
            
            # Keep bot running
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        except KeyboardInterrupt:
            print("\n\n⛔ Bot stopped by user")
            self.running = False
        
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            self.running = False

if __name__ == "__main__":
    bot = TradingBot()
    bot.run()
