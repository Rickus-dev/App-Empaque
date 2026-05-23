import streamlit as st
import re

st.set_page_config(page_title="Validador Kaeser Pro", layout="centered")

st.title("📦 Sistema Poka-Yoke V4")
st.subheader("Motor de Reconocimiento de Patrones")

if 'empaque' not in st.session_state:
    st.session_state.empaque = {}

st.write("### Paso 1: Escaneo del Talón")
texto = st.text_area("Pega aquí el texto OCR del documento:", height=150)

if st.button("Procesar Orden", use_container_width=True):
    # 1. ADN Kaeser: Extrae TODOS los códigos que cumplan la morfología estricta, sin importar dónde estén.
    patron_codigo = r'\b(\d{1,2}\.\d{4}[A-Z0-9\.]*|\d{6}\.\d{5}|[A-Z]{2,4}\d{2,4}-\d+)\b'
    codigos = re.findall(patron_codigo, texto, re.IGNORECASE)
    
    # 2. Extrae TODAS las cantidades que estén ligadas a "PZA"
    patron_cant = r'(\d+(?:\.\d+)?)\s*PZA'
    cantidades = re.findall(patron_cant, texto, re.IGNORECASE)
    
    # 3. Emparejamiento táctico (Cierra la brecha de las columnas)
    if codigos and cantidades and len(codigos) == len(cantidades):
        st.session_state.empaque = {codigos[i]: int(float(cantidades[i])) for i in range(len(codigos))}
    elif codigos and not cantidades: 
        # Sistema de emergencia: Si el OCR no vio la palabra PZA, asume 1 pieza para no bloquearte
        st.session_state.empaque = {c: 1 for c in codigos}
    else:
         st.session_state.empaque = {"ERROR": True}
         
    st.session_state.debug_info = f"🔍 Códigos detectados: {codigos} | 📦 Cantidades detectadas: {cantidades}"
    st.rerun()

if st.session_state.empaque:
    st.write("---")
    if "ERROR" in st.session_state.empaque:
        st.error("⚠️ Desfase de lectura: La cámara leyó una cantidad distinta de códigos y de piezas. Vuelve a escanear solo el área de la tabla.")
        st.info(st.session_state.get("debug_info", ""))
    else:
        st.write("### 🎯 Objetivos de Empaque:")
        for codigo, cant in st.session_state.empaque.items():
            st.warning(f"Material: **{codigo}** ➡️ Faltan: **{cant}** piezas")
        st.success("Caja inicializada. Lista para escaneo físico.")
