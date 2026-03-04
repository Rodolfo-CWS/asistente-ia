from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json

class FitnessGoalProcessor:
    """Procesa objetivos de fitness: pérdida de peso, ganancia muscular, etc."""
    
    GOAL_SUBTYPES = {
        'weight_loss': 'Pérdida de peso',
        'muscle_gain': 'Ganancia muscular',
        'body_recomp': 'Recomposición corporal',
        'endurance': 'Mejorar resistencia',
        'strength': 'Ganar fuerza'
    }
    
    def __init__(self, db_session):
        self.db = db_session
        
    def create_goal_from_conversation(self, user_id: int, conversation_data: Dict) -> Dict[str, Any]:
        """
        Crea un objetivo de fitness a partir de la conversación con el usuario.
        
        conversation_data esperado:
        {
            'subtype': 'weight_loss',
            'current_weight': 80,
            'target_weight': 75,
            'target_date': '2026-03-29',
            'height': 175,
            'age': 30,
            'gender': 'M',
            'activity_level': 'moderate',
            'diet_data': {...},  # Opcional: si el usuario proporciona una dieta
            'preferences': {
                'workout_types': ['cardio', 'strength'],
                'days_per_week': 4,
                'time_preference': 'morning'
            }
        }
        """
        
        subtype = conversation_data.get('subtype', 'weight_loss')
        
        # Calcular métricas
        current_weight = conversation_data['current_weight']
        target_weight = conversation_data['target_weight']
        weight_diff = abs(target_weight - current_weight)
        
        # Calcular BMI
        height_m = conversation_data['height'] / 100
        current_bmi = current_weight / (height_m ** 2)
        target_bmi = target_weight / (height_m ** 2)
        
        # Calcular objetivo de calorías (fórmula simplificada)
        calories_target = self._calculate_calorie_target(conversation_data)
        
        # Crear plan de entrenamiento
        workout_plan = self._generate_workout_plan(conversation_data)
        
        goal_data = {
            'subtype': subtype,
            'metrics': {
                'current_weight': current_weight,
                'target_weight': target_weight,
                'weight_to_lose_gain': weight_diff,
                'current_bmi': round(current_bmi, 1),
                'target_bmi': round(target_bmi, 1),
                'height': conversation_data['height'],
                'age': conversation_data['age'],
                'gender': conversation_data['gender']
            },
            'nutrition': {
                'daily_calories': calories_target,
                'protein_g': self._calculate_protein_target(conversation_data),
                'has_custom_diet': 'diet_data' in conversation_data
            },
            'workout_plan': workout_plan,
            'preferences': conversation_data.get('preferences', {}),
            'tracking': {
                'weigh_in_frequency': 'weekly',  # semanal por defecto
                'measure_body_fat': False,
                'track_measurements': False
            }
        }
        
        return {
            'goal_type': 'fitness',
            'title': self._generate_title(conversation_data),
            'description': self._generate_description(conversation_data),
            'target_date': conversation_data.get('target_date'),
            'goal_data': goal_data
        }
    
    def process_diet(self, diet_data: Dict) -> Dict[str, Any]:
        """
        Procesa una dieta proporcionada por el usuario.
        
        diet_data puede ser:
        - Texto libre que se parsea con IA
        - JSON estructurado
        - Imagen/PDF que se procesa
        """
        
        # Si es texto, usar Claude para estructurarlo
        if isinstance(diet_data.get('content'), str):
            structured_diet = self._parse_diet_text(diet_data['content'])
        else:
            structured_diet = diet_data
        
        # Validar y enriquecer
        processed_diet = {
            'name': structured_diet.get('name', 'Mi dieta'),
            'total_calories': 0,
            'meals': [],
            'macros': {
                'protein': 0,
                'carbs': 0,
                'fats': 0
            }
        }
        
        # Procesar comidas
        for meal in structured_diet.get('meals', []):
            processed_meal = {
                'name': meal['name'],
                'time': meal.get('time'),
                'foods': meal.get('foods', []),
                'calories': meal.get('calories', 0),
                'macros': meal.get('macros', {})
            }
            processed_diet['meals'].append(processed_meal)
            processed_diet['total_calories'] += processed_meal['calories']
        
        return processed_diet
    
    def log_progress(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """
        Registra progreso: pesaje, workout completado, medidas, etc.
        """
        
        log_type = log_data.get('type')
        
        if log_type == 'weight_update':
            return self._log_weight_update(goal_id, log_data)
        elif log_type == 'workout_completed':
            return self._log_workout(goal_id, log_data)
        elif log_type == 'measurements':
            return self._log_measurements(goal_id, log_data)
        
        return {'status': 'unknown_type'}
    
    def _log_weight_update(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra actualización de peso"""
        
        weight = log_data['weight']
        date = log_data.get('date', datetime.utcnow())
        
        # Obtener peso anterior
        # previous_logs = self.db.query(ProgressLog).filter(...)
        
        return {
            'log_type': 'weight_update',
            'log_data': {
                'weight': weight,
                'date': date.isoformat() if isinstance(date, datetime) else date,
                'notes': log_data.get('notes')
            }
        }
    
    def _log_workout(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra workout completado"""
        
        return {
            'log_type': 'workout_completed',
            'log_data': {
                'workout_type': log_data['workout_type'],
                'duration_minutes': log_data.get('duration', 30),
                'intensity': log_data.get('intensity', 'moderate'),
                'calories_burned': log_data.get('calories_burned'),
                'notes': log_data.get('notes')
            }
        }
    
    def calculate_progress(self, goal_id: int) -> Dict[str, Any]:
        """Calcula el progreso actual del objetivo"""
        
        # Obtener objetivo y logs
        # goal = self.db.query(Goal).filter_by(id=goal_id).first()
        # logs = self.db.query(ProgressLog).filter_by(goal_id=goal_id).all()
        
        # Por ahora, retornar estructura de ejemplo
        return {
            'percentage': 40,
            'current_weight': 77,
            'target_weight': 75,
            'weight_lost': 3,
            'days_elapsed': 20,
            'days_remaining': 40,
            'weekly_average_loss': 0.375,
            'on_track': True,
            'insights': [
                'Vas muy bien! Has perdido 3kg en 20 días',
                'Tu promedio semanal es de 375g, necesitas 333g/semana para llegar',
                'Estás adelante del objetivo ✓'
            ]
        }
    
    def generate_feedback(self, progress_data: Dict) -> str:
        """Genera feedback personalizado basado en el progreso"""
        
        if progress_data['on_track']:
            return f"""¡Excelente trabajo! 💪

Progreso: {progress_data['percentage']}%
Has perdido {progress_data['weight_lost']}kg de {abs(progress_data['target_weight'] - progress_data['current_weight'] - progress_data['weight_lost'])}kg total.

{chr(10).join(progress_data['insights'])}

Sigue así! 🎯"""
        else:
            return "Necesitas ajustar tu plan..."
    
    def _calculate_calorie_target(self, data: Dict) -> int:
        """Calcula objetivo de calorías (fórmula Mifflin-St Jeor)"""
        
        weight = data['current_weight']
        height = data['height']
        age = data['age']
        gender = data['gender']
        
        # BMR (Basal Metabolic Rate)
        if gender == 'M':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Multiplicador por nivel de actividad
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        activity = data.get('activity_level', 'moderate')
        tdee = bmr * activity_multipliers[activity]
        
        # Ajustar según objetivo
        if data.get('subtype') == 'weight_loss':
            # Déficit de 500 cal para ~0.5kg/semana
            return int(tdee - 500)
        elif data.get('subtype') == 'muscle_gain':
            # Superávit de 300-500 cal
            return int(tdee + 400)
        
        return int(tdee)
    
    def _calculate_protein_target(self, data: Dict) -> int:
        """Calcula objetivo de proteína en gramos"""
        
        weight = data['current_weight']
        subtype = data.get('subtype')
        
        if subtype == 'muscle_gain':
            # 2g por kg
            return int(weight * 2)
        else:
            # 1.6g por kg (preservar músculo en déficit)
            return int(weight * 1.6)
    
    def _generate_workout_plan(self, data: Dict) -> Dict:
        """Genera plan de entrenamiento"""
        
        preferences = data.get('preferences', {})
        days_per_week = preferences.get('days_per_week', 3)
        
        # Plan básico de ejemplo
        if data.get('subtype') == 'weight_loss':
            return {
                'days_per_week': days_per_week,
                'sessions': [
                    {'day': 'Lunes', 'type': 'Cardio', 'duration': 30},
                    {'day': 'Miércoles', 'type': 'Fuerza', 'duration': 45},
                    {'day': 'Viernes', 'type': 'Cardio', 'duration': 30}
                ]
            }
        
        return {'days_per_week': days_per_week, 'sessions': []}
    
    def _generate_title(self, data: Dict) -> str:
        """Genera título para el objetivo"""
        
        subtype = data.get('subtype', 'weight_loss')
        
        if subtype == 'weight_loss':
            return f"Bajar de {data['current_weight']}kg a {data['target_weight']}kg"
        elif subtype == 'muscle_gain':
            return f"Ganar músculo: {data['current_weight']}kg → {data['target_weight']}kg"
        
        return "Mi objetivo de fitness"
    
    def _generate_description(self, data: Dict) -> str:
        """Genera descripción del objetivo"""
        
        weight_diff = abs(data['target_weight'] - data['current_weight'])
        weeks = self._calculate_weeks_to_target(data)
        
        return f"Objetivo: cambiar {weight_diff}kg en {weeks} semanas"
    
    def _calculate_weeks_to_target(self, data: Dict) -> int:
        """Calcula semanas hasta la fecha objetivo"""
        
        if 'target_date' in data:
            target = datetime.fromisoformat(data['target_date'])
            delta = target - datetime.now()
            return delta.days // 7
        
        return 8  # Default: 2 meses
    
    def _parse_diet_text(self, text: str) -> Dict:
        """
        Parsea texto de dieta usando IA.
        Aquí se integraría con Claude API para estructurar el texto.
        """
        
        # Por ahora, retornar estructura básica
        # En producción, esto llamaría a Claude API
        
        return {
            'name': 'Dieta del usuario',
            'meals': [
                {
                    'name': 'Desayuno',
                    'foods': [],
                    'calories': 400
                }
            ]
        }
