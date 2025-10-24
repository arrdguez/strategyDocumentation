# 📊 Guía para Visualizar Datos en TradingView

## 🚀 **Método Rápido: Importar CSV**

### Paso 1: Preparar los datos
Tu archivo CSV ya está listo en:
```
data/exports/latest_dataset.csv
data/processed/ETHUSDT_1h_20251023_220002.csv
```

### Paso 2: Subir a TradingView
1. Ve a [TradingView](https://www.tradingview.com/)
2. Crea una cuenta gratuita (si no tienes)
3. Ve al **Chart** (Gráfico)
4. Haz clic en el **ícono de carga** (📁) en la barra superior
5. Selecciona "Import custom historical data"

### Paso 3: Formato requerido
Tu CSV ya tiene el formato correcto:
```csv
date,open,high,low,close,volume,ema10,ema55,ema200,adx,atr,smi
2025-10-15 21:00:00,3961.52,3981.77,3926.74,3954.17,20888.7313,...
```

### Paso 4: Configurar en TradingView
- **Symbol**: Pon cualquier nombre (ej: "ETH_CUSTOM")
- **Timezone**: UTC
- **Session**: 24x7
- **Format**: CSV

## 🔧 **Método Avanzado: Script Pine**

### Crear indicadores personalizados
En TradingView, puedes crear scripts Pine para replicar tus indicadores:

```pinescript
//@version=5
indicator("EMA Custom", overlay=true)
ema10 = ta.ema(close, 10)
ema55 = ta.ema(close, 55)
ema200 = ta.ema(close, 200)

plot(ema10, color=color.orange, linewidth=1)
plot(ema55, color=color.blue, linewidth=1.5)
plot(ema200, color=color.red, linewidth=2)
```

## 📈 **Ventajas de TradingView**

- ✅ **Interfaz profesional**
- ✅ **Miles de indicadores built-in**
- ✅ **Herramientas de dibujo**
- ✅ **Análisis técnico avanzado**
- ✅ **Comunidad activa**
- ✅ **Funciona en web/móvil**

## 🎯 **Recomendación**

**Usa ambos métodos:**
- **Python Visualizer**: Para análisis rápido y automatizado
- **TradingView**: Para análisis profundo y herramientas avanzadas

## 📱 **Cómo Usar el Visualizador Python**

```bash
# Visualizar datos existentes
python candlestick_visualizer.py --file data/processed/ETHUSDT_1h_20251023_220002.csv

# Guardar como HTML interactivo
python candlestick_visualizer.py --file data/processed/ETHUSDT_1h_20251023_220002.csv --output mi_analisis.html

# Con título personalizado
python candlestick_visualizer.py --file data/processed/ETHUSDT_1h_20251023_220002.csv --title "Análisis ETHUSDT 1h" --output eth_analysis.html
```

## 🎨 **Características del Visualizador Python**

- 📊 **4 subplots**: Velas, Volumen, ADX, SMI
- 🎯 **EMAs**: 10, 55, 200 (colores distintos)
- 📈 **Interactivo**: Zoom, pan, hover
- 💾 **Exportable**: Guarda como HTML
- 🔍 **Análisis automático**: Estadísticas básicas

## 🚀 **Próximos Pasos**

1. **Abre el archivo HTML** generado en tu navegador
2. **Sube el CSV** a TradingView para comparar
3. **Experimenta** con ambos métodos
4. **Etiqueta patrones** usando Label Studio