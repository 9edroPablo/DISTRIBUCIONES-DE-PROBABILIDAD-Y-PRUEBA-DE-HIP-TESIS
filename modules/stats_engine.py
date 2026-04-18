import streamlit as st
import numpy as np
import scipy.stats as stats
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def generar_resumen_rapido(params, resultados, api_key):
    if not api_key:
        return "Resumen no disponible (falta API Key)."
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        En 2 frases cortas y muy casuales, dime qué significa que la prueba Z 
        con media esperada {params['mu']} haya dado un p-value de {resultados['p_value']:.4f} 
        y la decisión sea {'Rechazar' if resultados['rechazar_h0'] else 'No rechazar'}.
        No uses términos técnicos. Habla sobre lo que dicen los datos.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar resumen: {e}"

def calcular_prueba_z(datos, mu_hipotesis, sigma_poblacional, alpha, tipo_prueba):
    n = len(datos)
    media_muestral = np.mean(datos)
    z_stat = (media_muestral - mu_hipotesis) / (sigma_poblacional / np.sqrt(n))

    if tipo_prueba == 'Cola izquierda':
        p_value = stats.norm.cdf(z_stat)
        z_critico = stats.norm.ppf(alpha)
    elif tipo_prueba == 'Cola derecha':
        p_value = 1 - stats.norm.cdf(z_stat)
        z_critico = stats.norm.ppf(1 - alpha)
    else:
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        z_critico = stats.norm.ppf(1 - alpha / 2)

    return {
        "media_muestral": media_muestral,
        "n": n,
        "z_stat": z_stat,
        "p_value": p_value,
        "z_critico": z_critico,
        "rechazar_h0": p_value < alpha
    }

def render_stats_tab():
    st.header("Configuración de la Prueba de Hipótesis (Z-Test)")

    if 'datos' not in st.session_state or st.session_state['datos'].empty:
        st.warning("Primero debes generar o subir datos en el Paso 1.")
        return

    df = st.session_state['datos']
    columna_datos = df.select_dtypes(include=[np.number]).columns[0]
    datos_crudos = df[columna_datos].dropna().values

    if len(datos_crudos) < 30:
        st.error(f"El tamaño de muestra actual (n={len(datos_crudos)}) es menor a 30.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<i class="fa-solid fa-sliders fa-icon"></i> **Parámetros de la Prueba**', unsafe_allow_html=True)
        mu_hipotesis = st.number_input("Media bajo la Hipótesis Nula (H0)", value=100.0, key="mu_z_stat")
        sigma_poblacional = st.number_input("Desviación estándar (σ)", value=15.0, min_value=0.1, key="sigma_z_stat")

    with col2:
        st.markdown('<i class="fa-solid fa-crosshairs fa-icon"></i> **Condiciones Críticas**', unsafe_allow_html=True)
        alpha = st.selectbox("Nivel de significancia (α)", options=[0.01, 0.05, 0.10], index=1, key="alpha_z_stat")
        tipo_prueba = st.radio("Tipo de prueba (H1)", options=['Bilateral', 'Cola izquierda', 'Cola derecha'], key="tipo_z_stat")

    st.divider()

    if st.button("Calcular Prueba Estadística", type="primary"):
        resultados = calcular_prueba_z(datos_crudos, mu_hipotesis, sigma_poblacional, alpha, tipo_prueba)

        st.session_state['parametros_z'] = {
            "mu": mu_hipotesis, "sigma": sigma_poblacional, "alpha": alpha, "tipo": tipo_prueba
        }

        with st.spinner("IA analizando resultados..."):
            api_key = os.getenv("GEMINI_API_KEY")
            st.session_state['resumen_hover'] = generar_resumen_rapido(st.session_state['parametros_z'], resultados, api_key)

        st.session_state['resultados_z'] = resultados

    if 'resultados_z' in st.session_state:
        res = st.session_state['resultados_z']
        hover_text = st.session_state.get('resumen_hover', "Pasa el mouse para ver la explicación.")

        st.markdown('<i class="fa-solid fa-chart-bar fa-icon"></i> **Resultados de la Prueba Z**', unsafe_allow_html=True, help=hover_text)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Estadístico Z", f"{res['z_stat']:.4f}")
        m2.metric("P-Value", f"{res['p_value']:.4f}")
        m3.metric("Z Crítico", f"{res['z_critico']:.4f}")
        m4.metric("Tamaño Muestra (n)", res['n'])

        if res['rechazar_h0']:
            st.error("**Decisión:** Se RECHAZA H0. Hay una diferencia significativa.")
        else:
            st.success("**Decisión:** NO se rechaza H0. Todo parece dentro de lo normal.")