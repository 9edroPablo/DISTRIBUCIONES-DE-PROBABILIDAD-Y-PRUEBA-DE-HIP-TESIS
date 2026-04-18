import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats

def render_plots_tab():
    st.header("Visualización y Distribución de Datos")

    if 'datos' not in st.session_state or st.session_state['datos'].empty:
        st.warning("Primero debes generar o subir datos en el Paso 1.")
        return

    df = st.session_state['datos']
    columna_datos = df.select_dtypes(include=[np.number]).columns[0]

    st.markdown('<i class="fa-solid fa-magnifying-glass-chart fa-icon"></i> **Análisis Exploratorio de la Muestra**', unsafe_allow_html=True)
    st.markdown("Visualiza la forma de tus datos y detecta valores atípicos.")

    fig_hist = px.histogram(
        df,
        x=columna_datos,
        marginal="box",
        title=f"Distribución de: {columna_datos}",
        color_discrete_sequence=['#00f2fe'],
        opacity=0.7
    )
    fig_hist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.divider()

    st.markdown('<i class="fa-solid fa-wave-square fa-icon"></i> **Visualización de la Prueba Z**', unsafe_allow_html=True)

    if 'resultados_z' not in st.session_state:
        st.info("Despliega el Paso 2 y calcula la prueba para ver la Campana de Gauss.")
        return

    resultados = st.session_state['resultados_z']
    params = st.session_state['parametros_z']
    z_stat = resultados['z_stat']
    z_critico = resultados['z_critico']
    tipo_prueba = params['tipo']

    x = np.linspace(-4, 4, 1000)
    y = stats.norm.pdf(x, 0, 1)

    fig_norm = go.Figure()
    fig_norm.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribución N(0,1)', line=dict(color='white')))

    if tipo_prueba in ('Cola derecha', 'Bilateral'):
        x_right = np.linspace(z_critico, 4, 100)
        fig_norm.add_trace(go.Scatter(x=x_right, y=stats.norm.pdf(x_right, 0, 1), fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.5)', name='Zona de Rechazo'))

    if tipo_prueba in ('Cola izquierda', 'Bilateral'):
        z_critico_izq = -z_critico if tipo_prueba == 'Bilateral' else z_critico
        x_left = np.linspace(-4, z_critico_izq, 100)
        fig_norm.add_trace(go.Scatter(x=x_left, y=stats.norm.pdf(x_left, 0, 1), fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.5)', name='Zona de Rechazo (Izq)'))

    fig_norm.add_vline(x=z_stat, line_dash="dash", line_color="#00f2fe", annotation_text=f"Z Calculado: {z_stat:.2f}", annotation_position="top right")
    fig_norm.update_layout(
        title="Regiones Críticas y Estadístico Z",
        xaxis_title="Valores Z",
        yaxis_title="Densidad de Probabilidad",
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_norm, use_container_width=True)