import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
import config

class BinanceClient:
    """Handle all Binance API interactions"""
    
    def __init__(self):
        self.client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET)
    
    def get_klines(self, symbol, interval, limit=100):
        """
        Get candlestick data from Binance
        Returns: DataFrame with OHLCV data
        """
        try:
            klines = self.client.futures_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            df = pd.DataFrame(klines, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Convert to numeric
            df['open'] = pd.to_numeric(df['open'])
            df['high'] = pd.to_numeric(df['high'])
            df['low'] = pd.to_numeric(df['low'])
            df['close'] = pd.to_numeric(df['close'])
            df['volume'] = pd.to_numeric(df['volume'])
            
            return df
        
        except BinanceAPIException as e:
            print(f"Binance API Error: {e}")
            return None
    
    def get_account_balance(self):
        """Get current account balance"""
        try:
            account = self.client.futures_account()
            total_balance = float(account['totalWalletBalance'])
            return total_balance
        except BinanceAPIException as e:
            print(f"Error getting account balance: {e}")
            return 0
    
    def get_open_positions(self):
        """Get all open positions"""
        try:
            positions = self.client.futures_position_information()
            open_positions = [p for p in positions if float(p['positionAmt']) != 0]
            return open_positions
        except BinanceAPIException as e:
            print(f"Error getting open positions: {e}")
            return []
    
    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """
        Place a futures order
        side: 'BUY' or 'SELL'
        order_type: 'LIMIT' or 'MARKET'
        """
        try:
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=quantity
                )
            else:  # LIMIT
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type='LIMIT',
                    timeInForce='GTC',
                    quantity=quantity,
                    price=price
                )
            
            return order
        except BinanceAPIException as e:
            print(f"Error placing order: {e}")
            return None
    
    def place_stop_loss(self, symbol, side, quantity, stop_price):
        """Place a stop loss order"""
        try:
            opposite_side = 'SELL' if side == 'BUY' else 'BUY'
            order = self.client.futures_create_order(
                symbol=symbol,
                side=opposite_side,
                type='STOP_MARKET',
                stopPrice=stop_price,
                quantity=quantity,
                timeInForce='GTC'
            )
            return order
        except BinanceAPIException as e:
            print(f"Error placing stop loss: {e}")
            return None
    
    def place_take_profit(self, symbol, side, quantity, take_profit_price):
        """Place a take profit order"""
        try:
            opposite_side = 'SELL' if side == 'BUY' else 'BUY'
            order = self.client.futures_create_order(
                symbol=symbol,
                side=opposite_side,
                type='TAKE_PROFIT_MARKET',
                stopPrice=take_profit_price,
                quantity=quantity,
                timeInForce='GTC'
            )
            return order
        except BinanceAPIException as e:
            print(f"Error placing take profit: {e}")
            return None
    
    def cancel_order(self, symbol, order_id):
        """Cancel an open order"""
        try:
            self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            return True
        except BinanceAPIException as e:
            print(f"Error canceling order: {e}")
            return False
    
    def set_leverage(self, symbol, leverage):
        """Set leverage for trading"""
        try:
            self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            print(f"Leverage set to {leverage}x for {symbol}")
            return True
        except BinanceAPIException as e:
            print(f"Error setting leverage: {e}")
            return False
    
    def get_24h_volume(self, symbol):
        """Get 24h trading volume"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            volume = float(ticker['quoteVolume'])
            return volume
        except BinanceAPIException as e:
            print(f"Error getting volume: {e}")
            return 0
