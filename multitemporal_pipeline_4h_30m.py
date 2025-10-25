"""
Multitemporal Pipeline - 4H Primary / 30m Secondary
Primary: 4H para identificar setups
Secondary: 30m para confirmación y timing
"""

import argparse
import json
import os
import pandas as pd
from datetime import datetime, timedelta
from config import TradingConfig, ConfigLoader
from data_downloader import downloader
from technical_indicators import indicators


class MultitemporalPipeline4H30m:
    """Pipeline específico para 4H (primary) + 30m (secondary)"""
    
    def __init__(self, config = None):
        self.config = config if config is not None else ConfigLoader.default()
        self.primary_tf = "4h"
        self.secondary_tf = "30m"
    
    def download_multitemporal_data(self):
        """Download data for both 4H (primary) and 30m (secondary)"""
        
        print(f"📥 Downloading {self.primary_tf} data (primary - setup identification)...")
        df_primary = downloader.download_data(
            symbol=self.config.symbol,
            interval=self.primary_tf,
            limit=self.config.limit
        )
        
        print(f"📥 Downloading {self.secondary_tf} data (secondary - timing confirmation)...")
        # Need more 30m data to cover the same time period
        df_secondary = downloader.download_data(
            symbol=self.config.symbol,
            interval=self.secondary_tf,
            limit=self.config.limit * 8  # 8 velas 30m por cada 4H
        )
        
        return df_primary, df_secondary
    
    def sincronizar_primary_secondary(self, df_primary, df_secondary):
        """
        Sincronizar datos: replicar valores 4H (primary) para cada vela 30m (secondary)
        Mantenemos 30m como base temporal (más detalle)
        """
        
        print(f"🔄 Sincronizando {self.primary_tf} → {self.secondary_tf}...")
        
        # Calcular indicadores para ambos timeframes
        df_primary_with_indicators = indicators.calculate_all_indicators(df_primary)
        df_secondary_with_indicators = indicators.calculate_all_indicators(df_secondary)
        
        # Convertir a datetime
        df_secondary_with_indicators['timestamp'] = pd.to_datetime(df_secondary_with_indicators['date'])
        df_primary_with_indicators['timestamp'] = pd.to_datetime(df_primary_with_indicators['date'])
        
        # Añadir columnas de contexto primary (4H)
        context_columns = [
            'close_primary', 'high_primary', 'low_primary', 'open_primary',
            'ema10_primary', 'ema55_primary', 'ema200_primary',
            'smi_primary', 'adx_primary', 'atr_primary', 'rsi_primary'
        ]
        
        for col in context_columns:
            df_secondary_with_indicators[col] = None
        
        # Para cada vela secondary (30m), encontrar la primary (4H) correspondiente
        for idx, row_secondary in df_secondary_with_indicators.iterrows():
            timestamp_secondary = row_secondary['timestamp']
            
            # Encontrar vela primary (4H) que contiene esta secondary (30m)
            # Una vela 4H cubre de HH:00 a HH+4:00
            primary_mask = (
                (df_primary_with_indicators['timestamp'] <= timestamp_secondary) & 
                (timestamp_secondary < df_primary_with_indicators['timestamp'] + pd.Timedelta(hours=4))
            )
            
            if primary_mask.any():
                primary_idx = primary_mask.idxmax()
                primary_row = df_primary_with_indicators.loc[primary_idx]
                
                # Replicar todos los valores primary
                df_secondary_with_indicators.at[idx, 'close_primary'] = primary_row['close']
                df_secondary_with_indicators.at[idx, 'high_primary'] = primary_row['high']
                df_secondary_with_indicators.at[idx, 'low_primary'] = primary_row['low']
                df_secondary_with_indicators.at[idx, 'open_primary'] = primary_row['open']
                df_secondary_with_indicators.at[idx, 'ema10_primary'] = primary_row['ema10']
                df_secondary_with_indicators.at[idx, 'ema55_primary'] = primary_row['ema55']
                df_secondary_with_indicators.at[idx, 'ema200_primary'] = primary_row['ema200']
                df_secondary_with_indicators.at[idx, 'smi_primary'] = primary_row['smi']
                df_secondary_with_indicators.at[idx, 'adx_primary'] = primary_row['adx']
                df_secondary_with_indicators.at[idx, 'atr_primary'] = primary_row['atr']
                df_secondary_with_indicators.at[idx, 'rsi_primary'] = primary_row['rsi']
        
        # Limpiar columna temporal
        df_secondary_with_indicators.drop('timestamp', axis=1, inplace=True)
        
        return df_secondary_with_indicators
    
    def run_pipeline(self):
        """Execute complete multitemporal pipeline"""
        
        print("🚀 Starting Multitemporal Pipeline - 4H/30m")
        print(f"📊 Symbol: {self.config.symbol}")
        print(f"🎯 Primary TF: {self.primary_tf} (setup identification)")
        print(f"⏰ Secondary TF: {self.secondary_tf} (timing confirmation)")
        print(f"📈 Limit: {self.config.limit} {self.primary_tf} candles")
        print()
        
        # Step 1: Download both timeframes
        df_primary, df_secondary = self.download_multitemporal_data()
        
        if df_primary is None or df_secondary is None:
            print("❌ Failed to download data")
            return None
        
        # Step 2: Sincronizar primary → secondary
        df_final = self.sincronizar_primary_secondary(df_primary, df_secondary)
        
        # Step 3: Save results
        print("💾 Saving multitemporal dataset...")
        
        # Create exports directory if it doesn't exist
        os.makedirs("data/exports", exist_ok=True)
        
        # Save dataset
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/exports/multitemporal_4h_30m_{self.config.symbol}_{timestamp}.csv"
        df_final.to_csv(output_file, index=False)
        
        # Save config
        config_file = f"data/exports/multitemporal_4h_30m_config_{self.config.symbol}.json"
        with open(config_file, 'w') as f:
            json.dump({
                "symbol": self.config.symbol,
                "primary_tf": self.primary_tf,
                "secondary_tf": self.secondary_tf,
                "dataset_file": output_file,
                "description": f"{self.secondary_tf} data with {self.primary_tf} context for multitemporal labeling",
                "primary_columns": [col for col in df_final.columns if 'primary' in col],
                "secondary_columns": [col for col in df_final.columns if 'primary' not in col and col != 'date']
            }, f, indent=2)
        
        print(f"✅ Multitemporal dataset saved: {output_file}")
        print(f"📊 Dataset shape: {df_final.shape}")
        print(f"🎯 Primary ({self.primary_tf}) context columns:")
        primary_cols = [col for col in df_final.columns if 'primary' in col]
        for col in primary_cols:
            print(f"   - {col}")
        
        return df_final


def main():
    """Main function for 4H/30m multitemporal pipeline"""
    parser = argparse.ArgumentParser(description='Multitemporal Pipeline - 4H Primary / 30m Secondary')
    parser.add_argument('--symbol', default='BTCUSDT', help='Trading symbol')
    parser.add_argument('--limit', type=int, default=100, help='Number of 4H candles (primary)')
    
    args = parser.parse_args()
    
    # Create config
    config = TradingConfig(
        symbol=args.symbol,
        interval="4h",  # Primary timeframe
        limit=args.limit
    )
    
    # Run pipeline
    pipeline = MultitemporalPipeline4H30m(config)
    result = pipeline.run_pipeline()
    
    if result is not None:
        print(f"\n🎯 Next steps:")
        print(f"1. Update label_studio_config.xml for {args.symbol} {pipeline.primary_tf}/{pipeline.secondary_tf}")
        print(f"2. Start Label Studio: ./start_labeling_fixed.sh")
        print(f"3. Import: {result.shape[0]} {pipeline.secondary_tf} candles with {pipeline.primary_tf} context")
        print(f"4. Label using primary/secondary relationship labels")


if __name__ == "__main__":
    main()