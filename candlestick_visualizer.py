"""
Candlestick Visualizer
Visualizador interactivo de velas japonesas con indicadores técnicos
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
import argparse
import os


class CandlestickVisualizer:
    """Visualizador interactivo de velas japonesas"""
    
    def __init__(self):
        self.fig = None
        
    def load_data(self, csv_path):
        """Cargar datos desde CSV"""
        print(f"📁 Cargando datos desde: {csv_path}")
        
        df = pd.read_csv(csv_path)
        
        # Convertir fecha a datetime y establecer como índice
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        print(f"✅ Datos cargados: {len(df)} velas")
        print(f"📊 Columnas disponibles: {list(df.columns)}")
        
        return df
    
    def create_candlestick_chart(self, df, title="Trading Data"):
        """Crear gráfico de velas con indicadores"""
        
        # Crear figura con subplots
        self.fig = make_subplots(
            rows=5, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Velas Japonesas + EMAs', 'Volumen', 'ADX', 'ATR', 'Squeeze Momentum'),
            row_heights=[0.4, 0.12, 0.12, 0.12, 0.24]
        )
        
        # 1. Gráfico de velas
        self.fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Velas'
            ),
            row=1, col=1
        )
        
        # 2. Agregar EMAs si existen
        if 'ema10' in df.columns:
            self.fig.add_trace(
                go.Scatter(x=df.index, y=df['ema10'], 
                         line=dict(color='orange', width=1),
                         name='EMA 10'),
                row=1, col=1
            )
        
        if 'ema55' in df.columns:
            self.fig.add_trace(
                go.Scatter(x=df.index, y=df['ema55'], 
                         line=dict(color='blue', width=1.5),
                         name='EMA 55'),
                row=1, col=1
            )
            
        if 'ema200' in df.columns:
            self.fig.add_trace(
                go.Scatter(x=df.index, y=df['ema200'], 
                         line=dict(color='red', width=2),
                         name='EMA 200'),
                row=1, col=1
            )
        
        # 3. Gráfico de volumen
        colors_volume = ['red' if df['close'].iloc[i] < df['open'].iloc[i] 
                        else 'green' for i in range(len(df))]
        
        self.fig.add_trace(
            go.Bar(x=df.index, y=df['volume'], 
                  marker_color=colors_volume,
                  name='Volumen'),
            row=2, col=1
        )
        
        # 4. Gráfico de ADX
        if 'adx' in df.columns:
            self.fig.add_trace(
                go.Scatter(x=df.index, y=df['adx'], 
                         line=dict(color='purple', width=1),
                         name='ADX'),
                row=3, col=1
            )
            
            # Línea de referencia ADX 25 usando shape
            self.fig.add_shape(
                type="line",
                x0=df.index.min(), x1=df.index.max(),
                y0=25, y1=25,
                line=dict(color="red", width=1, dash="dash"),
                row=3, col=1
            )
            
            # Anotación para la línea ADX 25
            self.fig.add_annotation(
                x=df.index.min(), y=25,
                text="ADX 25",
                showarrow=False,
                yshift=10,
                row=3, col=1
            )
        
        # 4. Gráfico de ATR
        if 'atr' in df.columns:
            self.fig.add_trace(
                go.Scatter(x=df.index, y=df['atr'], 
                         line=dict(color='orange', width=1),
                         name='ATR'),
                row=4, col=1
            )
        
        # 5. Gráfico de Squeeze Momentum con estados
        if 'squeeze_momentum' in df.columns:
            # Squeeze Momentum como línea
            self.fig.add_trace(
                go.Scatter(x=df.index, y=df['squeeze_momentum'], 
                         line=dict(color='brown', width=1),
                         name='Squeeze Momentum'),
                row=5, col=1
            )
            
            # Agregar barras verticales para squeeze states
            if 'squeeze_state' in df.columns:
                # Colores para cada estado
                squeeze_colors = {
                    'squeeze_on': 'red',
                    'squeeze_off': 'green', 
                    'no_squeeze': 'gray'
                }
                
                # Crear barras verticales para cada estado
                for state, color in squeeze_colors.items():
                    mask = df['squeeze_state'] == state
                    if mask.any():
                        # Calcular altura máxima del squeeze momentum para escalar las barras
                        max_squeeze = abs(df['squeeze_momentum']).max() if len(df['squeeze_momentum']) > 0 else 1
                        bar_height = max_squeeze * 0.8  # 80% del máximo
                        
                        self.fig.add_trace(
                            go.Scatter(
                                x=df.index[mask],
                                y=[bar_height] * mask.sum(),
                                mode='markers',
                                marker=dict(
                                    color=color,
                                    size=8,
                                    symbol='line-ns-open',
                                    line=dict(width=2)
                                ),
                                name=f'Squeeze {state}',
                                showlegend=True
                            ),
                            row=5, col=1
                        )
        
        # Configurar layout
        self.fig.update_layout(
            title=title,
            xaxis_rangeslider_visible=False,
            height=1000,
            showlegend=True,
            template="plotly_white"
        )
        
        # Configurar ejes Y
        self.fig.update_yaxes(title_text="Precio", row=1, col=1)
        self.fig.update_yaxes(title_text="Volumen", row=2, col=1)
        self.fig.update_yaxes(title_text="ADX", row=3, col=1)
        self.fig.update_yaxes(title_text="ATR", row=4, col=1)
        self.fig.update_yaxes(title_text="Squeeze Momentum", row=5, col=1)
        
        return self.fig
    
    def show_chart(self, output_file=None):
        """Mostrar o guardar el gráfico"""
        if self.fig is None:
            print("❌ No hay gráfico para mostrar. Ejecuta create_candlestick_chart primero.")
            return
            
        if output_file:
            # Guardar como HTML interactivo
            self.fig.write_html(output_file)
            print(f"💾 Gráfico guardado como: {output_file}")
            print("🌐 Abre el archivo en tu navegador para verlo interactivo")
        else:
            # Mostrar en el navegador
            self.fig.show()
    
    def analyze_data(self, df):
        """Análisis rápido de los datos"""
        print("\n📈 ANÁLISIS RÁPIDO:")
        print(f"   • Rango de fechas: {df.index.min()} a {df.index.max()}")
        print(f"   • Precio máximo: ${df['high'].max():.2f}")
        print(f"   • Precio mínimo: ${df['low'].min():.2f}")
        print(f"   • Volumen promedio: {df['volume'].mean():.0f}")
        
        if 'adx' in df.columns:
            strong_trend = (df['adx'] > 25).sum()
            print(f"   • Velas con ADX > 25: {strong_trend} ({strong_trend/len(df)*100:.1f}%)")
        
        if 'squeeze_state' in df.columns:
            squeeze_on = (df['squeeze_state'] == 'squeeze_on').sum()
            squeeze_off = (df['squeeze_state'] == 'squeeze_off').sum()
            no_squeeze = (df['squeeze_state'] == 'no_squeeze').sum()
            print(f"   • Squeeze ON: {squeeze_on} ({squeeze_on/len(df)*100:.1f}%)")
            print(f"   • Squeeze OFF: {squeeze_off} ({squeeze_off/len(df)*100:.1f}%)")
            print(f"   • No Squeeze: {no_squeeze} ({no_squeeze/len(df)*100:.1f}%)")


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Visualizador de Velas Japonesas')
    parser.add_argument('--file', required=True, help='Ruta al archivo CSV')
    parser.add_argument('--output', help='Guardar como archivo HTML')
    parser.add_argument('--title', default='Análisis de Trading', help='Título del gráfico')
    
    args = parser.parse_args()
    
    # Verificar que el archivo existe
    if not os.path.exists(args.file):
        print(f"❌ Archivo no encontrado: {args.file}")
        return
    
    # Crear visualizador
    visualizer = CandlestickVisualizer()
    
    # Cargar datos
    df = visualizer.load_data(args.file)
    
    # Mostrar análisis
    visualizer.analyze_data(df)
    
    # Crear gráfico
    visualizer.create_candlestick_chart(df, args.title)
    
    # Mostrar o guardar
    visualizer.show_chart(args.output)


if __name__ == "__main__":
    main()