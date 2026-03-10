import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Asistente IA - Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_BASE_URL = "https://asistente-ia-txf0.onrender.com"

# Estilos personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .goal-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1E88E5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Funciones de API
def get_user_by_phone(phone):
    """Obtener usuario por número de teléfono"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/users/{phone}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error al conectar con la API: {e}")
        return None

def get_user_goals(user_id):
    """Obtener objetivos del usuario"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/users/{user_id}/goals")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error al obtener objetivos: {e}")
        return None

def get_goal_progress(goal_id):
    """Obtener progreso de un objetivo"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/goals/{goal_id}/progress")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error al obtener progreso: {e}")
        return None

def get_goal_logs(goal_id, limit=50):
    """Obtener historial de logs de un objetivo"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/goals/{goal_id}/logs?limit={limit}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error al obtener logs: {e}")
        return None

def get_user_stats(user_id):
    """Obtener estadísticas generales del usuario"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/users/{user_id}/stats")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error al obtener estadísticas: {e}")
        return None

# Autenticación
def authenticate():
    """Pantalla de autenticación"""
    st.markdown('<p class="main-header">🎯 Asistente IA - Dashboard</p>', unsafe_allow_html=True)

    st.markdown("""
    ### Bienvenido

    Ingresa tu número de teléfono para acceder a tu dashboard personal.
    """)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        phone = st.text_input(
            "Número de teléfono",
            placeholder="+524444844003",
            help="Ingresa tu número con código de país (ej: +521234567890)"
        )

        if st.button("Acceder", type="primary", use_container_width=True):
            if phone:
                with st.spinner("Verificando..."):
                    user = get_user_by_phone(phone)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.success("¡Acceso concedido!")
                        st.rerun()
                    else:
                        st.error("Usuario no encontrado. Asegúrate de haber usado el bot de WhatsApp primero.")
            else:
                st.warning("Por favor ingresa tu número de teléfono.")

# Función para mostrar estadísticas generales
def show_overview():
    """Página de resumen general"""
    user_id = st.session_state.user['id']
    stats = get_user_stats(user_id)

    if not stats:
        st.error("No se pudieron cargar las estadísticas.")
        return

    # Header
    st.markdown(f'<p class="main-header">👋 Hola, {st.session_state.user.get("name", "Usuario")}!</p>', unsafe_allow_html=True)

    # Estadísticas principales en tarjetas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div class="stat-label">Total Objetivos</div>
            <div class="stat-value">{stats['total_goals']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <div class="stat-label">Activos</div>
            <div class="stat-value">{stats['active_goals']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <div class="stat-label">Racha Actual</div>
            <div class="stat-value">{stats['current_streak']} días</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
            <div class="stat-label">Total Registros</div>
            <div class="stat-value">{stats['total_logs']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Distribución de objetivos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Distribución de Objetivos")

        # Gráfico de dona
        labels = ['Activos', 'Completados', 'Pausados']
        values = [stats['active_goals'], stats['completed_goals'], stats['paused_goals']]
        colors = ['#667eea', '#43e97b', '#f5576c']

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.4,
            marker_colors=colors
        )])

        fig.update_layout(
            showlegend=True,
            height=300,
            margin=dict(t=0, b=0, l=0, r=0)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📅 Información de la Cuenta")

        member_since = datetime.fromisoformat(stats['member_since'].replace('Z', '+00:00'))
        last_activity = stats.get('last_activity')

        st.markdown(f"""
        **Miembro desde:** {member_since.strftime('%d de %B, %Y')}

        **Última actividad:** {datetime.fromisoformat(last_activity.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M') if last_activity else 'Sin actividad reciente'}

        **Objetivos completados:** {stats['completed_goals']}

        **Objetivos pausados:** {stats['paused_goals']}
        """)

# Función para mostrar objetivos
def show_goals():
    """Página de objetivos"""
    st.markdown('<p class="main-header">🎯 Mis Objetivos</p>', unsafe_allow_html=True)

    user_id = st.session_state.user['id']
    goals_data = get_user_goals(user_id)

    if not goals_data or not goals_data.get('goals'):
        st.info("Aún no tienes objetivos. ¡Crea uno usando el bot de WhatsApp!")
        return

    # Filtros
    col1, col2 = st.columns([1, 3])
    with col1:
        filter_status = st.selectbox(
            "Filtrar por estado",
            ["Todos", "Activos", "Completados", "Pausados"]
        )

    # Mostrar objetivos
    goals = goals_data['goals']

    for goal in goals:
        # Aplicar filtro
        if filter_status != "Todos":
            if filter_status.lower() != goal['status']:
                continue

        # Obtener progreso
        progress = get_goal_progress(goal['id'])

        with st.container():
            st.markdown(f"""
            <div class="goal-card">
                <h3>{goal['title']}</h3>
                <p><strong>Tipo:</strong> {goal['goal_type'].title()}</p>
                <p><strong>Estado:</strong> <span style="color: {'#43e97b' if goal['status'] == 'active' else '#f5576c'}">{goal['status'].title()}</span></p>
            </div>
            """, unsafe_allow_html=True)

            # Mostrar progreso específico según el tipo
            if progress:
                if goal['goal_type'] == 'fitness':
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Peso Inicial", f"{progress.get('start_weight', 0)} kg")
                    with col2:
                        st.metric("Peso Actual", f"{progress.get('current_weight', 0)} kg")
                    with col3:
                        st.metric("Peso Objetivo", f"{progress.get('target_weight', 0)} kg")

                    # Barra de progreso
                    progress_pct = progress.get('progress_percentage', 0)
                    st.progress(min(abs(progress_pct) / 100, 1.0))
                    st.caption(f"Progreso: {abs(progress_pct):.1f}%")

                elif goal['goal_type'] == 'learning':
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Horas Estudiadas", progress.get('total_study_hours', 0))
                    with col2:
                        st.metric("Objetivo Diario", f"{progress.get('target_hours_per_day', 0)} horas")

                elif goal['goal_type'] == 'productivity':
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Horas Practicadas", progress.get('total_practice_hours', 0))
                    with col2:
                        st.metric("Tareas Completadas", progress.get('completed_tasks', 0))

            st.markdown("---")

# Función para mostrar progreso detallado
def show_progress():
    """Página de progreso detallado"""
    st.markdown('<p class="main-header">📈 Progreso Detallado</p>', unsafe_allow_html=True)

    user_id = st.session_state.user['id']
    goals_data = get_user_goals(user_id)

    if not goals_data or not goals_data.get('goals'):
        st.info("Aún no tienes objetivos para mostrar progreso.")
        return

    # Selector de objetivo
    goals = goals_data['goals']
    goal_options = {f"{goal['title']} ({goal['goal_type']})": goal['id'] for goal in goals}

    selected_goal_name = st.selectbox("Selecciona un objetivo", list(goal_options.keys()))
    selected_goal_id = goal_options[selected_goal_name]

    # Obtener logs del objetivo
    logs_data = get_goal_logs(selected_goal_id)

    if not logs_data or not logs_data.get('logs'):
        st.info("Este objetivo aún no tiene registros de progreso.")
        return

    # Convertir a DataFrame
    logs = logs_data['logs']

    # Encontrar el objetivo seleccionado
    selected_goal = next(g for g in goals if g['id'] == selected_goal_id)

    # Mostrar gráfico según el tipo de objetivo
    if selected_goal['goal_type'] == 'fitness':
        # Extraer datos de peso
        dates = []
        weights = []

        for log in reversed(logs):  # Invertir para orden cronológico
            if log.get('log_data') and 'weight' in log['log_data']:
                dates.append(datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00')))
                weights.append(log['log_data']['weight'])

        if dates and weights:
            # Gráfico de línea
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=dates,
                y=weights,
                mode='lines+markers',
                name='Peso',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))

            # Línea de objetivo
            goal_data = selected_goal.get('goal_data', {})
            target_weight = goal_data.get('target_weight')
            if target_weight:
                fig.add_hline(
                    y=target_weight,
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Objetivo: {target_weight} kg"
                )

            fig.update_layout(
                title="Evolución del Peso",
                xaxis_title="Fecha",
                yaxis_title="Peso (kg)",
                hovermode='x unified',
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aún no hay suficientes datos de peso para graficar.")

    elif selected_goal['goal_type'] == 'learning':
        # Extraer horas de estudio
        dates = []
        hours = []

        for log in reversed(logs):
            if log.get('log_data') and 'study_hours' in log['log_data']:
                dates.append(datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00')))
                hours.append(log['log_data']['study_hours'])

        if dates and hours:
            fig = go.Figure()

            fig.add_trace(go.Bar(
                x=dates,
                y=hours,
                name='Horas de Estudio',
                marker_color='#43e97b'
            ))

            fig.update_layout(
                title="Horas de Estudio por Sesión",
                xaxis_title="Fecha",
                yaxis_title="Horas",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aún no hay suficientes datos de estudio para graficar.")

    # Tabla de registros
    st.subheader("📋 Historial de Registros")

    records = []
    for log in logs:
        record = {
            "Fecha": datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M'),
            "Tipo": log.get('log_type', 'N/A')
        }

        # Agregar datos específicos según log_data
        if log.get('log_data'):
            for key, value in log['log_data'].items():
                record[key.replace('_', ' ').title()] = value

        records.append(record)

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)

# Main
def main():
    # Verificar autenticación
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        authenticate()
    else:
        # Sidebar
        with st.sidebar:
            st.markdown("### 📱 Usuario")
            st.markdown(f"**{st.session_state.user.get('name', 'Usuario')}**")
            st.markdown(f"📞 {st.session_state.user['phone_number']}")

            st.markdown("---")

            # Navegación
            page = st.radio(
                "Navegación",
                ["📊 Resumen", "🎯 Objetivos", "📈 Progreso"],
                label_visibility="collapsed"
            )

            st.markdown("---")

            if st.button("Cerrar Sesión", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user = None
                st.rerun()

        # Mostrar página seleccionada
        if page == "📊 Resumen":
            show_overview()
        elif page == "🎯 Objetivos":
            show_goals()
        elif page == "📈 Progreso":
            show_progress()

if __name__ == "__main__":
    main()
