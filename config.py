import os
from dotenv import load_dotenv

load_dotenv()

# Binance API Configuration
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')

# Trading Settings
RISK_PERCENTAGE = float(os.getenv('RISK_PERCENTAGE', 2))
LEVERAGE = int(os.getenv('LEVERAGE', 5))
TRADING_SYMBOLS = os.getenv('TRADING_SYMBOLS', 'BTCUSDT,ETHUSDT,BNBUSDT').split(',')

# Stop Loss & Take Profit
STOP_LOSS_PERCENT = float(os.getenv('STOP_LOSS_PERCENT', 2))
TAKE_PROFIT_1_PERCENT = float(os.getenv('TAKE_PROFIT_1_PERCENT', 3))
TAKE_PROFIT_2_PERCENT = float(os.getenv('TAKE_PROFIT_2_PERCENT', 6))
TAKE_PROFIT_3_PERCENT = float(os.getenv('TAKE_PROFIT_3_PERCENT', 10))

# Technical Indicators Settings
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

EMA_20 = 20
EMA_50 = 50
EMA_200 = 200

# Timeframes
TIMEFRAME = '1h'  # 1h, 4h, 1d
