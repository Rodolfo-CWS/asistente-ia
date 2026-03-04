"""
Ejemplos de uso del sistema de objetivos
"""

from goal_orchestrator import GoalOrchestrator

# Simular sesión de DB (en producción usar SQLAlchemy session real)
db_session = None

orchestrator = GoalOrchestrator(db_session)

# ============================================
# EJEMPLO 1: FITNESS - Pérdida de peso
# ============================================

print("=" * 50)
print("EJEMPLO 1: Objetivo de Fitness - Pérdida de peso")
print("=" * 50)

# Datos que se extraerían de la conversación con el usuario
fitness_data = {
    'subtype': 'weight_loss',
    'current_weight': 80,
    'target_weight': 75,
    'target_date': '2026-03-29',
    'height': 175,
    'age': 30,
    'gender': 'M',
    'activity_level': 'moderate',
    'preferences': {
        'workout_types': ['cardio', 'strength'],
        'days_per_week': 4,
        'time_preference': 'morning'
    }
}

# Crear objetivo
result = orchestrator.create_goal(
    user_id=1,
    goal_type='fitness',
    conversation_data=fitness_data
)

print("\n✓ Objetivo creado:")
print(result['message'])
print(f"\nGoal ID: {result['goal_id']}")

# Simular registro de progreso - pesaje
print("\n--- Registrando pesaje (semana 1) ---")
progress_result = orchestrator.log_progress(
    goal_id=result['goal_id'],
    log_data={
        'type': 'weight_update',
        'weight': 79,
        'notes': 'Me siento bien!'
    }
)

print(progress_result['feedback'])

# ============================================
# EJEMPLO 2: FITNESS con Dieta
# ============================================

print("\n" + "=" * 50)
print("EJEMPLO 2: Procesamiento de Dieta")
print("=" * 50)

diet_text = """
Desayuno (7am): 
- 3 huevos revueltos
- 1 taza de avena
- 1 plátano
Total: ~450 cal

Comida (2pm):
- Pechuga de pollo 200g
- Arroz integral 1 taza
- Ensalada verde
Total: ~550 cal

Cena (8pm):
- Salmón 150g
- Vegetales al vapor
- Quinoa 1/2 taza
Total: ~500 cal
"""

diet_result = orchestrator.process_diet(
    user_id=1,
    goal_id=result['goal_id'],
    diet_data={'content': diet_text}
)

if diet_result['success']:
    print(f"\n{diet_result['message']}")

# ============================================
# EJEMPLO 3: LEARNING - Aprender idioma
# ============================================

print("\n" + "=" * 50)
print("EJEMPLO 3: Objetivo de Aprendizaje - Inglés")
print("=" * 50)

learning_data = {
    'subtype': 'language',
    'target': 'Inglés',
    'current_level': 'A2',
    'target_level': 'B2',
    'target_date': '2026-07-29',
    'study_time_per_day': 30,
    'preferred_times': ['morning'],
    'resources': ['Duolingo', 'YouTube', 'Libros'],
    'focus_areas': ['speaking', 'listening']
}

learning_result = orchestrator.create_goal(
    user_id=1,
    goal_type='learning',
    conversation_data=learning_data
)

print("\n✓ Objetivo creado:")
print(learning_result['message'])

# Registrar sesión de estudio
print("\n--- Registrando sesión de estudio ---")
study_progress = orchestrator.log_progress(
    goal_id=learning_result['goal_id'],
    log_data={
        'type': 'study_session',
        'duration_minutes': 45,
        'focus_area': 'listening',
        'resource': 'YouTube',
        'quality': 'good'
    }
)

print(study_progress['feedback'])

# ============================================
# EJEMPLO 4: PRODUCTIVITY - Hábito de meditación
# ============================================

print("\n" + "=" * 50)
print("EJEMPLO 4: Objetivo de Productividad - Meditar")
print("=" * 50)

productivity_data = {
    'subtype': 'habit',
    'habit_name': 'Meditar',
    'frequency': 'daily',
    'target_days': 30,
    'time_of_day': 'morning',
    'duration_minutes': 10,
    'reminder_time': '07:00',
    'tracking_metric': 'binary'
}

productivity_result = orchestrator.create_goal(
    user_id=1,
    goal_type='productivity',
    conversation_data=productivity_data
)

print("\n✓ Objetivo creado:")
print(productivity_result['message'])

# Registrar completación
print("\n--- Registrando día completado ---")
habit_progress = orchestrator.log_progress(
    goal_id=productivity_result['goal_id'],
    log_data={
        'type': 'completion',
        'duration_minutes': 12,
        'quality': 4,
        'notes': 'Excelente sesión, muy relajante'
    }
)

print(habit_progress['feedback'])

# ============================================
# EJEMPLO 5: Verificar recordatorios
# ============================================

print("\n" + "=" * 50)
print("EJEMPLO 5: Verificando recordatorios pendientes")
print("=" * 50)

reminders = orchestrator.check_reminders(user_id=1)

print(f"\nRecordatorios a enviar: {len(reminders)}")
for reminder in reminders:
    print(f"\nGoal ID {reminder['goal_id']}:")
    print(f"  → {reminder['message']}")

# ============================================
# EJEMPLO 6: Obtener progreso de todos los objetivos
# ============================================

print("\n" + "=" * 50)
print("EJEMPLO 6: Dashboard - Progreso de todos los objetivos")
print("=" * 50)

# En producción, esto consultaría todos los objetivos activos del usuario
active_goals = [
    {'id': result['goal_id'], 'type': 'fitness'},
    {'id': learning_result['goal_id'], 'type': 'learning'},
    {'id': productivity_result['goal_id'], 'type': 'productivity'}
]

for goal in active_goals:
    progress = orchestrator.get_progress(goal['id'])
    if progress['success']:
        print(f"\n{goal['type'].upper()}:")
        print(f"  Progreso: {progress['progress']['percentage']}%")
        if 'current_streak' in progress['progress']:
            print(f"  Racha: {progress['progress']['current_streak']} días")

print("\n" + "=" * 50)
print("Ejemplos completados!")
print("=" * 50)
