import streamlit as st
import re

st.set_page_config(page_title="Validador Kaeser Pro", layout="centered")

st.title("📦 Sistema Poka-Yoke")
st.subheader("Cero Errores de Empaque")

if 'empaque' not in st.session_state:
    st.session_state.empaque = {}

st.write("### Paso 1: Escaneo del Talón")
texto = st.text_area("Pega aquí el texto del documento:", height=150)

if st.button("Procesar Orden", use_container_width=True):
    # Busca códigos y cantidades en formato PZA (ignora los N/A automáticamente)
    items = re.findall(r'([\w\.-]+)\s+.*?(\d+\.\d+)\s+PZA', texto)
    if items:
        st.session_state.empaque = {codigo: int(float(cant)) for codigo, cant in items}
        st.rerun()
    else:
        st.error("No se detectaron materiales válidos.")

if st.session_state.empaque:
    st.write("---")
    st.write("### 🎯 Objetivos de Empaque:")
    for codigo, cant in st.session_state.empaque.items():
        st.warning(f"Material: **{codigo}** ➡️ Faltan: **{cant}** piezas")
    
    st.success("Caja inicializada y blindada. Lista para validación física.")
  
