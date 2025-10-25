"""
Test script for multitemporal pipeline
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from trading_pipeline_multitemporal import MultitemporalPipeline
# Temporary import fix - we'll test directly
from config import TradingConfig

def test_multitemporal():
    """Test the multitemporal pipeline"""
    
    print("🧪 Testing Multitemporal Pipeline...")
    
    # Create config for testing
    config = TradingConfig(
        symbol="BTCUSDT",
        interval="1h",  # Primary timeframe
        limit=100  # Small dataset for testing
    )
    
    # Run pipeline
    pipeline = MultitemporalPipeline(config)
    result = pipeline.run_pipeline()
    
    if result is not None:
        print(f"\n✅ Test successful!")
        print(f"📊 Dataset shape: {result.shape}")
        print(f"📋 Columns: {list(result.columns)}")
        
        # Show some 4H context columns
        context_cols = [col for col in result.columns if '4h' in col.lower()]
        print(f"\n🔍 4H Context columns:")
        for col in context_cols:
            print(f"   - {col}")
            
        # Show sample data
        print(f"\n📈 Sample data (first 5 rows):")
        print(result[['date', 'close', 'ema10', 'ema55', 'tendencia_4h', 'smi_4h_activo']].head())
        
    else:
        print("❌ Test failed!")

if __name__ == "__main__":
    test_multitemporal()