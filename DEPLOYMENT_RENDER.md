# 🚀 Guía de Deployment en Render

Esta guía te llevará paso a paso para desplegar el Asistente IA Personal en Render.

## 📋 Pre-requisitos

- Cuenta en GitHub (con el código ya subido)
- Cuenta en Render.com (gratis)
- Cuenta en Twilio (con WhatsApp configurado)
- API Key de Anthropic (Claude)

---

## 🗄️ Paso 1: Crear Base de Datos PostgreSQL (5 minutos)

1. Ve a https://dashboard.render.com
2. Click en **"New +"** → **"PostgreSQL"**
3. Configura:
   - **Name**: `asistente-ia-db`
   - **Database**: `asistente_ia_db`
   - **User**: `asistente_ia_user`
   - **Region**: Oregon (US West)
   - **Plan**: **Free**
4. Click **"Create Database"**
5. Espera 2-3 minutos a que se cree
6. **GUARDA** la "Internal Database URL" (la usaremos después)
   - Formato: `postgresql://usuario:password@dpg-xxxxx.oregon-postgres.render.com/asistente_ia_db`

---

## 🌐 Paso 2: Crear Web Service (10 minutos)

1. En Render Dashboard, click **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub:
   - Click "Connect GitHub" si no lo has hecho
   - Busca y selecciona: `Rodolfo-CWS/asistente-ia`
3. Configura el servicio:
   - **Name**: `asistente-ia`
   - **Region**: Oregon (US West) - *misma que la BD*
   - **Branch**: `main` o `master`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: **Python 3**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 10000`
   - **Plan**: **Free**

4. Click **"Advanced"** para configurar variables de entorno

---

## 🔐 Paso 3: Configurar Variables de Entorno (5 minutos)

En la sección "Environment Variables", agrega las siguientes variables:

| Key | Value | Notas |
|-----|-------|-------|
| `ANTHROPIC_API_KEY` | `sk-ant-api03-...` | Tu API key de Claude |
| `TWILIO_ACCOUNT_SID` | `AC2269e1bddbe817...` | De tu .env local |
| `TWILIO_AUTH_TOKEN` | `bf1c6c772cec504e...` | De tu .env local |
| `TWILIO_WHATSAPP_NUMBER` | `whatsapp:+524444844003` | Tu número de Twilio |
| `SECRET_KEY` | `jBGUqAwPfK1tGwnY0317HLUvxM3IFh1cX4eT9-APZh4` | **Clave generada - NUEVA** |
| `ENVIRONMENT` | `production` | Cambiar de development |
| `PYTHON_VERSION` | `3.10.0` | Versión de Python |

⚠️ **NO** agregues `DATABASE_URL` manualmente - lo haremos en el siguiente paso.

---

## 🔗 Paso 4: Vincular Base de Datos (2 minutos)

1. En la configuración del Web Service, ve a la pestaña **"Environment"**
2. En la sección **"Environment Variables"**, click **"Add Environment Variable"**
3. Selecciona **"Add from Database"**
4. Selecciona tu base de datos: `asistente-ia-db`
5. Render automáticamente agregará `DATABASE_URL`

---

## 🚀 Paso 5: Deploy (5 minutos)

1. Click **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Verás los logs en tiempo real
4. Espera a que aparezca: **"Your service is live 🎉"**
5. Copia la URL de tu servicio (ej: `https://asistente-ia.onrender.com`)

---

## ✅ Paso 6: Verificar Deployment

### 6.1 Probar Health Check

Abre en tu navegador:
```
https://asistente-ia.onrender.com/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "production"
}
```

### 6.2 Verificar Logs

En Render Dashboard:
1. Ve a tu servicio
2. Click en **"Logs"**
3. Busca mensajes como:
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

---

## 📱 Paso 7: Configurar Webhook de Twilio (5 minutos)

1. Ve a https://console.twilio.com
2. Navega a: **Messaging** → **Settings** → **WhatsApp Sandbox Settings**
3. En el campo **"When a message comes in"**, pon:
   ```
   https://asistente-ia.onrender.com/webhook/whatsapp
   ```
   *(Reemplaza con tu URL de Render)*
4. **HTTP Method**: POST
5. Click **"Save"**

---

