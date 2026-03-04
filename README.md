# 🤖 Asistente IA Personal

Asistente de IA que trabaja por WhatsApp para ayudarte a lograr tus objetivos de **fitness**, **aprendizaje** y **productividad**.

![Status](https://img.shields.io/badge/status-MVP-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Características

- 💪 **Fitness**: Pérdida de peso, ganancia muscular, procesamiento de dietas
- 📚 **Aprendizaje**: Idiomas, habilidades, tracking de progreso
- ✨ **Productividad**: Hábitos diarios, rutinas, sistema de rachas
- 🤖 **IA Conversacional**: Interfaz natural vía WhatsApp
- 📊 **Tracking Automático**: Métricas, progreso, feedback personalizado

## 🚀 Quick Start (5 minutos)

```bash
# 1. Clonar repositorio
git clone https://github.com/Rodolfo-CWS/asistente-ia.git
cd asistente-ia

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar
cp .env.example .env
# Editar .env con tus API keys

# 4. Probar
python test_local.py
```

📖 **Documentación completa:** [QUICKSTART.md](QUICKSTART.md)

## 📋 Pre-requisitos

- Python 3.10+
- Cuenta Anthropic (API gratis): https://console.anthropic.com
- Cuenta Twilio (gratis): https://www.twilio.com/try-twilio
- ngrok para testing local: https://ngrok.com

## 📁 Estructura del Proyecto

```
asistente-ia/
├── main.py                    # Servidor FastAPI + webhook WhatsApp
├── models.py                  # Modelos de base de datos
├── goal_orchestrator.py       # Orquestador de objetivos
├── whatsapp_handler.py        # Manejo de conversaciones
├── claude_helpers.py          # Integración con Claude API
├── processors/
│   ├── fitness_processor.py   # Objetivos de fitness
│   ├── learning_processor.py  # Objetivos de aprendizaje
│   └── productivity_processor.py  # Hábitos y rutinas
├── requirements.txt           # Dependencias Python
├── .env.example              # Template de configuración
└── docs/
    ├── QUICKSTART.md         # Inicio rápido
    ├── SETUP.md              # Setup completo paso a paso
    └── CHECKLIST.md          # Plan de implementación

```

## 🎯 Cómo Funciona

### 1. Usuario envía mensaje por WhatsApp
```
"Quiero bajar 5kg en 2 meses"
```

### 2. IA analiza y crea plan
- Clasifica intención (objetivo de fitness)
- Hace preguntas para recopilar info
- Calcula calorías, plan de entrenamiento
- Crea objetivo en la base de datos

### 3. Tracking y Feedback
```
"Hoy pesé 78kg"
→ IA registra progreso
→ Calcula métricas
→ Envía feedback motivacional
```

## 💰 Costos Estimados

**Desarrollo (primeros 30 días):**
- Anthropic API: $0 (crédito gratis)
- Twilio Sandbox: $0
- Railway/Render: $0 (trial)
- **Total: $0**

**Producción (10 usuarios):**
- Anthropic: ~$15 MXN/mes
- Twilio: ~$90 MXN/mes  
- Hosting: ~$90 MXN/mes
- **Total: ~$195 MXN/mes**

## 📚 Documentación

- [🚀 Quick Start](QUICKSTART.md) - Empieza en 5 minutos
- [⚙️ Setup Completo](SETUP.md) - Guía detallada paso a paso
- [✅ Checklist](CHECKLIST.md) - Plan de ejecución por fases
- [📖 README Técnico](README.md) - Arquitectura y detalles

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI + Python
- **IA**: Claude API (Anthropic)
- **Messaging**: Twilio WhatsApp API
- **Database**: PostgreSQL / SQLite
- **Deployment**: Railway / Render

## 🧪 Testing

```bash
# Test local sin WhatsApp
python test_local.py

# Servidor de desarrollo
python main.py

# Exponer con ngrok
ngrok http 8000
```

## 📈 Roadmap

- [x] MVP - Procesadores de 3 tipos de objetivos
- [x] Integración WhatsApp + Claude API
- [ ] Google Calendar integration
- [ ] Dashboard web (Next.js)
- [ ] Sistema de recordatorios automáticos
- [ ] API pública
- [ ] Mobile app

## 🤝 Contribuir

Este es un proyecto personal en desarrollo. Sugerencias y feedback son bienvenidos.

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE)

## 👤 Autor

**Rodolfo**
- GitHub: [@Rodolfo-CWS](https://github.com/Rodolfo-CWS)

---

**Nota:** Este proyecto está en fase MVP. Basado en el plan de desarrollo documentado en `Plan_Desarrollo_Asistente_IA_Personal.pdf`
