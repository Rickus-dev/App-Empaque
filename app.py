import streamlit as st
import re

st.set_page_config(page_title="Validador Kaeser Pro", layout="centered")

st.title("📦 Sistema Poka-Yoke V5")
st.subheader("Motor de Extracción Precisa")

if 'empaque' not in st.session_state:
    st.session_state.empaque = {}

st.write("### Paso 1: Escaneo del Talón")
texto = st.text_area("Pega aquí el texto OCR del documento:", height=150)

if st.button("Procesar Orden", use_container_width=True):
    # V5: Filtro anti-fechas. Exige que haya un punto (.) o una 'E' antes del último bloque alfanumérico
    patron_codigo = r'\b(\d{1,2}\.\d{4}[\.E][A-Z0-9]+|\d{6}\.\d{5,6}|[A-Z]{2,4}\d{2,4}-\d+)\b'
    codigos = re.findall(patron_codigo, texto, re.IGNORECASE)
    
    patron_cant = r'(\d+(?:\.\d+)?)\s*PZA'
    cantidades = re.findall(patron_cant, texto, re.IGNORECASE)
    
    if codigos and cantidades and len(codigos) == len(cantidades):
        st.session_state.empaque = {codigos[i]: int(float(cantidades[i])) for i in range(len(codigos))}
    elif codigos and not cantidades: 
        st.session_state.empaque = {c: 1 for c in codigos}
    else:
         st.session_state.empaque = {"ERROR": True}
         
    st.session_state.debug_info = f"🔍 Códigos: {codigos} | 📦 Piezas: {cantidades}"
    st.rerun()

if st.session_state.empaque:
    st.write("---")
    if "ERROR" in st.session_state.empaque:
        st.error("⚠️ Desfase de lectura. Revisa la caja de diagnóstico abajo para ver qué detectó mal la cámara:")
        st.info(st.session_state.get("debug_info", ""))
    else:
        st.write("### 🎯 Objetivos de Empaque:")
        for codigo, cant in st.session_state.empaque.items():
            st.warning(f"Material: **{codigo}** ➡️ Faltan: **{cant}** piezas")
        st.success("Caja inicializada. Lista para empacar.")
        
