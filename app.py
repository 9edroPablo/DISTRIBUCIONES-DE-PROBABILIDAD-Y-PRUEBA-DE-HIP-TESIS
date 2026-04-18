import streamlit as st
from modules.data_handler import render_data_tab
from modules.stats_engine import render_stats_tab

st.set_page_config(page_title="Z-Test & AI Analytics", page_icon="📊", layout="wide")

st.title("📊 Analizador Estadístico & Prueba de Hipótesis")
st.markdown("Documentación interactiva de toma de decisiones estadísticas con IA.")

tab1, tab2, tab3, tab4 = st.tabs([
    "1. Carga de Datos", 
    "2. Visualización", 
    "3. Prueba Z", 
    " 4. Asistente IA"
])

with tab1:
    render_data_tab()

with tab2:
    st.info("🚧 Módulo de visualizaciones en construcción...")

with tab3:
    render_stats_tab()

with tab4:
    st.info("🚧 Módulo de integración con Gemini en construcción...")