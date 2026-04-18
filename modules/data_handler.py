import streamlit as st
import pandas as pd
import numpy as np

def render_data_tab():
    st.header("Generación o Carga de Datos")

    if 'modo_vista' not in st.session_state:
        st.session_state['modo_vista'] = 'ambos'

    if st.session_state['modo_vista'] != 'ambos':
        if st.button("↺ Cambiar método de ingreso de datos"):
            st.session_state['modo_vista'] = 'ambos'
            if 'datos' in st.session_state:
                del st.session_state['datos']
            st.rerun()
        st.divider()

    if st.session_state['modo_vista'] == 'ambos':
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<i class="fa-solid fa-wand-magic-sparkles fa-icon"></i> **Opción A: Generar Datos Sintéticos**', unsafe_allow_html=True)
            n_muestras = st.slider("Tamaño de la muestra (n)", 30, 1000, 100, 10)
            media_real = st.number_input("Media poblacional real (μ)", value=100.0)
            desv_est = st.number_input("Desviación estándar (σ)", value=15.0, min_value=0.1)

            if st.button("Generar Datos", type="primary"):
                datos = np.random.normal(loc=media_real, scale=desv_est, size=n_muestras)
                st.session_state['datos'] = pd.DataFrame({'Valor': datos})
                st.session_state['modo_vista'] = 'opcion_a'
                st.rerun()

        with col2:
            st.markdown('<i class="fa-solid fa-file-arrow-up fa-icon"></i> **Opción B: Subir CSV**', unsafe_allow_html=True)
            archivo_subido = st.file_uploader("Elige un archivo CSV", type="csv")
            if archivo_subido is not None:
                df = pd.read_csv(archivo_subido)
                st.session_state['datos'] = df
                st.session_state['modo_vista'] = 'opcion_b'
                st.rerun()

    elif st.session_state['modo_vista'] == 'opcion_a':
        st.markdown('<i class="fa-solid fa-wand-magic-sparkles fa-icon"></i> **Opción A: Generar Datos Sintéticos**', unsafe_allow_html=True)
        st.info("Modo sintético activo. Ajusta los controles y regenera si quieres nuevos datos.")

        col_n, col_mu, col_sigma = st.columns(3)
        with col_n: n_muestras = st.slider("Tamaño de la muestra (n)", 30, 1000, 100, 10, key="n_re")
        with col_mu: media_real = st.number_input("Media poblacional (μ)", value=100.0, key="mu_re")
        with col_sigma: desv_est = st.number_input("Desviación estándar (σ)", value=15.0, min_value=0.1, key="sigma_re")

        if st.button("Regenerar Datos", type="primary"):
            datos = np.random.normal(loc=media_real, scale=desv_est, size=n_muestras)
            st.session_state['datos'] = pd.DataFrame({'Valor': datos})
            st.success("¡Datos actualizados!")

    elif st.session_state['modo_vista'] == 'opcion_b':
        st.markdown('<i class="fa-solid fa-file-arrow-up fa-icon"></i> **Opción B: Subir CSV**', unsafe_allow_html=True)
        st.success("¡Archivo procesado correctamente!")
        archivo_subido = st.file_uploader("Elige otro archivo si deseas reemplazar el actual", type="csv")
        if archivo_subido is not None:
            df = pd.read_csv(archivo_subido)
            st.session_state['datos'] = df

    st.divider()

    if 'datos' in st.session_state:
        total_datos = len(st.session_state['datos'])
        st.write(f"### Vista de los datos ({total_datos} registros):")
        st.dataframe(st.session_state['datos'], use_container_width=True)