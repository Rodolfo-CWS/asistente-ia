from datetime import datetime, timedelta
from typing import Dict, Any, List

class LearningGoalProcessor:
    """Procesa objetivos de aprendizaje: idiomas, habilidades, cursos, etc."""
    
    GOAL_SUBTYPES = {
        'language': 'Aprender idioma',
        'skill': 'Desarrollar habilidad',
        'certification': 'Obtener certificación',
        'reading': 'Programa de lectura',
        'course': 'Completar curso'
    }
    
    # Niveles comunes para idiomas
    LANGUAGE_LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    
    def __init__(self, db_session):
        self.db = db_session
    
    def create_goal_from_conversation(self, user_id: int, conversation_data: Dict) -> Dict[str, Any]:
        """
        Crea objetivo de aprendizaje.
        
        conversation_data esperado:
        {
            'subtype': 'language',
            'target': 'Inglés',
            'current_level': 'A2',
            'target_level': 'B2',
            'target_date': '2026-07-29',
            'study_time_per_day': 30,  # minutos
            'preferred_times': ['morning', 'evening'],
            'resources': ['Duolingo', 'YouTube', 'Books'],
            'focus_areas': ['speaking', 'listening']
        }
        """
        
        subtype = conversation_data.get('subtype', 'skill')
        
        # Crear plan de estudio
        study_plan = self._generate_study_plan(conversation_data)
        
        # Calcular horas totales necesarias
        total_hours = self._estimate_total_hours(conversation_data)
        
        goal_data = {
            'subtype': subtype,
            'target': conversation_data['target'],
            'levels': {
                'current': conversation_data.get('current_level'),
                'target': conversation_data.get('target_level')
            },
            'schedule': {
                'minutes_per_day': conversation_data.get('study_time_per_day', 30),
                'days_per_week': conversation_data.get('days_per_week', 5),
                'preferred_times': conversation_data.get('preferred_times', [])
            },
            'resources': conversation_data.get('resources', []),
            'focus_areas': conversation_data.get('focus_areas', []),
            'study_plan': study_plan,
            'estimated_total_hours': total_hours,
            'tracking': {
                'log_sessions': True,
                'track_vocabulary': subtype == 'language',
                'practice_exercises': True
            }
        }
        
        return {
            'goal_type': 'learning',
            'title': self._generate_title(conversation_data),
            'description': self._generate_description(conversation_data),
            'target_date': conversation_data.get('target_date'),
            'goal_data': goal_data
        }
    
    def log_progress(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """
        Registra progreso: sesión de estudio, lección completada, práctica, etc.
        """
        
        log_type = log_data.get('type')
        
        if log_type == 'study_session':
            return self._log_study_session(goal_id, log_data)
        elif log_type == 'lesson_completed':
            return self._log_lesson(goal_id, log_data)
        elif log_type == 'practice':
            return self._log_practice(goal_id, log_data)
        elif log_type == 'vocabulary':
            return self._log_vocabulary(goal_id, log_data)
        
        return {'status': 'unknown_type'}
    
    def _log_study_session(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra sesión de estudio"""
        
        return {
            'log_type': 'study_session',
            'log_data': {
                'duration_minutes': log_data['duration_minutes'],
                'focus_area': log_data.get('focus_area'),
                'resource_used': log_data.get('resource'),
                'quality': log_data.get('quality', 'good'),  # poor, ok, good, excellent
                'notes': log_data.get('notes')
            }
        }
    
    def _log_lesson(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra lección completada"""
        
        return {
            'log_type': 'lesson_completed',
            'log_data': {
                'lesson_name': log_data['lesson_name'],
                'platform': log_data.get('platform'),
                'score': log_data.get('score'),
                'time_spent': log_data.get('time_spent')
            }
        }
    
    def _log_practice(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra práctica"""
        
        return {
            'log_type': 'practice',
            'log_data': {
                'practice_type': log_data['practice_type'],  # speaking, writing, listening
                'duration': log_data.get('duration'),
                'performance': log_data.get('performance')
            }
        }
    
    def _log_vocabulary(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra palabras/vocabulario aprendido"""
        
        return {
            'log_type': 'vocabulary',
            'log_data': {
                'words_learned': log_data.get('words_learned', []),
                'count': log_data.get('count', len(log_data.get('words_learned', []))),
                'review': log_data.get('review', False)
            }
        }
    
    def calculate_progress(self, goal_id: int) -> Dict[str, Any]:
        """Calcula progreso del objetivo de aprendizaje"""
        
        # Estructura de ejemplo
        return {
            'percentage': 35,
            'total_hours_studied': 28,
            'target_hours': 80,
            'lessons_completed': 42,
            'current_streak': 7,  # días consecutivos
            'longest_streak': 12,
            'weekly_hours': 6.5,
            'on_track': True,
            'insights': [
                '¡7 días seguidos estudiando! 🔥',
                'Has completado 42 lecciones',
                'Promedio de 6.5h por semana - excelente ritmo',
                'Al paso actual, terminarás 2 semanas antes ✓'
            ],
            'vocabulary_stats': {
                'total_words': 340,
                'words_this_week': 45
            }
        }
    
    def generate_feedback(self, progress_data: Dict) -> str:
        """Genera feedback personalizado"""
        
        streak_emoji = '🔥' if progress_data['current_streak'] >= 7 else '✨'
        
        return f"""¡Buen progreso! {streak_emoji}

Progreso: {progress_data['percentage']}%
Horas estudiadas: {progress_data['total_hours_studied']}/{progress_data['target_hours']}h
Racha actual: {progress_data['current_streak']} días

{chr(10).join(progress_data['insights'])}

¡Sigue así! 📚"""
    
    def _generate_study_plan(self, data: Dict) -> Dict:
        """Genera plan de estudio personalizado"""
        
        subtype = data.get('subtype')
        minutes_per_day = data.get('study_time_per_day', 30)
        
        if subtype == 'language':
            # Plan balanceado para idiomas
            return {
                'weekly_structure': [
                    {'day': 'Lunes', 'focus': 'Vocabulario y gramática', 'duration': minutes_per_day},
                    {'day': 'Martes', 'focus': 'Listening comprehension', 'duration': minutes_per_day},
                    {'day': 'Miércoles', 'focus': 'Speaking practice', 'duration': minutes_per_day},
                    {'day': 'Jueves', 'focus': 'Writing exercises', 'duration': minutes_per_day},
                    {'day': 'Viernes', 'focus': 'Review y práctica mixta', 'duration': minutes_per_day}
                ],
                'milestones': self._generate_milestones(data)
            }
        
        return {
            'weekly_structure': [],
            'milestones': []
        }
    
    def _generate_milestones(self, data: Dict) -> List[Dict]:
        """Genera hitos intermedios"""
        
        subtype = data.get('subtype')
        
        if subtype == 'language':
            current = data.get('current_level', 'A1')
            target = data.get('target_level', 'B2')
            
            # Generar hitos entre niveles
            current_idx = self.LANGUAGE_LEVELS.index(current) if current in self.LANGUAGE_LEVELS else 0
            target_idx = self.LANGUAGE_LEVELS.index(target) if target in self.LANGUAGE_LEVELS else 3
            
            milestones = []
            for i in range(current_idx + 1, target_idx + 1):
                milestones.append({
                    'level': self.LANGUAGE_LEVELS[i],
                    'description': f'Alcanzar nivel {self.LANGUAGE_LEVELS[i]}',
                    'weeks_estimated': (i - current_idx) * 8  # 8 semanas por nivel (aprox)
                })
            
            return milestones
        
        return []
    
    def _estimate_total_hours(self, data: Dict) -> int:
        """Estima horas totales necesarias"""
        
        subtype = data.get('subtype')
        
        if subtype == 'language':
            current = data.get('current_level', 'A1')
            target = data.get('target_level', 'B2')
            
            # Estimaciones aproximadas (según CEFR)
            level_hours = {
                'A1': 80,
                'A2': 160,
                'B1': 320,
                'B2': 480,
                'C1': 640,
                'C2': 800
            }
            
            current_hours = level_hours.get(current, 0)
            target_hours = level_hours.get(target, 480)
            
            return target_hours - current_hours
        
        # Default para otros tipos
        return 100
    
    def _generate_title(self, data: Dict) -> str:
        """Genera título del objetivo"""
        
        subtype = data.get('subtype')
        target = data.get('target')
        
        if subtype == 'language':
            target_level = data.get('target_level', 'intermedio')
            return f"Aprender {target} - nivel {target_level}"
        elif subtype == 'skill':
            return f"Desarrollar habilidad: {target}"
        elif subtype == 'certification':
            return f"Certificación: {target}"
        elif subtype == 'reading':
            return f"Programa de lectura: {target}"
        
        return f"Aprender {target}"
    
    def _generate_description(self, data: Dict) -> str:
        """Genera descripción del objetivo"""
        
        minutes_per_day = data.get('study_time_per_day', 30)
        days_per_week = data.get('days_per_week', 5)
        
        return f"{minutes_per_day} min/día, {days_per_week} días/semana"
