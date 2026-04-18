import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats

def render_plots_tab():
    st.header("📈 Visualización y Distribución de Datos")
    
    # 1. Verificar si hay datos
    if 'datos' not in st.session_state or st.session_state['datos'].empty:
        st.warning("⚠️ Primero debes generar o subir datos en la pestaña '1. Carga de Datos'.")
        return
        
    df = st.session_state['datos']
    columna_datos = df.select_dtypes(include=[np.number]).columns[0]
    
    st.subheader("1. Análisis Exploratorio de la Muestra")
    st.markdown("Visualiza la forma de tus datos y detecta valores atípicos (outliers).")
    
    fig_hist = px.histogram(
        df, 
        x=columna_datos, 
        marginal="box", 
        title=f"Distribución de: {columna_datos}",
        color_discrete_sequence=['#636EFA'],
        opacity=0.7
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.divider()
    
    st.subheader("2. Visualización de la Prueba Z")
    
    if 'resultados_z' not in st.session_state:
        st.info("💡 Ve a la pestaña '3. Prueba Z' y calcula la prueba para ver la Campana de Gauss con las zonas de rechazo.")
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
    

    if tipo_prueba == 'Cola derecha' or tipo_prueba == 'Bilateral':
        x_right = np.linspace(z_critico, 4, 100)
        y_right = stats.norm.pdf(x_right, 0, 1)
        fig_norm.add_trace(go.Scatter(x=x_right, y=y_right, fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.5)', name='Zona de Rechazo'))
        
    if tipo_prueba == 'Cola izquierda' or tipo_prueba == 'Bilateral':
        z_critico_izq = -z_critico if tipo_prueba == 'Bilateral' else z_critico
        x_left = np.linspace(-4, z_critico_izq, 100)
        y_left = stats.norm.pdf(x_left, 0, 1)
        fig_norm.add_trace(go.Scatter(x=x_left, y=y_left, fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.5)', name='Zona de Rechazo (Izq)'))

   
    fig_norm.add_vline(x=z_stat, line_dash="dash", line_color="blue", annotation_text=f"Z Calculado: {z_stat:.2f}", annotation_position="top right")

    fig_norm.update_layout(
        title="Regiones Críticas y Estadístico Z",
        xaxis_title="Valores Z",
        yaxis_title="Densidad de Probabilidad",
        showlegend=False
    )
    
    st.plotly_chart(fig_norm, use_container_width=True)