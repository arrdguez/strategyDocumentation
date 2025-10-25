"""
Trading Data Pipeline - Multitemporal version
Generates dataset with 1H data + 4H context for labeling
"""

import argparse
import json
import os
import pandas as pd
from config import TradingConfig, ConfigLoader
from data_downloader import downloader
from technical_indicators import indicators


class MultitemporalPipeline:
    """Pipeline for generating multitemporal datasets"""
    
    def __init__(self, config = None):
        self.config = config if config is not None else ConfigLoader.default()
    
    def download_multitemporal_data(self):
        """Download data for both 1H and 4H timeframes"""
        
        print("📥 Downloading 1H data...")
        df_1h = downloader.download_data(
            symbol=self.config.symbol,
            interval="1h",
            limit=self.config.limit * 4  # More data for 1H
        )
        
        print("📥 Downloading 4H data...")
        df_4h = downloader.download_data(
            symbol=self.config.symbol,
            interval="4h", 
            limit=self.config.limit
        )
        
        return df_1h, df_4h
    
    def add_4h_context_to_1h(self, df_1h, df_4h):
        """Add 4H context information to 1H dataset"""
        
        print("🔄 Adding 4H context to 1H data...")
        
        # Calculate indicators for both timeframes
        df_1h_with_indicators = indicators.calculate_all_indicators(df_1h)
        df_4h_with_indicators = indicators.calculate_all_indicators(df_4h)
        
        # Create mapping from 1H timestamps to 4H periods
        df_1h_with_indicators['timestamp'] = pd.to_datetime(df_1h_with_indicators['date'])
        df_4h_with_indicators['timestamp'] = pd.to_datetime(df_4h_with_indicators['date'])
        
        # Add 4H context columns
        df_1h_with_indicators['tendencia_4h'] = False
        df_1h_with_indicators['smi_4h_activo'] = False
        df_1h_with_indicators['adx_4h_fuerte'] = False
        df_1h_with_indicators['ema_alignment_4h'] = False
        
        # For each 1H candle, find the corresponding 4H candle
        for idx, row in df_1h_with_indicators.iterrows():
            timestamp_1h = row['timestamp']
            
            # Find the 4H candle that contains this 1H timestamp
            mask_4h = (df_4h_with_indicators['timestamp'] <= timestamp_1h)
            if mask_4h.any():
                latest_4h_idx = mask_4h.idxmax()
                latest_4h = df_4h_with_indicators.loc[latest_4h_idx]
                
                # Add 4H context
                df_1h_with_indicators.at[idx, 'tendencia_4h'] = latest_4h['ema10'] > latest_4h['ema55']
                df_1h_with_indicators.at[idx, 'smi_4h_activo'] = latest_4h['smi'] > 0
                df_1h_with_indicators.at[idx, 'adx_4h_fuerte'] = latest_4h['adx'] > 25
                df_1h_with_indicators.at[idx, 'ema_alignment_4h'] = (
                    (latest_4h['ema10'] > latest_4h['ema55']) and 
                    (latest_4h['ema55'] > latest_4h['ema200'])
                )
                
                # Add raw 4H values for reference
                df_1h_with_indicators.at[idx, 'close_4h'] = latest_4h['close']
                df_1h_with_indicators.at[idx, 'ema10_4h'] = latest_4h['ema10']
                df_1h_with_indicators.at[idx, 'ema55_4h'] = latest_4h['ema55']
                df_1h_with_indicators.at[idx, 'smi_4h'] = latest_4h['smi']
                df_1h_with_indicators.at[idx, 'adx_4h'] = latest_4h['adx']
        
        # Clean up
        df_1h_with_indicators.drop('timestamp', axis=1, inplace=True)
        
        return df_1h_with_indicators
    
    def run_pipeline(self):
        """Execute complete multitemporal pipeline"""
        
        print("🚀 Starting Multitemporal Trading Pipeline")
        print(f"📊 Symbol: {self.config.symbol}")
        print(f"⏰ Primary TF: 1H (with 4H context)")
        print(f"📈 Limit: {self.config.limit} candles")
        print()
        
        # Step 1: Download both timeframes
        df_1h, df_4h = self.download_multitemporal_data()
        
        if df_1h is None or df_4h is None:
            print("❌ Failed to download data")
            return None
        
        # Step 2: Add 4H context to 1H data
        df_final = self.add_4h_context_to_1h(df_1h, df_4h)
        
        # Step 3: Save results
        print("💾 Saving multitemporal dataset...")
        
        # Create exports directory if it doesn't exist
        os.makedirs("data/exports", exist_ok=True)
        
        # Save dataset
        output_file = f"data/exports/multitemporal_dataset_{self.config.symbol}_1H.csv"
        df_final.to_csv(output_file, index=False)
        
        # Save config
        config_file = f"data/exports/multitemporal_config_{self.config.symbol}.json"
        with open(config_file, 'w') as f:
            json.dump({
                "symbol": self.config.symbol,
                "primary_tf": "1h",
                "context_tf": "4h", 
                "dataset_file": output_file,
                "description": "1H data with 4H context for multitemporal labeling"
            }, f, indent=2)
        
        print(f"✅ Multitemporal dataset saved: {output_file}")
        print(f"📊 Dataset shape: {df_final.shape}")
        print(f"📋 Columns with 4H context:")
        context_cols = [col for col in df_final.columns if '4h' in col.lower()]
        for col in context_cols:
            print(f"   - {col}")
        
        return df_final


def main():
    """Main function for multitemporal pipeline"""
    parser = argparse.ArgumentParser(description='Multitemporal Trading Pipeline')
    parser.add_argument('--symbol', default='BTCUSDT', help='Trading symbol')
    parser.add_argument('--limit', type=int, default=1000, help='Number of 1H candles')
    
    args = parser.parse_args()
    
    # Create config
    config = TradingConfig(
        symbol=args.symbol,
        interval="1h",  # Primary timeframe
        limit=args.limit
    )
    
    # Run pipeline
    pipeline = MultitemporalPipeline(config)
    result = pipeline.run_pipeline()
    
    if result is not None:
        print("\n🎯 Next steps:")
        print("1. Start Label Studio: ./start_labeling_fixed.sh")
        print("2. Import the multitemporal dataset")
        print("3. Use the new criteria-based labeling system")
        print("4. Label 50-100 candles to test the approach")


if __name__ == "__main__":
    main()