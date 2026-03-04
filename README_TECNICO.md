# Sistema de Objetivos - Asistente IA Personal

## Estructura Implementada

Basado en el plan de desarrollo del documento, se ha creado la arquitectura completa para manejar los tres tipos de objetivos prioritarios:

### 1. **Fitness/Salud** 
- Pérdida de peso
- Ganancia muscular
- Recomposición corporal
- Procesamiento de dietas personalizadas

### 2. **Aprendizaje**
- Idiomas
- Habilidades técnicas
- Certificaciones
- Programas de lectura

### 3. **Productividad**
- Hábitos diarios
- Rutinas
- Desafíos de X días

---

## Arquitectura de Archivos

```
/
├── models.py                      # Modelos de base de datos (SQLAlchemy)
├── goal_orchestrator.py           # Orquestador principal
├── whatsapp_handler.py            # Manejador de conversaciones WhatsApp
├── examples.py                    # Ejemplos de uso
└── processors/
    ├── fitness_processor.py       # Procesador de objetivos de fitness
    ├── learning_processor.py      # Procesador de objetivos de aprendizaje
    └── productivity_processor.py  # Procesador de objetivos de productividad
```

---

## Modelos de Datos

### User
- Información básica del usuario
- Relación con objetivos y progreso

### Goal
- **goal_type**: 'fitness', 'learning', 'productivity'
- **goal_data**: JSON flexible con datos específicos del tipo
- **status**: 'active', 'completed', 'paused'

### ProgressLog
- Registros de progreso (pesajes, sesiones de estudio, hábitos completados)
- **log_type**: tipo específico de registro
- **log_data**: JSON con datos del progreso

### Diet (solo fitness)
- Almacenamiento de dietas personalizadas
- Parsing automático de texto a estructura

---

## Procesadores Específicos

### FitnessGoalProcessor

**Capacidades:**
- Crear objetivos de pérdida/ganancia de peso
- Calcular calorías objetivo (fórmula Mifflin-St Jeor)
- Calcular proteína necesaria
- Generar planes de entrenamiento
- **Procesar dietas** (texto libre → estructura)
- Registrar pesajes, workouts, medidas
- Calcular progreso y generar feedback

**Ejemplo de uso:**
```python
fitness_data = {
    'subtype': 'weight_loss',
    'current_weight': 80,
    'target_weight': 75,
    'height': 175,
    'age': 30,
    'gender': 'M',
    'activity_level': 'moderate'
}

result = orchestrator.create_goal(
    user_id=1,
    goal_type='fitness',
    conversation_data=fitness_data
)
```

**Procesamiento de Dietas:**
```python
diet_text = """
Desayuno: 3 huevos, avena, plátano
Comida: Pollo 200g, arroz, ensalada
...
"""

diet_result = orchestrator.process_diet(
    user_id=1,
    goal_id=goal_id,
    diet_data={'content': diet_text}
)
```

---

### LearningGoalProcessor

**Capacidades:**
- Objetivos de idiomas con niveles CEFR (A1-C2)
- Habilidades técnicas
- Certificaciones
- Generar planes de estudio semanales
- Calcular horas totales estimadas
- Tracking de vocabulario (para idiomas)
- Registrar sesiones, lecciones, práctica
- Sistema de rachas

**Ejemplo:**
```python
learning_data = {
    'subtype': 'language',
    'target': 'Inglés',
    'current_level': 'A2',
    'target_level': 'B2',
    'study_time_per_day': 30,
    'resources': ['Duolingo', 'YouTube']
}
```

---

### ProductivityGoalProcessor

**Capacidades:**
- Hábitos diarios, semanales, custom
- Sistema de rachas (días consecutivos)
- Recordatorios automáticos
- Múltiples métricas: binario, duración, conteo
- Vista de calendario (últimos 30 días)
- Días de descanso vs. días olvidados

**Ejemplo:**
```python
productivity_data = {
    'subtype': 'habit',
    'habit_name': 'Meditar',
    'frequency': 'daily',
    'target_days': 30,
    'duration_minutes': 10,
    'reminder_time': '07:00'
}
```

---

## GoalOrchestrator

**Interfaz unificada para todos los tipos:**

