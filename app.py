import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="FN_MARKET - Emergencias y Seguridad", layout="wide", initial_sidebar_state="expanded")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .report-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #262730;
        margin-bottom: 10px;
        border-left: 5px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADO (SIMULACIÓN DB) ---
if 'ambulancias' not in st.session_state:
    st.session_state.ambulancias = pd.DataFrame({
        'ID': ['AMB-001', 'AMB-002', 'AMB-003'],
        'Lat': [19.4326, 19.4290, 19.4350],
        'Lon': [-99.1332, -99.1350, -99.1300],
        'Estado': ['Disponible', 'Disponible', 'Ocupada'],
        'Tipo': ['Ambulancia'] * 3
    })

if 'patrullas' not in st.session_state:
    st.session_state.patrullas = pd.DataFrame({
        'ID': ['PAT-101', 'PAT-102', 'PAT-103'],
        'Lat': [19.4310, 19.4340, 19.4300],
        'Lon': [-99.1320, -99.1340, -99.1310],
        'Estado': ['Patrullando', 'En Alerta', 'Patrullando'],
        'Tipo': ['Patrulla'] * 3
    })

if 'incidentes' not in st.session_state:
    st.session_state.incidentes = []

if 'solicitud_ambulancia_activa' not in st.session_state:
    st.session_state.solicitud_ambulancia_activa = None

# --- NAVEGACIÓN PRINCIPAL ---
st.title("�️ FN_MARKET: Centro de Comando")

tab1, tab2, tab3 = st.tabs(["🚑 Solicitar Ambulancia", "🚨 Reportar Robo/Seguridad", "🗺️ Mapa en Tiempo Real"])

# --- TAB 1: AMBULANCIAS ---
with tab1:
    st.header("Servicio Médico de Urgencia")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📋 Datos del Paciente")
        with st.form("form_ambulancia"):
            tipo_emergencia = st.selectbox("Tipo de Emergencia", ["🔴 Crítico (Paro, Trauma)", "🟡 Urgente (Fractura, Dolor)", "🟢 Moderado (Consulta)"])
            sintomas = st.text_area("Descripción de Síntomas")
            ubicacion_manual = st.text_input("Ubicación (Si es diferente a GPS actual)")
            
            # Simulación GPS
            user_lat = 19.4326 + np.random.uniform(-0.001, 0.001)
            user_lon = -99.1332 + np.random.uniform(-0.001, 0.001)
            
            submit_amb = st.form_submit_button("🚨 SOLICITAR UNIDAD AHORA")
            
            if submit_amb:
                st.session_state.solicitud_ambulancia_activa = {
                    'tipo': tipo_emergencia,
                    'hora': datetime.now().strftime("%H:%M"),
                    'lat': user_lat,
                    'lon': user_lon,
                    'estado': 'En camino'
                }
                st.success("¡Solicitud enviada! Buscando unidad más cercana...")
                time.sleep(1)
                st.rerun()

    with col2:
        if st.session_state.solicitud_ambulancia_activa:
            st.info(f"✅ Unidad asignada: AMB-001")
            st.metric(label="Tiempo Estimado de Llegada (ETA)", value="7 min", delta="-1 min")
            st.map(pd.DataFrame({
                'lat': [user_lat, 19.4326],
                'lon': [user_lon, -99.1332],
                'color': ['#0000FF', '#FF0000']
            }), zoom=14)
            if st.button("Cancelar Solicitud"):
                st.session_state.solicitud_ambulancia_activa = None
                st.rerun()
        else:
            st.markdown("#### 🏥 Ambulancias Disponibles en tu Zona")
            st.dataframe(st.session_state.ambulancias[['ID', 'Estado']], use_container_width=True)

