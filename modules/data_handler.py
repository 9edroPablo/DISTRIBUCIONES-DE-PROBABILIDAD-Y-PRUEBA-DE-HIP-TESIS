import streamlit as st
import pandas as pd
import numpy as np

def render_data_tab():
    st.header("Generación o Carga de Datos")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Opción A: Generar Datos Sintéticos")
        n_muestras = st.slider("Tamaño de la muestra (n)", 30, 1000, 100, 10)
        media_real = st.number_input("Media poblacional real (μ)", value=100.0)
        desv_est = st.number_input("Desviación estándar (σ)", value=15.0, min_value=0.1)
        
        if st.button("Generar Datos", type="primary"):
            datos = np.random.normal(loc=media_real, scale=desv_est, size=n_muestras)
            st.session_state['datos'] = pd.DataFrame({'Valor': datos})
            st.success(f"¡{n_muestras} datos generados!")
            
    with col2:
        st.subheader("Opción B: Subir CSV")
        archivo_subido = st.file_uploader("Elige un archivo CSV", type="csv")
        if archivo_subido is not None:
            df = pd.read_csv(archivo_subido)
            st.session_state['datos'] = df
            st.success("¡Archivo cargado!")

    st.divider()
    if 'datos' in st.session_state:
        st.write("### Vista previa de los datos:")
        st.dataframe(st.session_state['datos'].head(10).T)