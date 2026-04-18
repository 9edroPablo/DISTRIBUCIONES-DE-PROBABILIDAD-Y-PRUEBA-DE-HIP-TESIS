import streamlit as st
import streamlit.components.v1 as components
import os
import time
from dotenv import load_dotenv
from modules.data_handler import render_data_tab
from modules.stats_engine import render_stats_tab
from modules.plots import render_plots_tab
from modules.gemini_api import render_ai_tab

load_dotenv()
st.set_page_config(page_title="Z-Test & AI Analytics", page_icon="⚡", layout="wide")

ICON_COLOR = "#00f2fe"

def aplicar_estilos_personalizados():
    if os.path.exists("style.css"):
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown(f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
    .fa-icon {{
        color: {ICON_COLOR};
        margin-right: 8px;
    }}

    [data-testid="stSpinner"] i {{
        display: none !important;
    }}
    [data-testid="stSpinner"] > div {{
        gap: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
    }}
    [data-testid="stSpinner"] [data-testid="stMarkdownContainer"] p {{
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        color: #ffffff;
    }}
    [data-testid="stSpinner"] [data-testid="stMarkdownContainer"] p::before {{
        content: "⠋";
        display: inline-block;
        font-family: monospace;
        font-size: 1.8rem;
        color: {ICON_COLOR};
        margin-right: 12px;
        animation: braille-spin 0.8s steps(10, end) infinite;
    }}
    @keyframes braille-spin {{
        0%  {{ content: "⠋"; }} 10% {{ content: "⠙"; }} 20% {{ content: "⠹"; }}
        30% {{ content: "⠸"; }} 40% {{ content: "⠼"; }} 50% {{ content: "⠴"; }}
        60% {{ content: "⠦"; }} 70% {{ content: "⠧"; }} 80% {{ content: "⠇"; }}
        90% {{ content: "⠏"; }}
    }}
    </style>
    """, unsafe_allow_html=True)

aplicar_estilos_personalizados()

particulas_js = """
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    body { margin: 0; padding: 0; overflow: hidden; background: linear-gradient(-45deg, #0e1117, #1e2638, #001220, #1f1423); background-size: 400% 400%; animation: gradientBG 15s ease infinite; }
    @keyframes gradientBG { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    #particles-js { position: absolute; width: 100vw; height: 100vh; z-index: 1; }
  </style>
</head>
<body>
  <div id="particles-js"></div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": { "value": 90, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": "#00f2fe" },
        "shape": { "type": "circle" },
        "opacity": { "value": 0.5 },
        "size": { "value": 2.5, "random": true },
        "line_linked": { "enable": true, "distance": 150, "color": "#4facfe", "opacity": 0.4, "width": 1.5 },
        "move": { "enable": true, "speed": 2, "random": true, "out_mode": "out" }
      },
      "interactivity": {
        "detect_on": "window",
        "events": { "onhover": { "enable": true, "mode": "repulse" }, "onclick": { "enable": true, "mode": "push" } },
        "modes": { "repulse": { "distance": 120 }, "push": { "particles_nb": 4 } }
      }
    });
    const myIframe = window.frameElement;
    if (myIframe) {
        myIframe.style.position = 'fixed';
        myIframe.style.top = '0'; myIframe.style.left = '0';
        myIframe.style.width = '100vw'; myIframe.style.height = '100vh';
        myIframe.style.zIndex = '0'; myIframe.style.border = 'none';
        myIframe.style.pointerEvents = 'none';
    }
    window.parent.document.addEventListener('mousemove', function(e) {
        var event = new MouseEvent('mousemove', { clientX: e.clientX, clientY: e.clientY });
        window.dispatchEvent(event);
    });
  </script>
</body>
</html>
"""
components.html(particulas_js, height=0)

st.markdown("<div style='height: 25vh;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="sticky-hero">
    <h1 class="animated-title">
        <i class="fa-solid fa-bolt fa-icon"></i> Analizador Estadístico Neural
    </h1>
    <p class="hero-subtitle">Pipeline interactivo para la toma de decisiones estadísticas con IA.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True)

with st.expander("PASO 1", expanded=('datos' not in st.session_state)):
    st.markdown('<i class="fa-solid fa-folder-open fa-icon"></i> **Generación o Carga de Datos**', unsafe_allow_html=True)
    render_data_tab()

if 'datos' in st.session_state and not st.session_state['datos'].empty:
    with st.expander("PASO 2", expanded=('resultados_z' not in st.session_state)):
        st.markdown('<i class="fa-solid fa-flask-vial fa-icon"></i> **Configuración de la Prueba Z**', unsafe_allow_html=True)
        render_stats_tab()

if 'resultados_z' in st.session_state:
    with st.expander("PASO 3", expanded=True):
        st.markdown('<i class="fa-solid fa-chart-line fa-icon"></i> **Visualización de Resultados**', unsafe_allow_html=True)
        render_plots_tab()

    with st.expander("PASO 4", expanded=True):
        st.markdown('<i class="fa-solid fa-microchip fa-icon"></i> **Interpretación con IA**', unsafe_allow_html=True)
        render_ai_tab()


