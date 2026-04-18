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


# BLOQUE DE PRUEBA LOCAL (Simulación)

if __name__ == "__main__":
    print("--- INICIANDO PRUEBA DEL MOTOR ESTADÍSTICO ---")
    
    np.random.seed(42) 
    datos_simulados = np.random.normal(loc=105, scale=15, size=50)
  
    mu_hipotesis = 100
    sigma_poblacional = 15
    alpha = 0.05
    tipo = 'Cola derecha' 
    
    print(f"Probando H0: mu = {mu_hipotesis} vs H1: mu > {mu_hipotesis} (Cola derecha)")
    print(f"Nivel de significancia (alpha): {alpha}\n")
    
  
    resultados = calcular_prueba_z(
        datos=datos_simulados, 
        mu_hipotesis=mu_hipotesis, 
        sigma_poblacional=sigma_poblacional, 
        alpha=alpha, 
        tipo_prueba=tipo
    )
    
   
    print("RESULTADOS DE LA PRUEBA:")
    for clave, valor in resultados.items():
        print(f"- {clave}: {valor}")