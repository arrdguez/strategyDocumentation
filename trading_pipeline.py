"""
Trading Data Pipeline - Main orchestrator for data processing
"""

import argparse
import json
import os
from config import TradingConfig, ConfigLoader
from data_downloader import downloader
from technical_indicators import indicators


class TradingPipeline:
    """Main pipeline for trading data processing"""
    
    def __init__(self, config: TradingConfig = None):
        self.config = config or ConfigLoader.default()
    
    def run_pipeline(self):
        """Execute complete data processing pipeline"""
        
        print("🚀 Starting Trading Data Pipeline")
        print(f"📊 Symbol: {self.config.symbol}")
        print(f"⏰ Interval: {self.config.interval}")
        print(f"📈 Limit: {self.config.limit}")
        print()
        
        # Step 1: Download data
        print("1️⃣ Downloading market data...")
        df = downloader.download_data(
            symbol=self.config.symbol,
            interval=self.config.interval,
            limit=self.config.limit
        )
        
        if df is None:
            print("❌ Failed to download data")
            return None
        
        # Step 2: Calculate technical indicators
        print("2️⃣ Calculating technical indicators...")
        df_with_indicators = indicators.calculate_all_indicators(
            df,
            ema_periods=self.config.ema_periods,
            adx_period=self.config.adx_period,
            atr_period=self.config.atr_period,
            smi_period=self.config.smi_period
        )
        
        # Step 3: Save results
        print("3️⃣ Saving results...")
        output_path = self._save_results(df_with_indicators)
        
        # Step 4: Print summary
        self._print_summary(df_with_indicators, output_path)
        
        print("✅ Pipeline completed successfully!")
        
        return df_with_indicators
    
    def _save_results(self, df):
        """Save processed data to organized directory structure"""
        import os
        
        # Ensure directories exist
        os.makedirs(self.config.output_dir, exist_ok=True)
        os.makedirs(self.config.raw_dir, exist_ok=True)
        
        # Generate automatic filename
        filename = self.config.get_output_filename()
        output_path = os.path.join(self.config.output_dir, filename)
        
        # Save processed data
        df.to_csv(output_path, index=False)
        print(f"💾 Data saved to: {output_path}")
        
        # Also save a copy in exports for Label Studio
        exports_path = os.path.join(self.config.exports_dir, "latest_dataset.csv")
        df.to_csv(exports_path, index=False)
        print(f"📤 Export copy for Label Studio: {exports_path}")
        
        return output_path
    
    def _print_summary(self, df, output_path):
        """Print pipeline summary"""
        print("\n📊 PIPELINE SUMMARY:")
        print(f"   • Dataset: {output_path}")
        print(f"   • Total candles: {len(df)}")
        print(f"   • Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"   • ADX > 25 (Strong trend): {(df['adx'] > 25).sum()}")
        print(f"   • Indicators calculated: EMA{self.config.ema_periods}, ADX, ATR, SMI")


def main():
    """Main function with command line interface"""
    
    parser = argparse.ArgumentParser(description='Trading Data Pipeline')
    parser.add_argument('--symbol', default='BTCUSDT', help='Trading symbol (default: BTCUSDT)')
    parser.add_argument('--interval', default='4h', help='Time interval (default: 4h)')
    parser.add_argument('--limit', type=int, default=1000, help='Number of candles (default: 1000)')
    parser.add_argument('--output-dir', default='data/processed', help='Output directory (default: data/processed)')
    parser.add_argument('--config-file', help='JSON configuration file')
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config_file and os.path.exists(args.config_file):
        with open(args.config_file, 'r') as f:
            config_dict = json.load(f)
        config = ConfigLoader.from_dict(config_dict)
    else:
        config = TradingConfig(
            symbol=args.symbol,
            interval=args.interval,
            limit=args.limit,
            output_dir=args.output_dir
        )
    
    # Run pipeline
    pipeline = TradingPipeline(config)
    pipeline.run_pipeline()


if __name__ == "__main__":
    main()