"""
Visualización Rápida - Abre automáticamente el gráfico en el navegador
Versión mejorada para velas japonesas
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser
import os
import sys


def quick_visualize(csv_path, auto_open=True):
    """Visualización rápida de datos de trading - Versión mejorada"""

    print(f"🚀 Cargando: {csv_path}")

    # Cargar datos
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    print(f"✅ {len(df)} velas cargadas")
    print(f"📊 Columnas disponibles: {list(df.columns)}")

    # Crear figura con más subplots para incluir todos los indicadores
    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=('Velas Japonesas + EMAs', 'Volumen', 'ADX', 'ATR', 'Squeeze Momentum + Estado'),
        row_heights=[0.4, 0.12, 0.12, 0.12, 0.24]
    )

    # **GRÁFICO DE VELAS JAPONESAS MEJORADO**
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Precio',
            increasing_line_color='#2E8B57',  # Verde para velas alcistas
            decreasing_line_color='#DC143C',  # Rojo para velas bajistas
            increasing_fillcolor='#2E8B57',
            decreasing_fillcolor='#DC143C'
        ), row=1, col=1
    )

    # EMAs con colores más visibles
    if 'ema10' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['ema10'],
            line=dict(color='#FFA500', width=2),
            name='EMA10'
        ), row=1, col=1)

    if 'ema55' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['ema55'],
            line=dict(color='#1E90FF', width=2.5),
            name='EMA55'
        ), row=1, col=1)

    if 'ema200' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['ema200'],
            line=dict(color='#FF0000', width=3),
            name='EMA200'
        ), row=1, col=1)

    # **VOLUMEN MEJORADO**
    colors_volume = ['#DC143C' if df['close'].iloc[i] < df['open'].iloc[i]
                    else '#2E8B57' for i in range(len(df))]

    fig.add_trace(go.Bar(
        x=df.index,
        y=df['volume'],
        marker_color=colors_volume,
        name='Volumen',
        opacity=0.7
    ), row=2, col=1)

    # **ADX MEJORADO**
    if 'adx' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['adx'],
            line=dict(color='#8A2BE2', width=2),
            name='ADX',
            fill='tozeroy',
            fillcolor='rgba(138, 43, 226, 0.1)'
        ), row=3, col=1)
        # Líneas de referencia para ADX (como trazas en lugar de add_hline)
        fig.add_trace(go.Scatter(
            x=[df.index[0], df.index[-1]], y=[25, 25],
            line=dict(color='red', dash='dash', width=1),
            name='ADX 25',
            showlegend=False
        ), row=3, col=1)
        fig.add_trace(go.Scatter(
            x=[df.index[0], df.index[-1]], y=[50, 50],
            line=dict(color='orange', dash='dash', width=1),
            name='ADX 50',
            showlegend=False
        ), row=3, col=1)

    # **ATR (nuevo)**
    if 'atr' in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index, y=df['atr'],
            line=dict(color='#FF6347', width=2),
            name='ATR',
            fill='tozeroy',
            fillcolor='rgba(255, 99, 71, 0.1)'
        ), row=4, col=1)

    # **SQUEEZE MOMENTUM + ESTADO (mejorado)**
    if 'squeeze_momentum' in df.columns:
        # Crear colores para el squeeze momentum
        colors_squeeze = ['red' if x < 0 else 'green' for x in df['squeeze_momentum']]

        # Gráfico de barras del squeeze momentum
        fig.add_trace(go.Bar(
            x=df.index,
            y=df['squeeze_momentum'],
            marker_color=colors_squeeze,
            name='Squeeze Momentum',
            opacity=0.7
        ), row=5, col=1)

        # Línea cero de referencia (como traza)
        fig.add_trace(go.Scatter(
            x=[df.index[0], df.index[-1]], y=[0, 0],
            line=dict(color='black', width=1),
            name='Zero Line',
            showlegend=False
        ), row=5, col=1)

        # Barra horizontal del squeeze state si está disponible
        if 'squeeze_state_numeric' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df['squeeze_state_numeric'],
                line=dict(color='yellow', width=3),
                name='Squeeze State',
                mode='lines'
            ), row=5, col=1)
            
            # Líneas de referencia para los estados (como trazas)
            fig.add_trace(go.Scatter(
                x=[df.index[0], df.index[-1]], y=[1, 1],
                line=dict(color='green', dash='dash', width=1),
                name='Squeeze ON',
                showlegend=False
            ), row=5, col=1)
            fig.add_trace(go.Scatter(
                x=[df.index[0], df.index[-1]], y=[-1, -1],
                line=dict(color='red', dash='dash', width=1),
                name='Squeeze OFF',
                showlegend=False
            ), row=5, col=1)
            fig.add_trace(go.Scatter(
                x=[df.index[0], df.index[-1]], y=[0, 0],
                line=dict(color='gray', dash='dash', width=1),
                name='No Squeeze',
                showlegend=False
            ), row=5, col=1)

    # **MEJORAS EN EL LAYOUT**
    symbol = os.path.basename(csv_path).split('_')[0]
    timeframe = os.path.basename(csv_path).split('_')[1]

    fig.update_layout(
        title=f'{symbol} {timeframe} - Análisis Técnico Completo<br><sub>Velas Japonesas + Indicadores</sub>',
        xaxis_rangeslider_visible=False,
        height=1000,
        template="plotly_dark",  # Cambiado a tema oscuro para mejor contraste
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Actualizar ejes
    fig.update_xaxes(title_text='Fecha', row="5", col="1")
    fig.update_yaxes(title_text='Precio', row="1", col="1")
    fig.update_yaxes(title_text='Volumen', row="2", col="1")
    fig.update_yaxes(title_text='ADX', row="3", col="1")
    fig.update_yaxes(title_text='ATR', row="4", col="1")
    if 'squeeze_momentum' in df.columns:
        fig.update_yaxes(title_text='Squeeze', row="5", col="1")

    # Guardar y abrir
    output_file = f'quick_view_{symbol}_{timeframe}.html'
    fig.write_html(output_file)

    print(f"💾 Guardado como: {output_file}")
    print(f"📈 Período: {df.index[0]} a {df.index[-1]}")

    if auto_open:
        print("🌐 Abriendo en navegador...")
        webbrowser.open(f'file://{os.path.abspath(output_file)}')

    return output_file


if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        # Usar el último archivo procesado
        csv_file = 'data/exports/latest_dataset.csv'

    if os.path.exists(csv_file):
        quick_visualize(csv_file)
    else:
        print("❌ Archivo no encontrado. Ejemplos:")
        print("python quick_visualize.py data/processed/BTCUSDT_4h_20251023_224303.csv")
        print("python quick_visualize.py data/exports/latest_dataset.csv")