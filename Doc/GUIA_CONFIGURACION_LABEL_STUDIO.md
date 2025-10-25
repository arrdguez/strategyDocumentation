# 🛠️ GUÍA DE CONFIGURACIÓN XML - LABEL STUDIO

## 📋 **ENTENDIENDO EL ARCHIVO XML**

El archivo `label_studio_config.xml` define:
- **Etiquetas disponibles** para seleccionar
- **Visualización** de datos (gráficos, indicadores)
- **Interfaz** de usuario (paneles, guías)

---

## 🏷️ **MODIFICAR ETIQUETAS (Lo Más Importante)**

### **Estructura Básica de una Etiqueta:**
```xml
<Label value="NOMBRE_ETIQUETA" background="#COLOR_HEX"/>
```

### **Tu Sistema Personalizado - EJEMPLO:**
```xml
<TimeSeriesLabels name="label" toName="ts">
  
  <!-- === TUS ETIQUETAS PERSONALES === -->
  
  <!-- Entradas -->
  <Label value="LONG_MI_BREAKOUT_EMA55" background="#27AE60"/>
  <Label value="SHORT_MI_REVERSION_RSI70" background="#C0392B"/>
  <Label value="LONG_MI_PULLBACK_EMA20" background="#2ECC71"/>
  <Label value="SHORT_MI_DOUBLE_TOP" background="#E74C3C"/>
  
  <!-- Salidas -->
  <Label value="EXIT_LONG_OBJETIVO" background="#16A085"/>
  <Label value="EXIT_SHORT_STOP_LOSS" background="#8E44AD"/>
  <Label value="EXIT_LONG_QUIEBRE_EMA" background="#F39C12"/>
  
  <!-- No Acción -->
  <Label value="NO_ACTION_AMBIGUO" background="#95A5A6"/>
  <Label value="NO_ACTION_LATERAL" background="#7F8C8D"/>
  
  <!-- Contexto -->
  <Label value="TREND_UP_FUERTE" background="#3498DB"/>
  <Label value="TREND_DOWN_FUERTE" background="#E67E22"/>
  <Label value="RANGE_BOUND" background="#9B59B6"/>
  
</TimeSeriesLabels>
```

### **Organización por Grupos (Recomendado):**
```xml
<TimeSeriesLabels name="label" toName="ts">
  
  <!-- 🎯 ENTRADAS -->
  <Header value="ENTRADAS"/>
  <Label value="LONG_BREAKOUT_EMA55" background="#27AE60"/>
  <Label value="SHORT_BREAKOUT_EMA55" background="#C0392B"/>
  <Label value="LONG_REVERSION_RSI30" background="#2ECC71"/>
  <Label value="SHORT_REVERSION_RSI70" background="#E74C3C"/>
  
  <!-- 🚪 SALIDAS -->
  <Header value="SALIDAS"/>
  <Label value="EXIT_LONG_OBJETIVO" background="#16A085"/>
  <Label value="EXIT_SHORT_OBJETIVO" background="#8E44AD"/>
  <Label value="EXIT_LONG_STOP" background="#F39C12"/>
  <Label value="EXIT_SHORT_STOP" background="#D35400"/>
  
  <!-- ❌ NO ACCIÓN -->
  <Header value="NO ACCIÓN"/>
  <Label value="NO_ACTION" background="#95A5A6"/>
  
  <!-- 🌡️ CONTEXTO -->
  <Header value="CONTEXTO"/>
  <Label value="TREND_UP" background="#3498DB"/>
  <Label value="TREND_DOWN" background="#E67E22"/>
  <Label value="RANGE_BOUND" background="#9B59B6"/>
  
</TimeSeriesLabels>
```

---

## 📊 **MODIFICAR INDICADORES VISUALES**

### **Sección TimeSeries - Agregar Nuevos Indicadores:**
```xml
<TimeSeries name="ts" value="$csv" valueType="url" timeColumn="date" timeFormat="%Y-%m-%d %H:%M:%S" overviewChannels="open,high,low,close">
  
  <!-- Precios Básicos -->
  <Channel column="open" strokeColor="#1f77b4"/>
  <Channel column="high" strokeColor="#ff7f0e"/>
  <Channel column="low" strokeColor="#2ca02c"/>
  <Channel column="close" strokeColor="#d62728"/>
  
  <!-- Volumen -->
  <Channel column="volume" strokeColor="#9467bd" optional="true"/>
  
  <!-- EMAs -->
  <Channel column="ema10" strokeColor="#17becf" optional="true"/>
  <Channel column="ema55" strokeColor="#bcbd22" optional="true"/>
  <Channel column="ema200" strokeColor="#8c564b" optional="true"/>
  
  <!-- === NUEVOS INDICADORES === -->
  <Channel column="rsi" strokeColor="#FF69B4" optional="true"/>
  <Channel column="squeeze_momentum" strokeColor="#1ABC9C" optional="true"/>
  <Channel column="tr_plus" strokeColor="#27AE60" optional="true"/>
  <Channel column="tr_minus" strokeColor="#E74C3C" optional="true"/>
  
</TimeSeries>
```

**Nota:** Los indicadores deben existir en tu CSV como columnas.

---

## 📝 **MODIFICAR GUÍAS Y PANELES**

