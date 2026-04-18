import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Cargar las variables ocultas del archivo .env
load_dotenv()

def render_ai_tab():
    st.header("🤖 Análisis Automatizado con Gemini AI")
    st.markdown("Deja que la Inteligencia Artificial interprete tus resultados estadísticos.")
    
    # 2. Leer la llave secreta
    api_key = os.getenv("GEMINI_API_KEY")
    
    st.divider()
    
    if 'resultados_z' not in st.session_state:
        st.warning("⚠️ Necesitas calcular primero la Prueba Z en la pestaña '3. Prueba Z' para que la IA tenga datos que analizar.")
        return
        
    resultados = st.session_state['resultados_z']
    params = st.session_state['parametros_z']
    
    st.subheader("Contexto actual para la IA:")
    st.info(f"**Prueba:** {params['tipo']} | **H0 (Media):** {params['mu']} | **Alpha:** {params['alpha']} \n\n **Resultados:** Z = {resultados['z_stat']:.4f}, p-value = {resultados['p_value']:.4f}")
    
    if st.button("Generar Interpretación Estadística", type="primary"):
        # Verificamos que el .env haya cargado bien
        if not api_key:
            st.error("No se encontró la API Key. Verifica que el archivo .env exista y tenga la variable GEMINI_API_KEY.")
            return
            
        try:
            # ==========================================
            # 3. AQUÍ SE COLOCA LA CONFIGURACIÓN DEL MODELO
            # ==========================================
            genai.configure(api_key=api_key)
            modelo = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Actúa como un profesor universitario experto en estadística. 
            Acabo de realizar una prueba de hipótesis Z con los siguientes parámetros y resultados:
            
            - Hipótesis Nula (Media): {params['mu']}
            - Nivel de significancia (Alpha): {params['alpha']}
            - Tipo de prueba: {params['tipo']}
            - Estadístico Z obtenido: {resultados['z_stat']:.4f}
            - Valor crítico de Z: {resultados['z_critico']:.4f}
            - P-value obtenido: {resultados['p_value']:.4f}
            - Decisión algorítmica: {'Rechazar H0' if resultados['rechazar_h0'] else 'No rechazar H0'}
            
            Escribe un resumen de máximo 3 párrafos explicando qué significan estos resultados de forma sencilla.
            Explica por qué la decisión final tiene sentido matemáticamente usando el p-value y el alpha.
            Termina con una frase reflexiva sobre los datos.
            """
            
            with st.spinner('Gemini está analizando tus resultados...'):
                respuesta = modelo.generate_content(prompt)
                
            st.success("¡Análisis completado!")
            st.write(respuesta.text)
            
        except Exception as e:
            st.error(f"Ocurrió un error al conectar con Gemini. Detalle técnico: {e}")