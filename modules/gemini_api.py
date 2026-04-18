import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def render_ai_tab():
    st.header("Análisis Automatizado con Gemini AI")
    st.markdown("Deja que la IA interprete tus resultados de forma sencilla y directa.")

    api_key = os.getenv("GEMINI_API_KEY")
    st.divider()

    if 'resultados_z' not in st.session_state:
        st.warning("Necesitas calcular primero la Prueba Z en el Paso 2.")
        return

    resultados = st.session_state['resultados_z']
    params = st.session_state['parametros_z']

    st.markdown('<i class="fa-solid fa-terminal fa-icon"></i> **Contexto actual para la IA:**', unsafe_allow_html=True)
    st.info(f"**Prueba:** {params['tipo']} | **H0 (Media):** {params['mu']} | **Alpha:** {params['alpha']}\n\n**Resultados:** Z = {resultados['z_stat']:.4f}, p-value = {resultados['p_value']:.4f}")

    if st.button("Generar Interpretación", type="primary"):
        if not api_key:
            st.error("No se encontró la API Key. Verifica tu archivo .env.")
            return
        try:
            genai.configure(api_key=api_key)
            modelo = genai.GenerativeModel('gemini-2.5-flash')
            prompt = f"""
            Actúa como un analista de datos amigable, casual y muy directo. 
            Acabo de realizar una prueba estadística con los siguientes resultados:
            - Lo que esperábamos (Media ideal): {params['mu']}
            - Tipo de prueba: {params['tipo']}
            - P-value obtenido: {resultados['p_value']:.4f}
            - Decisión del sistema: {'Rechazar H0 (Hay una diferencia real)' if resultados['rechazar_h0'] else 'No rechazar H0 (No hay diferencia real)'}
            Escribe una conclusión de máximo 2 párrafos en palabras sencillas, sin jerga técnica.
            Ve directo al grano: dime si encontramos algo fuera de lo común o si todo está dentro de lo normal.
            """
            with st.spinner("Gemini está traduciendo los números a lenguaje humano..."):
                respuesta = modelo.generate_content(prompt)
            st.success("¡Análisis completado!")
            st.write(respuesta.text)
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {e}")