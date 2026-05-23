import streamlit as st
import re

st.set_page_config(page_title="Validador Kaeser Pro", layout="centered")

st.title("📦 Sistema Poka-Yoke")

if 'empaque' not in st.session_state:
    st.session_state.empaque = {}

st.write("### Paso 1: Escaneo del Talón")
texto = st.text_area("Pega aquí el texto OCR del documento:", height=150)

if st.button("Procesar Orden", use_container_width=True):
    texto_plano = texto.replace('\n', ' ')
    
    # Regex V3: Correa Corta. Exige que haya max 100 caracteres entre el Código y la palabra PZA
    # El (?:.{1,100}?) crea un puente irrompible que ignora anotaciones a pluma pero no salta párrafos enteros.
    items = re.findall(r'([A-Z0-9]{1,15}[\.-][A-Z0-9]{1,15})\s+(?:.{1,100}?)\s+(\d+\.\d{1,2})\s+PZA', texto_plano, re.IGNORECASE)
    
    if items:
        st.session_state.empaque = {codigo: int(float(cant)) for codigo, cant in items}
    else:
        st.session_state.empaque = {"ERROR": 0}
        
    st.session_state.texto_crudo = texto
    st.rerun()

if st.session_state.empaque:
    st.write("---")
    if "ERROR" in st.session_state.empaque:
        st.error("⚠️ Falla de lectura. No se detectó la estructura de Kaeser. Evidencia de escaneo:")
        st.code(st.session_state.get("texto_crudo", "Nada escrito"))
    else:
        st.write("### 🎯 Objetivos de Empaque:")
        for codigo, cant in st.session_state.empaque.items():
            st.warning(f"Material: **{codigo}** ➡️ Faltan: **{cant}** piezas")
        st.success("Caja inicializada y blindada.")
