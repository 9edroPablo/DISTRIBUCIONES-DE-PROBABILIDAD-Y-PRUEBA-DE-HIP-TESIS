[Uploading README.md…]()
# ⚡ Analizador Estadístico Neural

Pipeline interactivo para la toma de decisiones estadísticas potenciado con IA. Combina pruebas Z clásicas con interpretación automática via Gemini AI, todo en una interfaz visual construida con Streamlit.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Flash-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/Licencia-MIT-green?style=flat-square)

---

## ✨ Features

- **Generación de datos sintéticos** o carga de CSV propio
- **Prueba Z** configurable (bilateral, cola izquierda, cola derecha)
- **Visualizaciones interactivas** con Plotly: histograma, boxplot y campana de Gauss con zonas de rechazo
- **Interpretación automática** con Gemini AI en lenguaje natural
- **UI personalizada** con partículas animadas, spinner Braille y iconos Font Awesome
- Optimizado para **Safari y navegadores modernos**

---

## 🗂️ Estructura del proyecto

```
├── app.py                  # Entrada principal de la app
├── style.css               # Estilos globales personalizados
├── .env                    # Variables de entorno (no subir a git)
├── requirements.txt        # Dependencias del proyecto
└── modules/
    ├── data_handler.py     # Generación y carga de datos
    ├── stats_engine.py     # Lógica de la prueba Z + resumen rápido IA
    ├── plots.py            # Visualizaciones con Plotly
    └── gemini_api.py       # Interpretación completa con Gemini
```

---

## 🚀 Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/tu-usuario/analizador-estadistico-neural.git
cd analizador-estadistico-neural
```

### 2. Crea un entorno virtual

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura tu API Key de Gemini

Crea un archivo `.env` en la raíz del proyecto:

```env
GEMINI_API_KEY=tu_api_key_aqui
```

Puedes obtener tu API Key gratis en [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Corre la app

```bash
streamlit run app.py
```

---

## 🧪 Cómo usarla

1. **PASO 1** — Genera datos sintéticos con parámetros personalizados o sube tu propio CSV
2. **PASO 2** — Configura la prueba Z: media hipotética, desviación estándar, alpha y tipo de cola
3. **PASO 3** — Explora las visualizaciones: distribución de datos y campana de Gauss con zonas de rechazo
4. **PASO 4** — Genera una interpretación en lenguaje natural con Gemini AI

---

## 📦 Dependencias principales

| Librería | Uso |
|---|---|
| `streamlit` | Framework de la interfaz |
| `numpy` / `scipy` | Cálculos estadísticos |
| `plotly` | Gráficas interactivas |
| `google-generativeai` | Integración con Gemini |
| `python-dotenv` | Manejo de variables de entorno |

Instálalas todas con:

```bash
pip install streamlit numpy scipy plotly google-generativeai python-dotenv
```

---

## ⚠️ Notas importantes

- El archivo `.env` **nunca debe subirse a GitHub**. Asegúrate de tenerlo en tu `.gitignore`
- La prueba Z requiere un mínimo de **n = 30** observaciones
- La interpretación con IA consume tokens de la API de Gemini. El modelo usado es `gemini-2.5-flash` (tier gratuito disponible)

---

## 📄 Licencia

MIT — libre para usar, modificar y distribuir.
