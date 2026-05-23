import streamlit as st
import re

st.set_page_config(page_title="Validador Kaeser Pro", layout="centered")

st.title("📦 Sistema Poka-Yoke V6")
st.subheader("Motor OCR de Alta Tolerancia")

if 'empaque' not in st.session_state:
    st.session_state.empaque = {}

st.write("### Paso 1: Escaneo del Talón")
texto = st.text_area("Pega aquí el texto OCR del documento:", height=150)

if st.button("Procesar Orden", use_container_width=True):
    # V6: ADN Definitivo (Atrapa alfanuméricos puros, formatos mixtos y excluye fechas)
    patron_codigo = r'\b(?!\d{2}\.\d{2}\.\d{4}\b)(?:\d+[\.-]\d+[\.-][A-Z0-9\.-]+|(?=[A-Z0-9\.-]*[A-Z])(?=[A-Z0-9\.-]*\d)[A-Z0-9\.-]{6,20}|\d{5,7}\.\d{4,6})\b'
    codigos = re.findall(patron_codigo, texto, re.IGNORECASE)
    
    patron_cant = r'(\d+(?:\.\d+)?)\s*PZA'
    cantidades = re.findall(patron_cant, texto, re.IGNORECASE)
    
    st.session_state.empaque = {}
    st.session_state.alerta_sello = False
    
    if codigos:
        for i, codigo in enumerate(codigos):
            if i < len(cantidades):
                # El int(float()) repara los errores de pluma (ej. 4.09 -> 4)
                st.session_state.empaque[codigo] = int(float(cantidades[i]))
            else:
                # Si el OCR no vio el PZA por culpa del sello, asume 1 pieza por seguridad
                st.session_state.empaque[codigo] = 1
                st.session_state.alerta_sello = True
    else:
        st.session_state.empaque = {"ERROR": True}
         
    st.session_state.debug_info = f"🔍 Códigos: {codigos} | 📦 Piezas: {cantidades}"
    st.rerun()

if st.session_state.empaque:
    st.write("---")
    if "ERROR" in st.session_state.empaque:
        st.error("⚠️ No se detectaron códigos de material. Vuelve a escanear.")
    else:
        st.write("### 🎯 Objetivos de Empaque:")
        
        # Alerta táctica si el sello tapó texto
        if st.session_state.get("alerta_sello"):
             st.warning("⚠️ Nota: El sello o las marcas a pluma ocultaron algunas cantidades. El sistema asignó 1 pieza por defecto a los ítems finales por seguridad.")
             
        for codigo, cant in st.session_state.empaque.items():
            st.success(f"Material: **{codigo}** ➡️ Faltan: **{cant}** piezas")
            
        st.info("📦 Caja inicializada. Lista para validación física.")
        
