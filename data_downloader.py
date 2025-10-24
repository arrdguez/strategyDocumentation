"""
Data Downloader Module - Modular data fetching from Binance
"""

import pandas as pd
import sys
import os

# Add current directory to path to import binanceExc
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from binanceExc import Binance


class DataDownloader:
    """Modular data downloader for trading data"""
    
    def __init__(self):
        self.exchange = Binance()
    
    def download_data(self, symbol='BTCUSDT', interval='4h', limit=1000):
        """
        Download OHLCV data from Binance
        
        Args:
            symbol: Trading pair symbol
            interval: Time interval
            limit: Number of candles to download
            
        Returns:
            DataFrame with OHLCV data
        """
        
        print(f"Downloading {symbol} {interval} data...")
        
        # Download data
        df = self.exchange.GetSymbolKlines(symbol, interval, limit=limit)
        
        if df.empty:
            print("Error: No data downloaded")
            return None
        
        print(f"Downloaded {len(df)} candles")
        
        # Format date for Label Studio
        df['date'] = pd.to_datetime(df['time'], unit='ms')
        df['date_str'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Select and order columns
        columns_for_export = [
            'date_str', 'open', 'high', 'low', 'close', 'volume'
        ]
        
        df_export = df[columns_for_export].copy()
        df_export = df_export.rename(columns={'date_str': 'date'})  # type: ignore
        
        # Remove any rows with NaN values
        df_export = df_export.dropna()
        
        print(f"Final dataset: {len(df_export)} rows")
        
        return df_export


# Singleton instance for easy access
downloader = DataDownloader()