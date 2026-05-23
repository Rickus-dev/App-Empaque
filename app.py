import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Validador Kaeser Pro", layout="centered")

st.title("📦 Sistema Poka-Yoke V8")
st.subheader("Extracción + Auditoría Activa")

# Control de estado de la orden
if 'empaque_confirmado' not in st.session_state:
    st.session_state.empaque_confirmado = False

if not st.session_state.empaque_confirmado:
    st.write("### Paso 1: Escaneo del Talón")
    texto = st.text_area("Pega el texto OCR aquí:", height=100)

    if st.button("Extraer Datos", use_container_width=True):
        texto_limpio = texto.upper()
        
        # Filtro Quirúrgico V7
        patron_codigo = r'\b(?!\d{2}\.\d{2}\.\d{4}\b)(?![A-Z0-9\.-]*X[A-Z0-9\.-]*\b)(?![A-Z0-9\.-]*(?:KCM|ENTREG|PZA|NO\.)[A-Z0-9\.-]*\b)(?:\d{1,2}\.\d{4}\.[A-Z0-9]+|[A-Z0-9]{4,8}\.\d+|[A-Z]{2,4}\d{2,4}-\d+|(?=[A-Z0-9\.-]*[A-Z])(?=[A-Z0-9\.-]*\d)[A-Z0-9]{8,15})\b'
        codigos = re.findall(patron_codigo, texto_limpio)
        
        patron_cant = r'(\d+(?:\.\d+)?)\s*PZA'
        cantidades = re.findall(patron_cant, texto_limpio)
        
        # Estructuración de la Tabla
        datos_tabla = []
        max_len = max(len(codigos), len(cantidades))
        for i in range(max_len):
            c = codigos[i] if i < len(codigos) else "FALTANTE"
            q = int(float(cantidades[i])) if i < len(cantidades) else 1
            datos_tabla.append({"Material": c, "Piezas": q})
        
        if datos_tabla:
            st.session_state.df_empaque = pd.DataFrame(datos_tabla)
        else:
            st.error("⚠️ No se detectaron códigos.")
        st.rerun()

    # Interfaz de Auditoría (Tabla Editable)
    if 'df_empaque' in st.session_state:
        st.warning("⚠️ Ojo: Revisa que Lens no haya cruzado los números. Si hay un error, toca el número y corrígelo.")
        
        # data_editor permite al usuario modificar la tabla en tiempo real
        df_editado = st.data_editor(st.session_state.df_empaque, use_container_width=True, hide_index=True)
        
        if st.button("✅ Confirmar y Bloquear Caja", type="primary", use_container_width=True):
            st.session_state.empaque = dict(zip(df_editado['Material'], df_editado['Piezas']))
            st.session_state.empaque_confirmado = True
            st.rerun()

else:
    # Pantalla de Empaque Físico (Solo se muestra tras confirmar la tabla)
    st.write("### 🎯 Objetivos de Empaque:")
    for codigo, cant in st.session_state.empaque.items():
        st.success(f"Cargar: **{codigo}** ➡️ Faltan: **{cant}** piezas")
        
    st.write("---")
    if st.button("🔄 Cerrar Caja y Nueva Orden", use_container_width=True):
        st.session_state.empaque_confirmado = False
        if 'empaque' in st.session_state: del st.session_state.empaque
        if 'df_empaque' in st.session_state: del st.session_state.df_empaque
        st.rerun()