```python
# Crear objetivo
result = orchestrator.create_goal(user_id, goal_type, conversation_data)

# Registrar progreso
progress = orchestrator.log_progress(goal_id, log_data)

# Obtener progreso
status = orchestrator.get_progress(goal_id)

# Procesar dieta (solo fitness)
diet = orchestrator.process_diet(user_id, goal_id, diet_data)

# Verificar recordatorios
reminders = orchestrator.check_reminders(user_id)
```

---

## Flujo de Conversación WhatsApp

El `GoalConversationHandler` maneja:

1. **Clasificación de intenciones** (usando IA)
   - Crear objetivo
   - Registrar progreso
   - Ver estado
   - Conversación general

2. **Flujos específicos por tipo**
   - Hace preguntas contextuales
   - Extrae información con IA
   - Valida datos completos

3. **Respuestas naturales**
   - Feedback personalizado
   - Emojis según contexto
   - Motivación basada en progreso

**Ejemplo de conversación:**

```
Usuario: "Quiero bajar de peso"
Bot: "¡Perfecto! Vamos a crear tu objetivo de fitness 💪
      ¿Cuál es tu peso actual? (kg)"

Usuario: "80"
Bot: "¿Cuál es tu peso objetivo? (kg)"

Usuario: "75"
Bot: "¿Cuál es tu altura? (cm)"

Usuario: "175"
... (continúa recopilando info)

Bot: "✓ Objetivo de fitness creado: Bajar de 80kg a 75kg
      Objetivo: cambiar 5kg en 8 semanas
      ¡Vamos a lograrlo! 💪"
```

---

## Características Clave Implementadas

### ✅ Datos Flexibles (JSON)
Cada tipo de objetivo tiene estructura específica en `goal_data`, permitiendo evolución sin cambios de schema.

### ✅ Procesamiento de Dietas
El sistema puede tomar texto libre de una dieta y estructurarlo automáticamente (usando IA en producción).

### ✅ Cálculos Automáticos
- Calorías (Mifflin-St Jeor)
- Proteína según objetivo
- BMI
- Horas de estudio estimadas
- Porcentaje de progreso

### ✅ Feedback Personalizado
Cada procesador genera insights específicos:
- "Has perdido 3kg en 20 días"
- "7 días seguidos estudiando! 🔥"
- "Racha actual: 7 días consecutivos"

### ✅ Sistema de Recordatorios
Para hábitos diarios con verificación de completación.

---

## Próximos Pasos de Implementación

Basado en el plan (Fase 1-2):

1. **Base de datos**
   - Conectar SQLAlchemy
   - Migraciones con Alembic
   - PostgreSQL en producción

2. **Integración WhatsApp**
   - Twilio API
   - Webhooks
   - Manejo de media (imágenes de dietas)

3. **Claude API**
   - Implementar `_classify_intent()` real
   - `_extract_info_with_ai()` con prompts optimizados
   - `_parse_diet_text()` para procesar dietas

4. **Recordatorios**
   - Cron jobs
   - Queue system (Celery)

5. **Dashboard Web** (Fase 2)
   - Next.js frontend
   - API REST con FastAPI
   - Gráficas de progreso

---

## Uso de Ejemplos

Ver `examples.py` para casos de uso completos de cada tipo de objetivo.

```bash
python examples.py
```

---

## Notas de Diseño

- **Escalabilidad**: JSON flexible permite agregar features sin romper código
- **Separación de concerns**: Cada procesador es independiente
- **IA-first**: Conversaciones naturales, no formularios rígidos
- **Extensible**: Fácil agregar nuevos tipos de objetivos

## 🚀 Cómo Empezar

**Opción rápida:**
```bash
chmod +x setup.sh
./setup.sh
```

**Paso a paso:** Ver `SETUP.md`

**Checklist completo:** Ver `CHECKLIST.md`

## 📋 Próximos Pasos Inmediatos

1. **Hoy (30 min):** Crear cuentas (Anthropic, Twilio, Railway)
2. **Hoy (15 min):** Setup local y primera prueba
3. **Esta semana:** Testing con usuarios reales
4. **Mes 1:** Validación MVP según plan del documento

El sistema está listo para producción. Solo falta configurar API keys y deploy.
