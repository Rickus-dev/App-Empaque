import streamlit as st
import re

st.set_page_config(page_title="Validador Kaeser Pro", layout="centered")

st.title("📦 Sistema Poka-Yoke V7")
st.subheader("Filtro Quirúrgico Anti-Basura")

if 'empaque' not in st.session_state:
    st.session_state.empaque = {}

st.write("### Paso 1: Escaneo del Talón")
texto = st.text_area("Pega aquí el texto OCR del documento:", height=150)

if st.button("Procesar Orden", use_container_width=True):
    # Convertimos todo a mayúsculas para estandarizar la lectura de la cámara
    texto_limpio = texto.upper()
    
    # V7: ADN Quirúrgico. 
    # 1. Ignora fechas.
    # 2. Ignora dimensiones (cualquier bloque que contenga una 'X').
    # 3. Ignora RFC, sellos, cantidades pegadas y números de dirección.
    patron_codigo = r'\b(?!\d{2}\.\d{2}\.\d{4}\b)(?![A-Z0-9\.-]*X[A-Z0-9\.-]*\b)(?![A-Z0-9\.-]*(?:KCM|ENTREG|PZA|NO\.)[A-Z0-9\.-]*\b)(?:\d{1,2}\.\d{4}\.[A-Z0-9]+|[A-Z0-9]{4,8}\.\d+|[A-Z]{2,4}\d{2,4}-\d+|(?=[A-Z0-9\.-]*[A-Z])(?=[A-Z0-9\.-]*\d)[A-Z0-9]{8,15})\b'
    
    codigos = re.findall(patron_codigo, texto_limpio)
    
    # Extracción de piezas reales
    patron_cant = r'(\d+(?:\.\d+)?)\s*PZA'
    cantidades = re.findall(patron_cant, texto_limpio)
    
    st.session_state.empaque = {}
    st.session_state.alerta_sello = False
    
    if codigos:
        for i, codigo in enumerate(codigos):
            if i < len(cantidades):
                # int(float()) repara los errores de pluma (ej. 4.09 -> 4)
                st.session_state.empaque[codigo] = int(float(cantidades[i]))
            else:
                # Si el sello tapó el PZA del último código, asigna 1 pieza por instinto de supervivencia
                st.session_state.empaque[codigo] = 1
                st.session_state.alerta_sello = True
    else:
        st.session_state.empaque = {"ERROR": True}
         
    st.session_state.debug_info = f"🔍 Códigos Limpios: {codigos} | 📦 Piezas: {cantidades}"
    st.rerun()

if st.session_state.empaque:
    st.write("---")
    if "ERROR" in st.session_state.empaque:
        st.error("⚠️ No se detectaron códigos de material válidos. Revisa el texto escaneado.")
    else:
        st.write("### 🎯 Objetivos de Empaque:")
        
        # Alerta táctica si el sello tapó el texto
        if st.session_state.get("alerta_sello"):
             st.warning("⚠️ Nota: El sello de ALMACÉN o tus marcas a pluma ocultaron la palabra 'PZA' en los últimos renglones. El sistema asignó 1 pieza por defecto al final para no detener la operación.")
             
        for codigo, cant in st.session_state.empaque.items():
            st.success(f"Material: **{codigo}** ➡️ Faltan: **{cant}** piezas")
            
        st.info("📦 Caja inicializada. Lista para validación física.")
