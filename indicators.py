import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator, MACD
from ta.trend import EMAIndicator

class TechnicalIndicators:
    """Calculate technical indicators for trading analysis"""
    
    @staticmethod
    def calculate_rsi(data, period=14):
        """Calculate Relative Strength Index"""
        rsi = RSIIndicator(close=data['close'], window=period)
        return rsi.rsi()
    
    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        macd = MACD(close=data['close'], window_fast=fast, window_slow=slow, window_sign=signal)
        return macd.macd(), macd.macd_signal(), macd.macd_diff()
    
    @staticmethod
    def calculate_ema(data, period):
        """Calculate Exponential Moving Average"""
        ema = EMAIndicator(close=data['close'], window=period)
        return ema.ema_indicator()
    
    @staticmethod
    def calculate_bollinger_bands(data, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        sma = data['close'].rolling(window=period).mean()
        std = data['close'].rolling(window=period).std()
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        return upper, sma, lower
    
    @staticmethod
    def analyze_trend(data, rsi, macd, macd_signal, ema_20, ema_50, ema_200):
        """
        Analyze market trend based on multiple indicators
        Returns: 'LONG', 'SHORT', or 'NEUTRAL'
        """
        current_price = data['close'].iloc[-1]
        current_rsi = rsi.iloc[-1]
        current_macd = macd.iloc[-1]
        current_macd_signal = macd_signal.iloc[-1]
        current_ema_20 = ema_20.iloc[-1]
        current_ema_50 = ema_50.iloc[-1]
        current_ema_200 = ema_200.iloc[-1]
        
        # Count bullish signals for LONG
        long_signals = 0
        
        # EMA alignment (uptrend)
        if current_ema_20 > current_ema_50 > current_ema_200:
            long_signals += 1
        
        # Price above EMA 20
        if current_price > current_ema_20:
            long_signals += 1
        
        # RSI oversold (bullish)
        if current_rsi < 40:
            long_signals += 1
        
        # MACD bullish crossover
        if current_macd > current_macd_signal:
            long_signals += 1
        
        # Count bearish signals for SHORT
        short_signals = 0
        
        # EMA alignment (downtrend)
        if current_ema_20 < current_ema_50 < current_ema_200:
            short_signals += 1
        
        # Price below EMA 20
        if current_price < current_ema_20:
            short_signals += 1
        
        # RSI overbought (bearish)
        if current_rsi > 60:
            short_signals += 1
        
        # MACD bearish crossover
        if current_macd < current_macd_signal:
            short_signals += 1
        
        # Decision logic
        if long_signals >= 3:
            return 'LONG'
        elif short_signals >= 3:
            return 'SHORT'
        else:
            return 'NEUTRAL'
    
    @staticmethod
    def get_signal_strength(long_signals, short_signals):
        """Get confidence level (0-100)"""
        max_signals = 4
        if long_signals > short_signals:
            return int((long_signals / max_signals) * 100)
        elif short_signals > long_signals:
            return int((short_signals / max_signals) * 100)
        else:
            return 0
