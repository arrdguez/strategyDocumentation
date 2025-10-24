#!/usr/bin/env python3
"""
Download trading data and calculate technical indicators for Label Studio
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add current directory to path to import binanceExc
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from binanceExc import Binance

def calculate_ema(data, period):
    """Calculate Exponential Moving Average"""
    return data['close'].ewm(span=period, adjust=False).mean()

def calculate_adx(data, period=14):
    """Calculate Average Directional Index"""
    # Calculate True Range
    data['tr'] = np.maximum(
        data['high'] - data['low'],
        np.maximum(
            abs(data['high'] - data['close'].shift(1)),
            abs(data['low'] - data['close'].shift(1))
        )
    )
    
    # Calculate +DM and -DM
    data['plus_dm'] = np.where(
        (data['high'] - data['high'].shift(1)) > (data['low'].shift(1) - data['low']),
        np.maximum(data['high'] - data['high'].shift(1), 0),
        0
    )
    
    data['minus_dm'] = np.where(
        (data['low'].shift(1) - data['low']) > (data['high'] - data['high'].shift(1)),
        np.maximum(data['low'].shift(1) - data['low'], 0),
        0
    )
    
    # Calculate smoothed values
    data['tr_smooth'] = data['tr'].ewm(span=period, adjust=False).mean()
    data['plus_dm_smooth'] = data['plus_dm'].ewm(span=period, adjust=False).mean()
    data['minus_dm_smooth'] = data['minus_dm'].ewm(span=period, adjust=False).mean()
    
    # Calculate +DI and -DI
    data['plus_di'] = 100 * (data['plus_dm_smooth'] / data['tr_smooth'])
    data['minus_di'] = 100 * (data['minus_dm_smooth'] / data['tr_smooth'])
    
    # Calculate ADX
    data['dx'] = 100 * abs(data['plus_di'] - data['minus_di']) / (data['plus_di'] + data['minus_di'])
    data['adx'] = data['dx'].ewm(span=period, adjust=False).mean()
    
    return data['adx']

def calculate_squeeze_momentum(data, bb_period=20, bb_std=2, kc_period=20, kc_mult=1.5):
    """Calculate Squeeze Momentum Indicator"""
    # Bollinger Bands
    data['bb_middle'] = data['close'].rolling(window=bb_period).mean()
    data['bb_std'] = data['close'].rolling(window=bb_period).std()
    data['bb_upper'] = data['bb_middle'] + (bb_std * data['bb_std'])
    data['bb_lower'] = data['bb_middle'] - (bb_std * data['bb_std'])
    
    # Keltner Channel
    data['kc_middle'] = data['close'].rolling(window=kc_period).mean()
    data['kc_atr'] = (data['high'] - data['low']).rolling(window=kc_period).mean()
    data['kc_upper'] = data['kc_middle'] + (kc_mult * data['kc_atr'])
    data['kc_lower'] = data['kc_middle'] - (kc_mult * data['kc_atr'])
    
    # Squeeze condition
    data['squeeze_on'] = (data['bb_lower'] > data['kc_lower']) & (data['bb_upper'] < data['kc_upper'])
    data['squeeze_off'] = (data['bb_lower'] < data['kc_lower']) & (data['bb_upper'] > data['kc_upper'])
    
    # Momentum (simplified)
    data['momentum'] = data['close'] - data['close'].shift(4)
    
    # Squeeze Momentum value
    data['squeeze_momentum'] = np.where(
        data['squeeze_on'], 
        0,  # No momentum during squeeze
        data['momentum']
    )
    
    return data['squeeze_momentum']

def download_and_prepare_data(symbol='BTCUSDT', interval='4h', limit=1000):
    """Download data and calculate all technical indicators"""
    
    print(f"Downloading {symbol} {interval} data...")
    
    # Initialize Binance client
    exchange = Binance()
    
    # Download data
    df = exchange.GetSymbolKlines(symbol, interval, limit=limit)
    
    if df.empty:
        print("Error: No data downloaded")
        return None
    
    print(f"Downloaded {len(df)} candles")
    
    # Calculate technical indicators
    print("Calculating technical indicators...")
    
    # EMAs
    df['ema10'] = calculate_ema(df, 10)
    df['ema55'] = calculate_ema(df, 55)
    
    # ADX
    df['adx'] = calculate_adx(df)
    
    # Squeeze Momentum
    df['squeeze_momentum'] = calculate_squeeze_momentum(df)
    
    # Additional useful calculations
    df['ema_cross'] = np.where(df['ema10'] > df['ema55'], 1, -1)
    df['price_vs_ema55'] = (df['close'] - df['ema55']) / df['ema55'] * 100
    
    # Format date for Label Studio
    df['date'] = pd.to_datetime(df['time'], unit='ms')
    df['date_str'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Select and order columns for Label Studio
    columns_for_export = [
        'date_str', 'open', 'high', 'low', 'close', 'volume',
        'ema10', 'ema55', 'squeeze_momentum', 'adx',
        'ema_cross', 'price_vs_ema55'
    ]
    
    df_export = df[columns_for_export].copy()
    df_export = df_export.rename(columns={'date_str': 'date'})
    
    # Remove any rows with NaN values
    df_export = df_export.dropna()
    
    print(f"Final dataset: {len(df_export)} rows with all indicators")
    
    return df_export

def save_data_for_label_studio(df, filename='trading_data_labeling.csv'):
    """Save data in format suitable for Label Studio"""
    
    if df is None:
        print("No data to save")
        return
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    
    # Print sample
    print("\nSample data:")
    print(df.head())
    
    # Print statistics
    print(f"\nDataset statistics:")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total candles: {len(df)}")
    print(f"EMA cross bullish: {(df['ema_cross'] == 1).sum()}")
    print(f"EMA cross bearish: {(df['ema_cross'] == -1).sum()}")

if __name__ == "__main__":
    # Download and prepare data
    df = download_and_prepare_data(
        symbol='BTCUSDT',
        interval='4h', 
        limit=1000
    )
    
    # Save for Label Studio
    if df is not None:
        save_data_for_label_studio(df, 'trading_data_labeling.csv')