### **Actualizar la Guía de Patrones:**
```xml
<!-- Pattern Description Panel -->
<View style="padding: 20px; background: #f8f9fa; border-radius: 5px; margin-top: 10px;">
  <Header value="TU ESTRATEGIA - Guía de Patrones"/>
  
  <View style="display: flex; flex-wrap: wrap; gap: 10px;">
    
    <!-- Tus Entradas -->
    <View style="flex: 1; min-width: 200px;">
      <Header value="🎯 Tus Entradas" size="4"/>
      <Text name="mis_entradas" value="
• **LONG_BREAKOUT_EMA55**: Ruptura EMA55 con volumen
• **SHORT_REVERSION_RSI70**: Reversión desde sobrecompra
• **LONG_PULLBACK_EMA20**: Pullback a EMA20 en tendencia
      "/>
    </View>
    
    <!-- Tus Salidas -->
    <View style="flex: 1; min-width: 200px;">
      <Header value="🚪 Tus Salidas" size="4"/>
      <Text name="mis_salidas" value="
• **EXIT_OBJETIVO**: Target de riesgo:beneficio 1:2
• **EXIT_STOP**: Stop por quiebre de estructura
• **EXIT_RSI_EXTREMO**: RSI >80 o <20
      "/>
    </View>
    
    <!-- Contexto -->
    <View style="flex: 1; min-width: 200px;">
      <Header value="🌡️ Contexto" size="4"/>
      <Text name="contexto" value="
• **TREND_UP**: EMAs alineadas arriba
• **TREND_DOWN**: EMAs alineadas abajo
• **RANGE_BOUND**: EMAs entrecruzadas
      "/>
    </View>
    
  </View>
</View>
```

---

## 🚀 **PROCESO PASO A PASO**

### **1. Crear Tu XML Personalizado**
```bash
# Copiar el original
cp label_studio_config.xml label_studio_config_MI_ESTRATEGIA.xml

# Editar con tus etiquetas
nano label_studio_config_MI_ESTRATEGIA.xml
```

### **2. Ejemplo Completo - Estrategia Simple:**
```xml
<View>
  
  <!-- Etiquetas -->
  <TimeSeriesLabels name="label" toName="ts">
    
    <!-- Entradas -->
    <Header value="🎯 ENTRADAS"/>
    <Label value="LONG_BREAKOUT_EMA55" background="#27AE60"/>
    <Label value="SHORT_BREAKOUT_EMA55" background="#C0392B"/>
    <Label value="LONG_PULLBACK_EMA20" background="#2ECC71"/>
    
    <!-- Salidas -->
    <Header value="🚪 SALIDAS"/>
    <Label value="EXIT_OBJETIVO" background="#16A085"/>
    <Label value="EXIT_STOP" background="#F39C12"/>
    
    <!-- No Acción -->
    <Header value="❌ NO ACCIÓN"/>
    <Label value="NO_ACTION" background="#95A5A6"/>
    
  </TimeSeriesLabels>

  <!-- Datos -->
  <TimeSeries name="ts" value="$csv" valueType="url" timeColumn="date" timeFormat="%Y-%m-%d %H:%M:%S" overviewChannels="open,high,low,close">
    <Channel column="open" strokeColor="#1f77b4"/>
    <Channel column="high" strokeColor="#ff7f0e"/>
    <Channel column="low" strokeColor="#2ca02c"/>
    <Channel column="close" strokeColor="#d62728"/>
    <Channel column="volume" strokeColor="#9467bd" optional="true"/>
    <Channel column="ema10" strokeColor="#17becf" optional="true"/>
    <Channel column="ema55" strokeColor="#bcbd22" optional="true"/>
    <Channel column="ema200" strokeColor="#8c564b" optional="true"/>
    <Channel column="rsi" strokeColor="#FF69B4" optional="true"/>
    <Channel column="squeeze_momentum" strokeColor="#1ABC9C" optional="true"/>
  </TimeSeries>
  
</View>
```

### **3. Usar en Label Studio**
```bash
# Iniciar Label Studio con tu configuración
./start_labeling_fixed.sh

# En la interfaz web:
# 1. Crear nuevo proyecto
# 2. Importar → label_studio_config_MI_ESTRATEGIA.xml
# 3. Subir datos → latest_dataset.csv
```

---

## 🎨 **CONSEJOS DE DISEÑO**

### **Colores por Categoría:**
- **Verdes (#27AE60, #2ECC71)**: Entradas largas
- **Rojos (#C0392B, #E74C3C)**: Entradas cortas  
- **Azules (#3498DB, #2980B9)**: Tendencia alcista
- **Naranjas (#E67E22, #D35400)**: Tendencia bajista
- **Grises (#95A5A6, #7F8C8D)**: No acción

### **Nombres Claros:**
```
✅ BIEN: "LONG_BREAKOUT_EMA55", "SHORT_REVERSION_RSI70"
❌ MAL:  "entrada1", "salida2", "patron_x"
```

### **Organización:**
- Grupos lógicos con `<Header>`
- Máximo 15-20 etiquetas principales
- Etiquetas específicas pero no demasiado

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Etiquetas No Aparecen:**
- Verificar que estén dentro de `<TimeSeriesLabels>`
- Revisar sintaxis XML (cerrar todas las etiquetas)
- Recargar proyecto en Label Studio

### **Indicadores No Se Ven:**
- Verificar que la columna exista en el CSV
- Revisar nombre exacto (case sensitive)
- Los indicadores deben calcularse en `technical_indicators.py`

### **Error al Importar:**
- Validar XML online: https://www.xmlvalidation.com/
- Revisar comillas y caracteres especiales

---

## 📋 **CHECKLIST FINAL**

- [ ] Definí mis etiquetas principales
- [ ] Organicé en grupos lógicos
- [ ] Asigné colores consistentes
- [ ] Incluí todos mis indicadores
- [ **NO_ACTION** es obligatorio
- [ ] Actualicé las guías de ayuda
- [ ] Probé la configuración
- [ ] Documenté mis reglas de etiquetado

**💡 Tu XML es la "cara" de tu estrategia en Label Studio. 
¡Hazlo claro, organizado y específico para TU forma de operar!**