## 🧪 Paso 8: ¡Probar con WhatsApp!

1. Si no lo has hecho, únete al Twilio Sandbox:
   - Envía desde tu WhatsApp a: `+1 415 523 8886`
   - Mensaje: `join [codigo]` (el código que te dio Twilio)

2. Prueba el bot:
   ```
   Hola
   ```

   El bot debería responder! 🎉

3. Crea un objetivo:
   ```
   Quiero bajar de peso
   ```

4. Sigue el flujo respondiendo las preguntas del bot

---

## 🔧 Troubleshooting

### ❌ Error: "Build Failed"

**Problema**: Error durante `pip install`

**Solución**:
- Revisa los logs de build
- Verifica que `requirements.txt` está en la raíz del repo
- Asegúrate que todas las dependencias son válidas

### ❌ Error: "Your service is not responding"

**Problema**: El servicio no arranca

**Solución**:
- Verifica el Start Command: `uvicorn main:app --host 0.0.0.0 --port 10000`
- Revisa los logs para ver el error
- Verifica que todas las variables de entorno están configuradas

### ❌ Error: "Database connection failed"

**Problema**: No puede conectar a PostgreSQL

**Solución**:
- Verifica que la base de datos esté vinculada correctamente
- Revisa que `DATABASE_URL` existe en Environment Variables
- Asegúrate que la BD y el Web Service están en la misma región

### ❌ WhatsApp no responde

**Problema**: El bot no responde a mensajes

**Solución**:
1. Verifica webhook URL en Twilio (debe terminar en `/webhook/whatsapp`)
2. Prueba el health check: `https://tu-app.onrender.com/health`
3. Revisa los logs en Render cuando envías un mensaje
4. Verifica que las credenciales de Twilio son correctas

### ❌ "Unhealthy" en health check

**Problema**: `/health` responde `"database": "disconnected"`

**Solución**:
- La base de datos no está conectada
- Verifica que DATABASE_URL está configurada
- Asegúrate que la BD está activa (no pausada por inactividad)

---

## 💡 Consejos Importantes

### Free Tier Limitations

**⏰ Sleep después de 15 minutos**:
- El servicio free "duerme" después de 15 min de inactividad
- Primera petición puede tardar 30-60 segundos en despertar
- Solución: Upgrade a plan pagado ($7/mes) o usar servicio de ping

**📊 PostgreSQL Free expira en 90 días**:
- La base de datos free se elimina después de 90 días
- Hacer backups regulares
- O upgrade a plan pagado ($7/mes)

### Monitoreo

**Ver logs en tiempo real**:
```bash
# Desde Render Dashboard → Logs
```

**Recibir alertas**:
- Ve a Service Settings → Notifications
- Configura email o Slack para alertas de errores

### Auto-Deploy

Render puede auto-desplegar cuando haces push a GitHub:
1. Ve a Service Settings
2. Enable "Auto-Deploy"
3. Cada push a `main` desplegará automáticamente

---

## 📊 Costos Estimados

### Desarrollo (Free Tier)
- Web Service: $0 (con limitaciones)
- PostgreSQL: $0 (90 días)
- **Total: $0**

### Producción (Paid Tier recomendado)
- Web Service: $7/mes (sin sleep, mejor performance)
- PostgreSQL: $7/mes (sin expiración, backups)
- Twilio WhatsApp: ~$0.005/mensaje
- Claude API: ~$0.003/mensaje
- **Total: ~$14/mes + uso**

---

## 🎯 Siguientes Pasos

Una vez desplegado:

1. ✅ Probar todos los flujos (fitness, learning, productivity)
2. ✅ Monitorear logs por 24 horas
3. ✅ Configurar alertas de errores
4. ✅ Hacer backup de la base de datos
5. ✅ Documentar cualquier configuración adicional

### Mejoras Futuras

- Configurar dominio personalizado
- Implementar caché con Redis
- Agregar autenticación para endpoints admin
- Dashboard web para ver estadísticas
- Tests automatizados con CI/CD

---

## 📞 Soporte

Si tienes problemas:
- Revisa los logs en Render Dashboard
- Consulta docs de Render: https://render.com/docs
- Revisa este troubleshooting guide

¡Felicidades! 🎉 Tu Asistente IA está en producción.
