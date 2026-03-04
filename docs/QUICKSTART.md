# 🚀 Quick Start (5 minutos)

## TL;DR
```bash
# 1. Clonar/copiar archivos
cd asistente-ia

# 2. Setup
pip install -r requirements.txt
cp .env.example .env
# Editar .env (ver abajo)

# 3. Probar localmente
python test_local.py

# 4. Servidor
python main.py &
ngrok http 8000

# 5. Conectar WhatsApp (ver Twilio setup abajo)
```

## API Keys Necesarias (GRATIS)

### Anthropic (2 min)
```
1. https://console.anthropic.com
2. Settings → API Keys → Create Key
3. Copiar: sk-ant-xxx
```

### Twilio (3 min)  
```
1. https://www.twilio.com/try-twilio
2. Console → Account Info
3. Copiar: 
   - Account SID: ACxxx
   - Auth Token: xxx
4. Messaging → Try WhatsApp
5. Número sandbox: +14155238886
```

### Railway (OPCIONAL - para producción)
```
1. https://railway.app
2. New Project → PostgreSQL
3. Copiar DATABASE_URL
```

## .env Mínimo

```bash
# Para testing local
DATABASE_URL=sqlite:///local.db
ANTHROPIC_API_KEY=sk-ant-xxx
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## Probar Sin WhatsApp

```bash
python test_local.py
```
Simula conversación completa.

## Conectar WhatsApp Real

```bash
# Terminal 1
python main.py

# Terminal 2  
ngrok http 8000
# Copiar URL: https://abc123.ngrok.io

# Twilio Console
Messaging → WhatsApp Sandbox → Configure
When a message comes in: https://abc123.ngrok.io/webhook/whatsapp

# Tu WhatsApp
Enviar código a +1 415 523 8886: "join xxx-xxx"
Luego: "Hola"
```

## Siguientes Pasos

Ver `CHECKLIST.md` para plan completo.

## Problemas Comunes

**"Invalid API key"**: Verifica .env
**"No module named 'anthropic'"**: `pip install -r requirements.txt`
**Bot no responde**: Verifica ngrok URL en Twilio
**WhatsApp no conecta**: Envía código "join xxx-xxx" primero
