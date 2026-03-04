from datetime import datetime, timedelta
from typing import Dict, Any, List

class ProductivityGoalProcessor:
    """Procesa objetivos de productividad: hábitos, rutinas, tareas recurrentes"""
    
    GOAL_SUBTYPES = {
        'habit': 'Crear hábito',
        'routine': 'Establecer rutina',
        'challenge': 'Desafío de días',
        'time_management': 'Gestión de tiempo',
        'focus': 'Mejorar concentración'
    }
    
    # Frecuencias comunes para hábitos
    FREQUENCIES = {
        'daily': 'Diario',
        'weekdays': 'Entre semana',
        'weekends': 'Fines de semana',
        'specific_days': 'Días específicos',
        'every_x_days': 'Cada X días'
    }
    
    def __init__(self, db_session):
        self.db = db_session
    
    def create_goal_from_conversation(self, user_id: int, conversation_data: Dict) -> Dict[str, Any]:
        """
        Crea objetivo de productividad.
        
        conversation_data esperado:
        {
            'subtype': 'habit',
            'habit_name': 'Meditar',
            'frequency': 'daily',
            'target_days': 30,  # Para challenges tipo "30 días de..."
            'time_of_day': 'morning',
            'duration_minutes': 10,
            'reminder_time': '07:00',
            'specific_days': ['Monday', 'Wednesday', 'Friday'],  # Si frequency = specific_days
            'tracking_metric': 'binary'  # binary (sí/no) o 'duration' o 'count'
        }
        """
        
        subtype = conversation_data.get('subtype', 'habit')
        
        goal_data = {
            'subtype': subtype,
            'habit_name': conversation_data.get('habit_name'),
            'frequency': {
                'type': conversation_data.get('frequency', 'daily'),
                'specific_days': conversation_data.get('specific_days', []),
                'every_x_days': conversation_data.get('every_x_days', 1)
            },
            'schedule': {
                'time_of_day': conversation_data.get('time_of_day'),
                'specific_time': conversation_data.get('reminder_time'),
                'duration_minutes': conversation_data.get('duration_minutes', 10),
                'flexible': conversation_data.get('flexible_timing', True)
            },
            'target': {
                'total_days': conversation_data.get('target_days', 30),
                'completion_rate': conversation_data.get('target_completion_rate', 80)  # % mínimo
            },
            'tracking': {
                'metric': conversation_data.get('tracking_metric', 'binary'),
                'allow_partial': conversation_data.get('allow_partial', False),
                'require_note': conversation_data.get('require_note', False)
            },
            'reminders': {
                'enabled': conversation_data.get('reminders_enabled', True),
                'time': conversation_data.get('reminder_time'),
                'advance_minutes': conversation_data.get('reminder_advance', 0)
            },
            'stats': {
                'current_streak': 0,
                'longest_streak': 0,
                'total_completions': 0,
                'completion_rate': 0
            }
        }
        
        return {
            'goal_type': 'productivity',
            'title': self._generate_title(conversation_data),
            'description': self._generate_description(conversation_data),
            'target_date': self._calculate_target_date(conversation_data),
            'goal_data': goal_data
        }
    
    def log_progress(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """
        Registra progreso: hábito completado, skipped, notas, etc.
        """
        
        log_type = log_data.get('type', 'completion')
        
        if log_type == 'completion':
            return self._log_completion(goal_id, log_data)
        elif log_type == 'skip':
            return self._log_skip(goal_id, log_data)
        elif log_type == 'partial':
            return self._log_partial(goal_id, log_data)
        
        return {'status': 'unknown_type'}
    
    def _log_completion(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra hábito completado"""
        
        return {
            'log_type': 'completion',
            'log_data': {
                'completed': True,
                'duration_minutes': log_data.get('duration_minutes'),
                'quality': log_data.get('quality'),  # 1-5 scale
                'time_of_day': log_data.get('time_of_day'),
                'notes': log_data.get('notes')
            }
        }
    
    def _log_skip(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra día saltado"""
        
        return {
            'log_type': 'skip',
            'log_data': {
                'completed': False,
                'reason': log_data.get('reason'),
                'intentional': log_data.get('intentional', False)  # Rest day vs forgot
            }
        }
    
    def _log_partial(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """Registra completación parcial"""
        
        return {
            'log_type': 'partial',
            'log_data': {
                'completed': 'partial',
                'percentage': log_data.get('percentage', 50),
                'duration_minutes': log_data.get('duration_minutes'),
                'notes': log_data.get('notes')
            }
        }
    
    def calculate_progress(self, goal_id: int) -> Dict[str, Any]:
        """Calcula progreso del objetivo de productividad"""
        
        # Obtener datos
        # goal = self.db.query(Goal).filter_by(id=goal_id).first()
        # logs = self.db.query(ProgressLog).filter_by(goal_id=goal_id).all()
        
        # Calcular racha
        current_streak = self._calculate_streak()
        
        return {
            'percentage': 60,
            'days_completed': 18,
            'target_days': 30,
            'current_streak': current_streak,
            'longest_streak': 12,
            'completion_rate': 85.7,  # De los días esperados
            'total_days_elapsed': 21,
            'on_track': True,
            'streak_status': self._get_streak_status(current_streak),
            'insights': [
                f'Racha actual: {current_streak} días 🔥',
                'Tasa de completación: 85.7%',
                'Has completado 18 de 30 días',
                '¡Estás en un excelente ritmo!'
            ],
            'calendar_view': self._generate_calendar_view()
        }
    
    def _calculate_streak(self) -> int:
        """Calcula racha actual de días consecutivos"""
        
        # Implementación simplificada
        # En producción, revisar logs de los últimos días
        return 7
    
    def _get_streak_status(self, streak: int) -> str:
        """Retorna status de racha"""
        
        if streak >= 30:
            return 'legendary'
        elif streak >= 14:
            return 'excellent'
        elif streak >= 7:
            return 'great'
        elif streak >= 3:
            return 'good'
        else:
            return 'building'
    
    def _generate_calendar_view(self) -> List[Dict]:
        """Genera vista de calendario de últimos 30 días"""
        
        # Generar últimos 30 días
        today = datetime.now()
        calendar = []
        
        for i in range(30):
            date = today - timedelta(days=29-i)
            # En producción, verificar si hay log para ese día
            status = 'completed' if i % 3 != 0 else 'missed'  # Ejemplo
            
            calendar.append({
                'date': date.strftime('%Y-%m-%d'),
                'status': status  # completed, missed, partial, future
            })
        
        return calendar
    
    def generate_feedback(self, progress_data: Dict) -> str:
        """Genera feedback personalizado"""
        
        streak = progress_data['current_streak']
        completion_rate = progress_data['completion_rate']
        
        # Emoji basado en racha
        emoji = '🔥' if streak >= 7 else '✨'
        
        feedback = f"""¡Excelente trabajo! {emoji}

Progreso: {progress_data['percentage']}%
Completados: {progress_data['days_completed']}/{progress_data['target_days']} días
Racha: {streak} días consecutivos

{chr(10).join(progress_data['insights'])}
"""
        
        # Motivación adicional
        if streak >= 7:
            feedback += "\n¡No rompas la racha! 💪"
        elif completion_rate >= 80:
            feedback += "\nVas muy bien! 🎯"
        
        return feedback
    
    def check_reminder_needed(self, goal_id: int) -> Dict[str, Any]:
        """Verifica si se debe enviar recordatorio"""
        
        # Obtener configuración de recordatorios
        # goal = self.db.query(Goal).filter_by(id=goal_id).first()
        
        now = datetime.now()
        reminder_time = "07:00"  # De goal_data
        
        # Verificar si ya completó hoy
        # completed_today = self._check_completion_today(goal_id)
        
        return {
            'send_reminder': True,
            'message': "¡Hora de meditar! 🧘‍♂️ 10 minutos para empezar bien el día."
        }
    
    def _generate_title(self, data: Dict) -> str:
        """Genera título del objetivo"""
        
        habit_name = data.get('habit_name', 'Mi hábito')
        target_days = data.get('target_days', 30)
        
        return f"{habit_name} - {target_days} días"
    
    def _generate_description(self, data: Dict) -> str:
        """Genera descripción del objetivo"""
        
        frequency = data.get('frequency', 'daily')
        duration = data.get('duration_minutes', 10)
        
        freq_text = self.FREQUENCIES.get(frequency, 'regular')
        
        return f"{freq_text}, {duration} min por sesión"
    
    def _calculate_target_date(self, data: Dict) -> str:
        """Calcula fecha objetivo basada en target_days"""
        
        target_days = data.get('target_days', 30)
        target_date = datetime.now() + timedelta(days=target_days)
        
        return target_date.isoformat()
