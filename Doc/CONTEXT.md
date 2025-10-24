# 🏗️ Trading Data Labeling System - Contexto del Proyecto

## 📋 Resumen del Sistema

Sistema modular para descargar datos de trading de Binance, calcular indicadores técnicos y preparar datasets para etiquetado en Label Studio.

## 🏛️ Arquitectura Modular

### **Módulos Principales:**

1. **`config.py`** - Configuración centralizada con `TradingConfig`
2. **`technical_indicators.py`** - Cálculo de indicadores (EMA, ADX, ATR, SMI, Squeeze Momentum)
3. **`data_downloader.py`** - Descarga modular de datos de Binance
4. **`trading_pipeline.py`** - Orquestador principal del pipeline
5. **`SMI.py`** - Implementaciones originales de indicadores (mantenido para compatibilidad)
6. **`binanceExc.py`** - Cliente de Binance API

## 🚀 Uso del Sistema

### **Comandos Principales:**

```bash
# Pipeline completo con parámetros CLI
python trading_pipeline.py --symbol ETHUSDT --interval 1h --limit 500

# Pipeline con archivo de configuración
python trading_pipeline.py --config-file config_btc_4h.json

# Pipeline con configuración por defecto
python trading_pipeline.py
```

### **Scripts de Label Studio:**

```bash
# Iniciar Label Studio sin autenticación
./start_labeling_fixed.sh

# Iniciar Label Studio con credenciales
./start_labeling.sh
```

## ⚙️ Configuración

### **Parámetros de Configuración (`TradingConfig`):**

- `symbol`: Par de trading (default: BTCUSDT)
- `interval`: Intervalo temporal (default: 4h)
- `limit`: Número de velas (default: 1000)
- `ema_periods`: Períodos EMA (default: [10, 55, 200])
- `adx_period`: Período ADX (default: 14)
- `atr_period`: Período ATR (default: 14)
- `smi_period`: Período SMI (default: 18)

### **Archivo de Configuración JSON:**

```json
{
  "symbol": "BTCUSDT",
  "interval": "4h",
  "limit": 1000,
  "ema_periods": [10, 55, 200],
  "adx_period": 14,
  "atr_period": 14,
  "smi_period": 18,
  "output_file": "trading_data_labeling.csv"
}
```

## 📊 Indicadores Técnicos Calculados

### **Implementados en `technical_indicators.py`:**

- **EMA**: 10, 55, 200 períodos
- **ADX**: Average Directional Index (14 períodos)
- **ATR**: Average True Range (14 períodos)
- **SMI**: Squeeze Momentum Indicator (18 períodos)
- **Squeeze Momentum**: Indicador completo con Bollinger Bands y Keltner Channel

### **Implementaciones Originales (`SMI.py`):**

- `SMIHistogram.SMIH()` - Squeeze Momentum Indicator
- `ADX` - Average Directional Index
- `ATR` - Average True Range

## 🔄 Flujo de Datos

1. **Descarga**: `data_downloader.py` → Binance API
2. **Procesamiento**: `technical_indicators.py` → Cálculo de indicadores
3. **Guardado**: Dataset CSV en `data/processed/`
4. **Export**: Copia en `data/exports/latest_dataset.csv` para Label Studio

## 📁 Estructura de Directorios

```
data/
├── exports/           # Dataset para Label Studio
│   └── latest_dataset.csv
├── processed/         # Datasets procesados con timestamp
│   └── BTCUSDT_4h_20251023_222652.csv
└── raw/              # Datos sin procesar
```

## 🔧 Dependencias Principales

- **Binance API**: `requests`, `pandas`
- **Indicadores Técnicos**: `ta-lib`, `pandas-ta`, `scikit-learn`
- **Label Studio**: `label-studio`
- **Visualización**: `matplotlib`, `seaborn`, `plotly`

## 🎯 Casos de Uso

### **1. Pipeline Completo:**
```python
from trading_pipeline import TradingPipeline
from config import TradingConfig

config = TradingConfig(symbol='ETHUSDT', interval='1h', limit=500)
pipeline = TradingPipeline(config)
df = pipeline.run_pipeline()
```

### **2. Solo Descarga de Datos:**
```python
from data_downloader import downloader

df = downloader.download_data(symbol='BTCUSDT', interval='4h', limit=1000)
```

### **3. Solo Cálculo de Indicadores:**
```python
from technical_indicators import indicators

df_with_indicators = indicators.calculate_all_indicators(
    df, 
    ema_periods=[20, 50, 100],
    adx_period=20,
    atr_period=10,
    smi_period=14
)
```

## 🔍 Archivos Clave

- **`README_MODULAR.md`**: Documentación completa del sistema
- **`requirements.txt`**: Dependencias del proyecto
- **`config_btc_4h.json`**: Configuración de ejemplo
- **`LABELING_GUIDE.md`**: Guía para etiquetado en Label Studio

## 🛠️ Scripts de Desarrollo

- **`quick_visualize.py`**: Visualización rápida de datos
- **`candlestick_visualizer.py`**: Visualización de velas
- **`download_trading_data.py`**: Script de descarga independiente

## 📈 Output del Sistema

El pipeline genera:
- Dataset CSV con todos los indicadores calculados
- Configuración actualizada para Label Studio
- Resumen estadístico del procesamiento
- Datasets organizados por timestamp en `data/processed/`

## 🔄 Mantenimiento

- **Compatibilidad**: `technical_indicators.py` usa implementaciones idénticas a `SMI.py`
- **Modularidad**: Cada módulo funciona independientemente
- **Configurabilidad**: Parámetros por CLI, JSON o variables de entorno
- **Extensibilidad**: Fácil agregar nuevos indicadores o fuentes de datos