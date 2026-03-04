# ✅ Checklist de Implementación

## Hoy (30 min)

### [ ] 1. Crear Cuentas
- [ ] Anthropic: https://console.anthropic.com → Copiar API key
- [ ] Twilio: https://www.twilio.com/try-twilio → Copiar SID + Token
- [ ] Railway: https://railway.app → Deploy PostgreSQL

### [ ] 2. Setup Local
```bash
cd asistente-ia
chmod +x setup.sh
./setup.sh
# Editar .env con tus keys
```

### [ ] 3. Primera Prueba
```bash
python main.py
# En otra terminal:
ngrok http 8000
```

### [ ] 4. Conectar WhatsApp
- [ ] Twilio → Messaging → WhatsApp Sandbox
- [ ] Unirse al sandbox (enviar código)
- [ ] Configurar webhook: tu-url.ngrok.io/webhook/whatsapp
- [ ] Probar enviando "Hola"

## Esta Semana

### [ ] Validar Flujos
- [ ] Crear objetivo de fitness (bajar peso)
- [ ] Registrar peso
- [ ] Ver progreso
- [ ] Crear objetivo de aprendizaje
- [ ] Crear hábito

### [ ] Mejorar IA
- [ ] Implementar `_classify_intent()` con Claude API
- [ ] Implementar `_extract_info_with_ai()` con Claude API
- [ ] Agregar manejo de errores robusto

### [ ] Testing
- [ ] Probar con 2-3 amigos
- [ ] Recopilar feedback
- [ ] Ajustar prompts

## Siguiente Mes

### [ ] Features MVP
- [ ] Google Calendar integration (opcional)
- [ ] Recordatorios automáticos (cron)
- [ ] Dashboard web básico

### [ ] Deploy Producción
- [ ] Deploy en Railway permanente
- [ ] Configurar dominio
- [ ] Salir de Twilio Sandbox ($20 USD one-time)
- [ ] Monitoreo con Sentry

## Decisión Go/No-Go (Mes 3)

**Métricas para continuar:**
- [ ] 10+ usuarios activos
- [ ] 70%+ dicen que es útil
- [ ] 3+ dispuestos a pagar

Si NO: Pivotar o detener
Si SÍ: Continuar con Fase 2 del plan
