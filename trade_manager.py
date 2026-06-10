import json
from datetime import datetime
import config
from binance_client import BinanceClient
from indicators import TechnicalIndicators

class TradeManager:
    """Manage trading logic and execution"""
    
    def __init__(self):
        self.client = BinanceClient()
        self.trades_log = 'trades_log.json'
        self.active_trades = {}
    
    def calculate_position_size(self, balance, risk_percent, entry_price, stop_loss_price):
        """
        Calculate position size based on risk management
        Works with ANY balance (even $1)
        """
        try:
            # Calculate risk amount
            risk_amount = balance * (risk_percent / 100)
            price_difference = abs(entry_price - stop_loss_price)
            
            if price_difference == 0:
                return 0
            
            # Calculate position size
            position_size = risk_amount / price_difference
            
            # Ensure minimum viable size for Binance
            # Binance minimum is usually 0.001 or $10 notional
            min_notional = 10  # $10 minimum
            notional_value = position_size * entry_price
            
            if notional_value < min_notional:
                # Use minimum if balance is very small
                position_size = min_notional / entry_price
            
            return position_size
        
        except Exception as e:
            print(f"Error calculating position size: {e}")
            return 0
    
    def execute_long_trade(self, symbol, entry_price, stop_loss_price):
        """Execute a LONG (BUY) trade - works with any balance"""
        try:
            balance = self.client.get_account_balance()
            
            # Calculate position size based on actual balance
            quantity = self.calculate_position_size(
                balance,
                config.RISK_PERCENTAGE,
                entry_price,
                stop_loss_price
            )
            
            if quantity == 0:
                print(f"⚠️  Position size too small for {symbol}")
                return False
            
            print(f"💰 Account Balance: ${balance:.2f}")
            print(f"📊 Position Size: {quantity:.8f} {symbol.replace('USDT', '')}")
            print(f"💵 Position Value: ${quantity * entry_price:.2f}")
            
            # Set leverage
            self.client.set_leverage(symbol, config.LEVERAGE)
            
            # Place BUY order
            order = self.client.place_order(
                symbol=symbol,
                side='BUY',
                order_type='MARKET',
                quantity=round(quantity, 8)
            )
            
            if order:
                print(f"✅ LONG Trade Opened: {symbol} @ ${entry_price:.2f}")
                
                # Place stop loss
                self.client.place_stop_loss(
                    symbol=symbol,
                    side='BUY',
                    quantity=round(quantity, 8),
                    stop_price=stop_loss_price
                )
                
                # Place take profit orders (split into 3 parts)
                tp1 = entry_price + (entry_price * config.TAKE_PROFIT_1_PERCENT / 100)
                tp2 = entry_price + (entry_price * config.TAKE_PROFIT_2_PERCENT / 100)
                tp3 = entry_price + (entry_price * config.TAKE_PROFIT_3_PERCENT / 100)
                
                qty_per_tp = round(quantity / 3, 8)
                
                self.client.place_take_profit(symbol, 'BUY', qty_per_tp, tp1)
                self.client.place_take_profit(symbol, 'BUY', qty_per_tp, tp2)
                self.client.place_take_profit(symbol, 'BUY', qty_per_tp, tp3)
                
                self.log_trade('LONG', symbol, entry_price, stop_loss_price, quantity)
                return True
            
            return False
        
        except Exception as e:
            print(f"❌ Error executing LONG trade: {e}")
            return False
    
    def execute_short_trade(self, symbol, entry_price, stop_loss_price):
        """Execute a SHORT (SELL) trade - works with any balance"""
        try:
            balance = self.client.get_account_balance()
            
            # Calculate position size based on actual balance
            quantity = self.calculate_position_size(
                balance,
                config.RISK_PERCENTAGE,
                entry_price,
                stop_loss_price
            )
            
            if quantity == 0:
                print(f"⚠️  Position size too small for {symbol}")
                return False
            
            print(f"💰 Account Balance: ${balance:.2f}")
            print(f"📊 Position Size: {quantity:.8f} {symbol.replace('USDT', '')}")
            print(f"💵 Position Value: ${quantity * entry_price:.2f}")
            
            # Set leverage
            self.client.set_leverage(symbol, config.LEVERAGE)
            
            # Place SELL order
            order = self.client.place_order(
                symbol=symbol,
                side='SELL',
                order_type='MARKET',
                quantity=round(quantity, 8)
            )
            
            if order:
                print(f"✅ SHORT Trade Opened: {symbol} @ ${entry_price:.2f}")
                
                # Place stop loss
                self.client.place_stop_loss(
                    symbol=symbol,
                    side='SELL',
                    quantity=round(quantity, 8),
                    stop_price=stop_loss_price
                )
                
                # Place take profit orders (split into 3 parts)
                tp1 = entry_price - (entry_price * config.TAKE_PROFIT_1_PERCENT / 100)
                tp2 = entry_price - (entry_price * config.TAKE_PROFIT_2_PERCENT / 100)
                tp3 = entry_price - (entry_price * config.TAKE_PROFIT_3_PERCENT / 100)
                
                qty_per_tp = round(quantity / 3, 8)
                
                self.client.place_take_profit(symbol, 'SELL', qty_per_tp, tp1)
                self.client.place_take_profit(symbol, 'SELL', qty_per_tp, tp2)
                self.client.place_take_profit(symbol, 'SELL', qty_per_tp, tp3)
                
                self.log_trade('SHORT', symbol, entry_price, stop_loss_price, quantity)
                return True
            
            return False
        
        except Exception as e:
            print(f"❌ Error executing SHORT trade: {e}")
            return False
    
    def log_trade(self, trade_type, symbol, entry, stop_loss, quantity):
        """Log trade details to file"""
        try:
            trade_data = {
                'timestamp': datetime.now().isoformat(),
                'type': trade_type,
                'symbol': symbol,
                'entry_price': entry,
                'stop_loss': stop_loss,
                'quantity': quantity,
                'position_value': quantity * entry
            }
            
            with open(self.trades_log, 'a') as f:
                json.dump(trade_data, f)
                f.write('\n')
            
            print(f"📝 Trade logged to {self.trades_log}")
        
        except Exception as e:
            print(f"⚠️  Error logging trade: {e}")
    
    def analyze_and_trade(self, symbol):
        """Analyze symbol and execute trade if conditions are met"""
        try:
            # Get klines data
            df = self.client.get_klines(symbol, config.TIMEFRAME, limit=100)
            
            if df is None or df.empty:
                return False
            
            # Calculate indicators
            rsi = TechnicalIndicators.calculate_rsi(df)
            macd, macd_signal, macd_diff = TechnicalIndicators.calculate_macd(df)
            ema_20 = TechnicalIndicators.calculate_ema(df, config.EMA_20)
            ema_50 = TechnicalIndicators.calculate_ema(df, config.EMA_50)
            ema_200 = TechnicalIndicators.calculate_ema(df, config.EMA_200)
            
            # Analyze trend
            signal = TechnicalIndicators.analyze_trend(df, rsi, macd, macd_signal, ema_20, ema_50, ema_200)
            
            current_price = float(df['close'].iloc[-1])
            
            if signal == 'LONG':
                stop_loss = current_price * (1 - config.STOP_LOSS_PERCENT / 100)
                self.execute_long_trade(symbol, current_price, stop_loss)
                return True
            
            elif signal == 'SHORT':
                stop_loss = current_price * (1 + config.STOP_LOSS_PERCENT / 100)
                self.execute_short_trade(symbol, current_price, stop_loss)
                return True
            
            return False
        
        except Exception as e:
            print(f"❌ Error analyzing {symbol}: {e}")
            return False
