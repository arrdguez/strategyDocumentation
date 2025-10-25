"""
Test script for 4H/30m multitemporal pipeline
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from multitemporal_pipeline_4h_30m import MultitemporalPipeline4H30m
from config import TradingConfig

def test_4h_30m():
    """Test the 4H/30m multitemporal pipeline"""
    
    print("🧪 Testing 4H/30m Multitemporal Pipeline...")
    
    # Create config for testing
    config = TradingConfig(
        symbol="BTCUSDT",
        interval="4h",  # Primary timeframe
        limit=10  # Small dataset for testing
    )
    
    # Run pipeline
    pipeline = MultitemporalPipeline4H30m(config)
    result = pipeline.run_pipeline()
    
    if result is not None:
        print(f"\n✅ Test successful!")
        print(f"📊 Dataset shape: {result.shape}")
        print(f"🎯 Primary (4H) context columns:")
        primary_cols = [col for col in result.columns if 'primary' in col]
        for col in primary_cols:
            print(f"   - {col}")
            
        # Show sample data
        print(f"\n📈 Sample data (first 3 rows):")
        sample_cols = ['date', 'close', 'ema10', 'close_primary', 'ema10_primary']
        available_cols = [col for col in sample_cols if col in result.columns]
        print(result[available_cols].head(3))
        
        print(f"\n🔍 Verificando sincronización:")
        # Check if primary values are consistent within 4H periods
        unique_primary = result[['close_primary', 'ema10_primary']].drop_duplicates()
        print(f"   Unique primary combinations: {len(unique_primary)}")
        print(f"   Expected: ~{config.limit} (one per 4H candle)")
        
    else:
        print("❌ Test failed!")

if __name__ == "__main__":
    test_4h_30m()