# --- TAB 2: SEGURIDAD ---
with tab2:
    st.header("Sistema de Alerta Ciudadana")
    
    col_alert, col_map_small = st.columns([1, 2])
    
    with col_alert:
        st.error("BOTÓN DE PÁNICO")
        if st.button("🆘 ALERTA SILENCIOSA INMEDIATA", type="primary"):
            st.toast("Alerta enviada a patrullas cercanas y contactos de emergencia.", icon="🤫")
            # Registrar incidente automático
            st.session_state.incidentes.append({
                'tipo': 'Pánico',
                'desc': 'Alerta silenciosa activada',
                'lat': 19.4326,
                'lon': -99.1332,
                'hora': datetime.now().strftime("%H:%M")
            })
        
        st.markdown("---")
        st.markdown("### Reportar Incidente")
        with st.form("form_robo"):
            tipo_robo = st.selectbox("Tipo de Incidente", ["Robo en Curso", "Actividad Sospechosa", "Persona Siguiéndome"])
            desc_robo = st.text_area("Descripción (Agresores, Vehículos)")
            foto = st.file_uploader("Adjuntar Evidencia (Foto/Video)", type=['png', 'jpg', 'mp4'])
            
            if st.form_submit_button("Enviar Reporte a la Comunidad"):
                nuevo_incidente = {
                    'tipo': tipo_robo,
                    'desc': desc_robo,
                    'lat': 19.4326 + np.random.uniform(-0.002, 0.002),
                    'lon': -99.1332 + np.random.uniform(-0.002, 0.002),
                    'hora': datetime.now().strftime("%H:%M")
                }
                st.session_state.incidentes.append(nuevo_incidente)
                st.success("Reporte registrado y notificado a vecinos.")
    
    with col_map_small:
        st.markdown("### 📢 Alertas Recientes en tu Zona")
        if st.session_state.incidentes:
            for inc in st.session_state.incidentes[-3:]:
                st.markdown(f"""
                <div class="report-card">
                    <b>{inc['tipo']}</b> - {inc['hora']}<br>
                    {inc['desc']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No hay reportes recientes en tu zona. ¡Mantente seguro!")

# --- TAB 3: MAPA GLOBAL ---
with tab3:
    st.header("Mapa en Tiempo Real")
    
    # Combinar datos para el mapa
    map_layers = []
    
    # Ambulancias (Verde)
    df_amb = st.session_state.ambulancias.copy()
    df_amb['color'] = '#00FF00'
    df_amb['size'] = 100
    
    # Patrullas (Azul)
    df_pat = st.session_state.patrullas.copy()
    df_pat['color'] = '#0000FF'
    df_pat['size'] = 100
    
    # Incidentes (Rojo)
    incident_data = []
    for inc in st.session_state.incidentes:
        incident_data.append({'lat': inc['lat'], 'lon': inc['lon'], 'color': '#FF0000', 'size': 50, 'ID': inc['tipo']})
    
    df_inc = pd.DataFrame(incident_data) if incident_data else pd.DataFrame(columns=['lat', 'lon', 'color', 'size', 'ID'])
    
    # Unir todo
    if not df_inc.empty:
        map_data = pd.concat([
            df_amb[['Lat', 'Lon', 'color', 'size']].rename(columns={'Lat': 'lat', 'Lon': 'lon'}),
            df_pat[['Lat', 'Lon', 'color', 'size']].rename(columns={'Lat': 'lat', 'Lon': 'lon'}),
            df_inc[['lat', 'lon', 'color', 'size']]
        ], ignore_index=True)
    else:
        map_data = pd.concat([
            df_amb[['Lat', 'Lon', 'color', 'size']].rename(columns={'Lat': 'lat', 'Lon': 'lon'}),
            df_pat[['Lat', 'Lon', 'color', 'size']].rename(columns={'Lat': 'lat', 'Lon': 'lon'})
        ], ignore_index=True)

    st.map(map_data, color='color', size='size', zoom=13)
    
    st.markdown("**Leyenda:** 🟢 Ambulancia | 🔵 Patrulla | 🔴 Incidente Reportado")

# --- SIDEBAR: SIMULADOR ---
st.sidebar.title("🔧 Panel de Control")
st.sidebar.info("Modo Desarrollador Activo")
if st.sidebar.button("Reiniciar Datos"):
    st.session_state.clear()
    st.rerun()