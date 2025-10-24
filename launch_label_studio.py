#!/usr/bin/env python3
"""
Launch Label Studio for trading data labeling
"""

import subprocess
import os
import sys

def launch_label_studio():
    """Launch Label Studio with trading data configuration"""
    
    print("Setting up Label Studio for trading data labeling...")
    
    # Check if data file exists
    if not os.path.exists('trading_data_labeling.csv'):
        print("Error: trading_data_labeling.csv not found. Run download_trading_data.py first.")
        return
    
    # Check if config file exists
    if not os.path.exists('label_studio_config.xml'):
        print("Error: label_studio_config.xml not found.")
        return
    
    print("✅ All files ready for labeling!")
    print("\nTo start Label Studio:")
    print("1. Activate virtual environment:")
    print("   source label_studio_env/bin/activate")
    print("2. Launch Label Studio:")
    print("   label-studio")
    print("\nThen in your browser:")
    print("1. Open http://localhost:8080")
    print("2. Create new project")
    print("3. Import configuration: label_studio_config.xml")
    print("4. Upload data: trading_data_labeling.csv")
    print("5. Start labeling trading patterns!")

def create_quick_start_guide():
    """Create a quick start guide for labeling"""
    
    guide = """
# TRADINGLATINO PATTERN LABELING - QUICK START GUIDE

## Setup Instructions:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download data**:
   ```bash
   python3 download_trading_data.py
   ```

3. **Launch Label Studio**:
   ```bash
   python3 launch_label_studio.py
   ```

4. **Access Label Studio**:
   - Open http://localhost:8080
   - Create new project
   - Import configuration: label_studio_config.xml
   - Upload data: trading_data_labeling.csv

## Labeling Guidelines:

### Wave Structure Patterns:
- **ONDA_0_SUELO**: Market bottom before impulse
- **ONDA_1_IMPULSO**: First strong upward movement  
- **ONDA_2_ENTRADA**: Correction for entry opportunity
- **ONDA_3_TENDENCIA**: Main trend movement
- **ONDA_4_CORRECCION**: Correction before exit
- **ONDA_5_SALIDA**: Final movement completion

### Entry Patterns:
- **ENTRADA_LONG_ROMBRE_APOYA**: Breakout with EMA support
- **ENTRADA_SHORT_LATERAL_FUERZA_BAJISTA**: Sideways with bearish strength
- **ENTRADA_LONG_EMA10_EMA55**: EMA crossover bullish
- **ENTRADA_SHORT_EMA10_EMA55**: EMA crossover bearish

### Exit Patterns:
- **SALIDA_QUIEBRE_ESTRUCTURA**: Structure break
- **SALIDA_VOLUMEN_ANORMAL**: Abnormal volume
- **SALIDA_OBJETIVO_ALCANZADO**: Target reached
- **SALIDA_STOP_LOSS**: Stop loss triggered

### Market Conditions:
- **TENDENCIA_ALCISTA/BAJISTA**: Bullish/Bearish trend
- **LATERAL_FUERZA_ALTA/BAJA**: Sideways with high/low strength

## Technical Indicators:
- **EMA10/EMA55**: Moving averages for trend direction
- **SQUEEZE_MOMENTUM**: Compression/expansion periods
- **ADX**: Trend strength indicator

Start with labeling 50-100 data points to validate the schema!
"""
    
    with open('Doc/LABELING_GUIDE.md', 'w') as f:
        f.write(guide)
    
    print("Quick start guide created: LABELING_GUIDE.md")

if __name__ == "__main__":
    create_quick_start_guide()
    print("\nTo launch Label Studio, run:")
    print("label-studio start trading_labeling_project --init --no-browser")
    print("\nOr use the virtual environment:")
    print("source label_studio_env/bin/activate && label-studio start trading_labeling_project --init --no-browser")