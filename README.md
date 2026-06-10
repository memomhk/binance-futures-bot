# Binance Futures Trading Bot 🤖

An automated cryptocurrency futures trading bot for Binance that uses technical analysis to identify and execute trades.

## Features ✨

- **Technical Analysis**: RSI, MACD, EMA (20/50/200), Bollinger Bands
- **Risk Management**: Position sizing based on account risk percentage
- **Multiple Timeframes**: 1H, 4H, Daily
- **Automated Trading**: LONG and SHORT positions
- **Stop Loss & Take Profit**: Multi-level take profit orders
- **Leverage Trading**: Configurable leverage up to 125x
- **Volume Filtering**: Excludes low-liquidity coins ($50M+ minimum)
- **Trade Logging**: All trades logged to JSON file

## Installation 🚀

### Prerequisites
- Python 3.8+
- Binance account with API keys

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/memomhk/binance-futures-bot.git
cd binance-futures-bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create `.env` file**
```bash
cp .env.example .env
```

4. **Add your Binance API keys to `.env`**
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

## Configuration ⚙️

Edit the `.env` file to customize:

```env
# Trading Settings
RISK_PERCENTAGE=2              # % of account to risk per trade
LEVERAGE=5                     # Leverage (1-125x)
TRADING_SYMBOLS=BTCUSDT,ETHUSDT,BNBUSDT

# Stop Loss & Take Profit (%)
STOP_LOSS_PERCENT=2
TAKE_PROFIT_1_PERCENT=3
TAKE_PROFIT_2_PERCENT=6
TAKE_PROFIT_3_PERCENT=10
```

## How to Run 🏃

```bash
python main.py
```

The bot will:
1. Check your account balance
2. Scan all configured symbols
3. Analyze technical indicators
4. Execute trades when conditions are met
5. Log all trades to `trades_log.json`

## Trading Logic 📊

### Long Signal (Buy)
- EMA 20 > EMA 50 > EMA 200 (uptrend)
- Price above EMA 20
- RSI < 40 (not overbought)
- MACD > MACD Signal

### Short Signal (Sell)
- EMA 20 < EMA 50 < EMA 200 (downtrend)
- Price below EMA 20
- RSI > 60 (overbought)
- MACD < MACD Signal

**Trade executes when 3+ signals align**

## Risk Management ⚠️

- **Position Sizing**: Calculated to risk only X% per trade
- **Stop Loss**: Automatically placed below/above entry
- **Take Profit**: 3 levels to secure profits gradually
- **Volume Check**: Only trades coins with $50M+ daily volume
- **Leverage**: Configurable but use with caution

## Important Warnings ⚠️⚠️⚠️

1. **START SMALL**: Test with $100-$500 before trading larger amounts
2. **YOUR $13**: This is too small for Futures. Recommend $500+ minimum
3. **LEVERAGE RISK**: Higher leverage = higher risk of liquidation
4. **LOSSES POSSIBLE**: Past performance ≠ future results
5. **TEST FIRST**: Run in demo mode or with small capital
6. **API KEYS**: Keep your API keys secret and use IP whitelist

## File Structure 📁

```
binance-futures-bot/
├── main.py                 # Main bot
├── config.py              # Configuration
├── binance_client.py      # Binance API wrapper
├── indicators.py          # Technical indicators
├── trade_manager.py       # Trading logic
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
├── .gitignore             # Git ignore file
├── trades_log.json        # Trade history
└── README.md              # This file
```

## Trade Log 📝

All trades are logged in `trades_log.json`:

```json
{
  "timestamp": "2024-01-15T10:30:45.123456",
  "type": "LONG",
  "symbol": "BTCUSDT",
  "entry_price": 42500.00,
  "stop_loss": 41625.00,
  "quantity": 0.05
}
```

## Disclaimer 📋

This bot is provided as-is. Trading cryptocurrency is risky:
- You can lose your entire investment
- Bot bugs or market gaps can cause unexpected losses
- Past performance doesn't guarantee future results
- Always use risk management (stop losses, position sizing)
- Never risk money you can't afford to lose

## Support & Issues 🆘

- Check your API keys are correct
- Ensure sufficient balance for trading
- Monitor bot logs for errors
- Test thoroughly before live trading

## License 📄

This project is open source and available under the MIT License.

---

**Happy Trading! 📈** (But please trade responsibly!)
