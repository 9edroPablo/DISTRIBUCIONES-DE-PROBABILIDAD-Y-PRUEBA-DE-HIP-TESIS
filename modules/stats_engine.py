import streamlit as st
import numpy as np
import scipy.stats as stats


def calcular_prueba_z(datos, mu_hipotesis, sigma_poblacional, alpha, tipo_prueba):
    """
    Evalúa una prueba de hipótesis Z para una muestra.
    """
    n = len(datos)
    media_muestral = np.mean(datos)
    
    z_stat = (media_muestral - mu_hipotesis) / (sigma_poblacional / np.sqrt(n))
    
    if tipo_prueba == 'Cola izquierda':
        p_value = stats.norm.cdf(z_stat)
        z_critico = stats.norm.ppf(alpha)
        rechazar_h0 = p_value < alpha
        
    elif tipo_prueba == 'Cola derecha':
        p_value = 1 - stats.norm.cdf(z_stat)
        z_critico = stats.norm.ppf(1 - alpha)
        rechazar_h0 = p_value < alpha
        
    elif tipo_prueba == 'Bilateral':
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        z_critico = stats.norm.ppf(1 - alpha / 2) 
        rechazar_h0 = p_value < alpha
        
    else:
        raise ValueError("Tipo de prueba no válido. Usa: 'Cola izquierda', 'Cola derecha' o 'Bilateral'.")
        
    return {
        "media_muestral": media_muestral,
        "n": n,
        "z_stat": z_stat,
        "p_value": p_value,
        "z_critico": z_critico,
        "rechazar_h0": rechazar_h0
    }


def render_stats_tab():
    st.header("Configuración de la Prueba de Hipótesis (Z-Test)")
    

    if 'datos' not in st.session_state or st.session_state['datos'].empty:
        st.warning("⚠️ Primero debes generar o subir datos en la pestaña '1. Carga de Datos'.")
        return
    
  
    df = st.session_state['datos']
    columna_datos = df.select_dtypes(include=[np.number]).columns[0]
    datos_crudos = df[columna_datos].dropna().values
    
    
    n_actual = len(datos_crudos)
    if n_actual < 30:
        st.error(f"El tamaño de muestra actual (n={n_actual}) es menor a 30. La prueba Z asume n >= 30.")
        return
        
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parámetros de la Prueba")
        mu_hipotesis = st.number_input("Media bajo la Hipótesis Nula (H0)", value=100.0)
        sigma_poblacional = st.number_input("Desviación estándar poblacional conocida (σ)", value=15.0, min_value=0.1)
        
    with col2:
        st.subheader("Condiciones Críticas")
        alpha = st.selectbox("Nivel de significancia (α)", options=[0.01, 0.05, 0.10], index=1)
        tipo_prueba = st.radio("Tipo de prueba (H1)", options=['Bilateral', 'Cola izquierda', 'Cola derecha'])
        
    st.divider()
    

    if st.button("Calcular Prueba Estadíostica", type="primary"):
     
        resultados = calcular_prueba_z(
            datos=datos_crudos,
            mu_hipotesis=mu_hipotesis,
            sigma_poblacional=sigma_poblacional,
            alpha=alpha,
            tipo_prueba=tipo_prueba
        )
        
        
        st.session_state['resultados_z'] = resultados
        st.session_state['parametros_z'] = {
            "mu": mu_hipotesis, "sigma": sigma_poblacional, "alpha": alpha, "tipo": tipo_prueba
        }
        
       
        st.subheader(" Resultados de la Prueba Z")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Estadístico Z", f"{resultados['z_stat']:.4f}")
        m2.metric("P-Value", f"{resultados['p_value']:.4f}")
        m3.metric("Z Crítico", f"{resultados['z_critico']:.4f}")
        m4.metric("Tamaño Muestra (n)", resultados['n'])
        
        
        if resultados['rechazar_h0']:
            st.error(f"**Decisión Automática:** Se RECHAZA la hipótesis nula (H0). El p-value ({resultados['p_value']:.4f}) es menor que alpha ({alpha}).")
        else:
            st.success(f"**Decisión Automática:** NO se rechaza la hipótesis nula (H0). El p-value ({resultados['p_value']:.4f}) es mayor que alpha ({alpha}).")