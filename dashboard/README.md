# 📊 Dashboard de Asistente IA

Dashboard web interactivo para monitorear objetivos y progreso del Asistente IA Personal.

## ✨ Características

- 🔐 **Autenticación trust-based** por número de teléfono
- 📊 **Página de Resumen** con estadísticas generales
- 🎯 **Página de Objetivos** con filtros por estado
- 📈 **Página de Progreso** con gráficos interactivos
- 📱 **Responsive** - funciona en mobile y desktop

## 🚀 Deployment en Streamlit Cloud

### Paso 1: Crear Cuenta en Streamlit Cloud

1. Ve a: https://streamlit.io/cloud
2. Click en **"Sign up"**
3. Conecta con tu cuenta de GitHub

### Paso 2: Crear Nueva App

1. En el dashboard de Streamlit Cloud, click **"New app"**

2. Configura la app:
   - **Repository**: `Rodolfo-CWS/asistente-ia`
   - **Branch**: `master`
   - **Main file path**: `dashboard/app.py`
   - **App URL** (custom): `asistente-ia-dashboard` (o el que prefieras)

3. **Advanced settings** (opcional):
   - Python version: `3.10`

4. Click **"Deploy!"**

### Paso 3: Esperar Deployment

- El proceso tarda 2-5 minutos
- Verás logs en tiempo real
- Cuando termine, verás: **"Your app is live!"**

### Paso 4: Acceder al Dashboard

1. Tu dashboard estará en: `https://[tu-app-url].streamlit.app`
2. Ingresa tu número de teléfono (el mismo que usas en WhatsApp)
3. ¡Listo! Ya puedes ver tus objetivos y progreso

## 📋 Requisitos Previos

- Haber usado el bot de WhatsApp al menos una vez
- Tener al menos un objetivo creado (opcional para testing)

## 🎨 Páginas del Dashboard

### 1. 📊 Resumen
- Total de objetivos (activos/completados/pausados)
- Racha actual (días consecutivos con logs)
- Total de registros
- Gráfico de distribución de objetivos
- Información de la cuenta

### 2. 🎯 Objetivos
- Lista de todos tus objetivos
- Filtros por estado (Activos/Completados/Pausados)
- Progreso detallado por objetivo:
  - **Fitness**: Peso inicial → Actual → Objetivo
  - **Learning**: Horas estudiadas vs objetivo diario
  - **Productivity**: Horas practicadas y tareas completadas

### 3. 📈 Progreso
- Selector de objetivo
- Gráficos interactivos con Plotly:
  - **Fitness**: Línea de evolución del peso
  - **Learning**: Barras de horas por sesión
  - **Productivity**: Tareas completadas
- Tabla detallada de historial de registros

## 🛠 Desarrollo Local

Para correr el dashboard localmente:

```bash
# Navegar al directorio
cd dashboard

# Instalar dependencias
pip install -r requirements.txt

# Correr la app
streamlit run app.py
```

La app estará disponible en: http://localhost:8501

## 🔧 Configuración

El dashboard se conecta automáticamente a la API de producción:
```
API_BASE_URL = "https://asistente-ia-txf0.onrender.com"
```

## 📱 Uso

1. **Login**: Ingresa tu número con código de país (ej: `+524444844003`)
2. **Navega**: Usa el sidebar para cambiar entre páginas
3. **Visualiza**: Explora tus objetivos y progreso
4. **Cierra Sesión**: Botón en el sidebar

## 🎨 Personalización

El tema del dashboard se puede personalizar en:
- `.streamlit/config.toml`

Colores actuales:
- Primary: `#667eea` (morado)
- Background: `#FFFFFF` (blanco)
- Secondary: `#F0F2F6` (gris claro)

## 🐛 Troubleshooting

### "Usuario no encontrado"
- Verifica que hayas usado el bot de WhatsApp
- Asegúrate de usar el mismo número de teléfono
- Incluye el código de país (ej: +52...)

### "Error al conectar con la API"
- Verifica que Render esté funcionando: https://asistente-ia-txf0.onrender.com/health
- Revisa que UptimeRobot esté activo

### Gráficos no se muestran
- Asegúrate de tener al menos 2 registros de progreso
- Verifica que los logs tengan datos válidos

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de Streamlit Cloud
2. Verifica la API: `/health` endpoint
3. Consulta este README

---

**¡Disfruta tu Dashboard! 🎉**
