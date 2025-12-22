import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="🚨 AmbuApp - Ambulancias a la Carta", layout="wide", initial_sidebar_state="expanded")

# --- SIMULACIÓN DE BASE DE DATOS Y SESIÓN ---
if 'solicitudes_activas' not in st.session_state:
    st.session_state.solicitudes_activas = pd.DataFrame(columns=['ID', 'Paciente', 'Direccion', 'Lat', 'Lon', 'Estado', 'Ambulancia Asignada', 'Tiempo Estimado'])
if 'ambulancias_disponibles' not in st.session_state:
    st.session_state.ambulancias_disponibles = pd.DataFrame({
        'ID': ['AMB-001', 'AMB-002', 'AMB-003', 'AMB-004'],
        'Lat': [19.4326 + np.random.uniform(-0.05, 0.05), 19.4326 + np.random.uniform(-0.05, 0.05), 19.4326 + np.random.uniform(-0.05, 0.05), 19.4326 + np.random.uniform(-0.05, 0.05)],
        'Lon': [-99.1332 + np.random.uniform(-0.05, 0.05), -99.1332 + np.random.uniform(-0.05, 0.05), -99.1332 + np.random.uniform(-0.05, 0.05), -99.1332 + np.random.uniform(-0.05, 0.05)],
        'Estado': ['Disponible', 'Disponible', 'Disponible', 'Disponible']
    })
if 'solicitud_enviada' not in st.session_state:
    st.session_state.solicitud_enviada = False

# --- TÍTULO Y DESCRIPCIÓN ---
st.title("🚑 AmbuApp: Tu Ambulancia, Rápido y Seguro")
st.markdown("### Solicita una ambulancia en tiempo real. Estamos para ayudarte.")

# --- FORMULARIO DE SOLICITUD ---
st.header("1. ¿Dónde necesitas la ambulancia?")

with st.form("solicitud_form"):
    nombre_paciente = st.text_input("Nombre del Paciente", placeholder="Ej: Juan Pérez")
    direccion_recogida = st.text_input("Dirección de Recogida", placeholder="Ej: Calle Falsa 123, Colonia Centro")
    motivo_emergencia = st.text_area("Motivo de la Emergencia", placeholder="Ej: Caída, dificultad para respirar, accidente automovilístico...")
    
    # Simulación de Geolocalización (Ciudad de México como referencia)
    st.markdown("*(Simulación de tu ubicación en Ciudad de México para fines de demostración)*")
    ubicacion_lat = st.slider("Latitud (Simulada)", min_value=19.0, max_value=20.0, value=19.4326)
    ubicacion_lon = st.slider("Longitud (Simulada)", min_value=-100.0, max_value=-98.0, value=-99.1332)
    
    submitted = st.form_submit_button("🚨 Solicitar Ambulancia Ahora")

if submitted and not st.session_state.solicitud_enviada:
    if nombre_paciente and direccion_recogida and motivo_emergencia:
        # Asignar una ambulancia disponible (simulado)
        ambulancias_libres = st.session_state.ambulancias_disponibles[st.session_state.ambulancias_disponibles['Estado'] == 'Disponible']
        
        if not ambulancias_libres.empty:
            ambulancia_asignada = ambulancias_libres.sample(1).iloc[0]
            
            # Calcular tiempo estimado (simulado, basado en distancia aleatoria)
            tiempo_estimado = np.random.randint(5, 20) 
            
            nueva_solicitud = {
                'ID': f"SOL-{len(st.session_state.solicitudes_activas) + 1:04d}",
                'Paciente': nombre_paciente,
                'Direccion': direccion_recogida,
                'Lat': ubicacion_lat,
                'Lon': ubicacion_lon,
                'Estado': 'Pendiente',
                'Ambulancia Asignada': ambulancia_asignada['ID'],
                'Tiempo Estimado': f"{tiempo_estimado} minutos"
            }
            st.session_state.solicitudes_activas.loc[len(st.session_state.solicitudes_activas)] = nueva_solicitud
            
            # Cambiar estado de la ambulancia asignada a 'En Servicio' (simulado)
            idx = st.session_state.ambulancias_disponibles[st.session_state.ambulancias_disponibles['ID'] == ambulancia_asignada['ID']].index
            st.session_state.ambulancias_disponibles.loc[idx, 'Estado'] = 'En Servicio'
            
            st.success(f"✅ ¡Solicitud enviada! Ambulancia {ambulancia_asignada['ID']} en camino. Tiempo estimado: {tiempo_estimado} minutos.")
            st.session_state.solicitud_enviada = True
            time.sleep(2) # Pausa para que el usuario lea el mensaje
            st.rerun() # Recargar para ver el estado actualizado
        else:
            st.error("❌ No hay ambulancias disponibles en este momento. Por favor, inténtalo de nuevo o llama al 911.")
    else:
        st.error("Por favor, rellena todos los campos.")
elif st.session_state.solicitud_enviada:
    st.info("Ya has enviado una solicitud. Revisa el estado abajo.")

st.divider()

# --- MAPA Y ESTADO DE LAS AMBULANCIAS ---
st.header("2. Mapa y Estado Actual")

# Mostrar las ambulancias y la solicitud del usuario en un mapa
map_data = pd.DataFrame({
    'lat': st.session_state.ambulancias_disponibles['Lat'].tolist() + ([ubicacion_lat] if st.session_state.solicitud_enviada else []),
    'lon': st.session_state.ambulancias_disponibles['Lon'].tolist() + ([ubicacion_lon] if st.session_state.solicitud_enviada else []),
    'size': [100 if s == 'Disponible' else 150 for s in st.session_state.ambulancias_disponibles['Estado']] + ([200] if st.session_state.solicitud_enviada else []),
    'color': ['#00FF00' if s == 'Disponible' else '#FF0000' for s in st.session_state.ambulancias_disponibles['Estado']] + (['#0000FF'] if st.session_state.solicitud_enviada else []),
    'label': st.session_state.ambulancias_disponibles['ID'].tolist() + (['Tu Solicitud'] if st.session_state.solicitud_enviada else [])
})

st.map(map_data,
       latitude='lat',
       longitude='lon',
       size='size',
       color='color',
       zoom=10)

st.subheader("Ambulancias y Solicitudes Activas:")
st.dataframe(st.session_state.solicitudes_activas, use_container_width=True)
st.dataframe(st.session_state.ambulancias_disponibles, use_container_width=True)

# --- PANEL DE ADMINISTRACIÓN SIMULADO (Sidebar) ---
st.sidebar.markdown("---")
st.sidebar.subheader("Panel de Operaciones (Simulado)")

selected_amb = st.sidebar.selectbox("Ambulancia para Gestionar", st.session_state.ambulancias_disponibles['ID'].tolist())
new_amb_state = st.sidebar.selectbox("Cambiar Estado a", ['Disponible', 'En Servicio', 'Mantenimiento'])

if st.sidebar.button("Actualizar Estado de Ambulancia"):
    idx = st.session_state.ambulancias_disponibles[st.session_state.ambulancias_disponibles['ID'] == selected_amb].index
    st.session_state.ambulancias_disponibles.loc[idx, 'Estado'] = new_amb_state
    st.sidebar.success(f"Estado de {selected_amb} actualizado a {new_amb_state}")
    st.rerun()

st.sidebar.button("Reiniciar Simulador", on_click=lambda: st.session_state.clear())