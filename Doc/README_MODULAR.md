# 🏗️ Sistema Modular de Trading Data Labeling

## 📋 Arquitectura Desacoplada

### **Módulos Principales:**

1. **`config.py`** - Configuración centralizada
2. **`technical_indicators.py`** - Cálculo de indicadores (EMA, ADX, ATR, SMI)
3. **`data_downloader.py`** - Descarga modular de datos
4. **`trading_pipeline.py`** - Orquestador principal
5. **`SMI.py`** - Indicadores originales (mantenido para compatibilidad)

## 🚀 Uso Rápido

### **Opción 1: Parámetros por línea de comandos**
```bash
python trading_pipeline.py --symbol ETHUSDT --interval 1h --limit 500
```

### **Opción 2: Archivo de configuración JSON**
```bash
python trading_pipeline.py --config-file config_btc_4h.json
```

### **Opción 3: Configuración por defecto**
```bash
python trading_pipeline.py
```

## ⚙️ Configuración

### **Archivo JSON de configuración:**
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

## 📊 Indicadores Calculados

- **EMA**: 10, 55, 200 períodos
- **ADX**: Average Directional Index
- **ATR**: Average True Range  
- **SMI**: Squeeze Momentum Indicator
- **Cruces EMA**: 10>55 y 55>200
- **Precio vs EMA**: Porcentaje sobre EMA55 y EMA200

## 🔧 Personalización

### **Cambiar indicadores:**
```python
from technical_indicators import indicators

df_with_indicators = indicators.calculate_all_indicators(
    df,
    ema_periods=[20, 50, 100],  # EMAs personalizadas
    adx_period=20,              # ADX de 20 períodos
    atr_period=10,              # ATR de 10 períodos
    smi_period=14               # SMI de 14 períodos
)
```

### **Usar solo módulo de descarga:**
```python
from data_downloader import downloader

df = downloader.download_data(
    symbol='ETHUSDT',
    interval='1h',
    limit=200
)
```

## 🎯 Beneficios de la Arquitectura

- **✅ Desacoplado**: Cada módulo funciona independientemente
- **✅ Configurable**: Parámetros por CLI o JSON
- **✅ Extensible**: Fácil agregar nuevos indicadores
- **✅ Mantenible**: Código modular y organizado
- **✅ Reutilizable**: Módulos independientes

## 📈 Output

El sistema genera:
- `trading_data_labeling.csv` - Dataset con todos los indicadores
- Configuración actualizada para Label Studio
- Resumen estadístico del pipeline

## 🔄 Flujo de Trabajo

1. **Configurar** parámetros (CLI o JSON)
2. **Descargar** datos de Binance
3. **Calcular** indicadores técnicos
4. **Guardar** dataset para Label Studio
5. **Etiquetar** patrones en Label Studio