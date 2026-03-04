# Guía de Setup - Asistente IA Personal

## Paso 1: Crear Cuentas (15 min)

### 1.1 Anthropic (Claude API)
```
1. Ve a: https://console.anthropic.com
2. Crea cuenta
3. Ve a API Keys → Create Key
4. Guarda la key: sk-ant-xxx
```
Costo: $5 gratis, luego ~$0.003/mensaje

### 1.2 Twilio (WhatsApp)
```
1. Ve a: https://www.twilio.com/try-twilio
2. Crea cuenta (pide tarjeta pero da $15 crédito)
3. Ve a: Messaging → Try it out → Send a WhatsApp message
4. Guarda:
   - Account SID: ACxxx
   - Auth Token: xxx
   - WhatsApp Sandbox Number: +14155238886
```
Costo: $0 en sandbox, $0.005/mensaje en producción

### 1.3 Railway (Hosting + DB)
```
1. Ve a: https://railway.app
2. Login con GitHub
3. New Project → Deploy PostgreSQL
4. Guarda la DATABASE_URL
```
Costo: $5/mes (gratis primeros días)

## Paso 2: Setup Local (10 min)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 3. Inicializar base de datos
python -c "from main import engine, Base; Base.metadata.create_all(bind=engine)"

# 4. Probar localmente
python main.py
# Servidor corriendo en http://localhost:8000
```

## Paso 3: Conectar WhatsApp Sandbox (5 min)

```
1. En Twilio Console → Messaging → Try it out → Send a WhatsApp message
2. Escanea el QR o envía mensaje a +1 415 523 8886
3. Envía el código que te dan (ej: "join xxx-xxx")
4. Ahora puedes recibir mensajes!
```

## Paso 4: Tunnel para Testing (ngrok)

```bash
# 1. Instalar ngrok
brew install ngrok  # Mac
# o descarga de https://ngrok.com

# 2. Exponer puerto 8000
ngrok http 8000

# 3. Copiar URL (ej: https://abc123.ngrok.io)

# 4. En Twilio Console:
#    Messaging → Settings → WhatsApp Sandbox Settings
#    "When a message comes in": https://abc123.ngrok.io/webhook/whatsapp
```

## Paso 5: Probar! 🎉

Envía a tu WhatsApp Sandbox:
```
"Hola"
→ Bot te saluda

"Quiero bajar 5kg"
→ Bot empieza a hacer preguntas

"80" (tu peso actual)
→ Continúa el flujo...
```

## Paso 6: Deploy a Producción (Railway)

```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Inicializar proyecto
railway init

# 4. Deploy
railway up

# 5. Configurar variables de entorno en Railway dashboard

# 6. Obtener URL de producción
railway domain

# 7. Actualizar webhook en Twilio con URL de Railway
```

## Costos Estimados

**Desarrollo (primeros 30 días):**
- Anthropic: $0 (crédito gratis)
- Twilio: $0 (sandbox gratis)
- Railway: $0 (trial)
**Total: $0**

**Producción (10 usuarios activos):**
- Anthropic API: ~$15 MXN/mes
- Twilio: ~$90 MXN/mes
- Railway: ~$90 MXN/mes
**Total: ~$195 MXN/mes**

## Troubleshooting

**Error: "Invalid API key"**
→ Verifica .env tiene las keys correctas

**Error: "Database connection failed"**
→ Verifica DATABASE_URL en .env

**WhatsApp no responde**
→ Verifica ngrok está corriendo
→ Verifica webhook URL en Twilio

**Bot no entiende mensajes**
→ Claude API key incorrecta
→ Verificar logs: `railway logs`

## Próximos Pasos

Una vez funcionando:
1. Implementar integraciones (Google Calendar)
2. Agregar más tipos de objetivos
3. Dashboard web (Next.js)
4. Sistema de pagos (Stripe)
