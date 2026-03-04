from typing import Dict, Any, Optional, List
from processors.fitness_processor import FitnessGoalProcessor
from processors.learning_processor import LearningGoalProcessor
from processors.productivity_processor import ProductivityGoalProcessor

class GoalOrchestrator:
    """
    Orquestador principal que maneja todos los tipos de objetivos.
    Decide qué procesador usar y coordina las operaciones.
    """
    
    def __init__(self, db_session):
        self.db = db_session
        
        # Inicializar procesadores
        self.fitness = FitnessGoalProcessor(db_session)
        self.learning = LearningGoalProcessor(db_session)
        self.productivity = ProductivityGoalProcessor(db_session)
        
        # Mapeo de tipos a procesadores
        self.processors = {
            'fitness': self.fitness,
            'learning': self.learning,
            'productivity': self.productivity
        }
    
    def create_goal(self, user_id: int, goal_type: str, conversation_data: Dict) -> Dict[str, Any]:
        """
        Crea un objetivo del tipo especificado.
        
        Args:
            user_id: ID del usuario
            goal_type: 'fitness', 'learning', o 'productivity'
            conversation_data: Datos extraídos de la conversación con el usuario
            
        Returns:
            Dict con información del objetivo creado
        """
        
        processor = self._get_processor(goal_type)
        
        if not processor:
            return {
                'success': False,
                'error': f'Tipo de objetivo no soportado: {goal_type}'
            }
        
        try:
            # Crear objetivo usando el procesador específico
            goal_data = processor.create_goal_from_conversation(user_id, conversation_data)
            
            # Aquí se guardaría en la base de datos
            # goal = Goal(**goal_data, user_id=user_id)
            # self.db.add(goal)
            # self.db.commit()
            
            return {
                'success': True,
                'goal_id': 123,  # ID del objetivo creado
                'goal_data': goal_data,
                'message': self._generate_creation_message(goal_type, goal_data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def log_progress(self, goal_id: int, log_data: Dict) -> Dict[str, Any]:
        """
        Registra progreso para cualquier tipo de objetivo.
        
        Args:
            goal_id: ID del objetivo
            log_data: Datos del progreso a registrar
            
        Returns:
            Dict con resultado del registro
        """
        
        # Obtener tipo de objetivo
        goal_type = self._get_goal_type(goal_id)
        processor = self._get_processor(goal_type)
        
        if not processor:
            return {'success': False, 'error': 'Objetivo no encontrado'}
        
        try:
            # Registrar progreso
            log_result = processor.log_progress(goal_id, log_data)
            
            # Guardar en DB
            # progress_log = ProgressLog(**log_result, goal_id=goal_id)
            # self.db.add(progress_log)
            # self.db.commit()
            
            # Calcular progreso actualizado
            progress = processor.calculate_progress(goal_id)
            
            # Generar feedback
            feedback = processor.generate_feedback(progress)
            
            return {
                'success': True,
                'progress': progress,
                'feedback': feedback
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_progress(self, goal_id: int) -> Dict[str, Any]:
        """Obtiene el progreso actual de un objetivo"""
        
        goal_type = self._get_goal_type(goal_id)
        processor = self._get_processor(goal_type)
        
        if not processor:
            return {'success': False, 'error': 'Objetivo no encontrado'}
        
        try:
            progress = processor.calculate_progress(goal_id)
            feedback = processor.generate_feedback(progress)
            
            return {
                'success': True,
                'progress': progress,
                'feedback': feedback
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def process_diet(self, user_id: int, goal_id: int, diet_data: Dict) -> Dict[str, Any]:
        """
        Procesa una dieta proporcionada por el usuario (solo para fitness)
        
        Args:
            user_id: ID del usuario
            goal_id: ID del objetivo de fitness
            diet_data: Datos de la dieta (texto, JSON, etc.)
        """
        
        goal_type = self._get_goal_type(goal_id)
        
        if goal_type != 'fitness':
            return {
                'success': False,
                'error': 'Las dietas solo aplican a objetivos de fitness'
            }
        
        try:
            processed_diet = self.fitness.process_diet(diet_data)
            
            # Guardar dieta en DB
            # diet = Diet(user_id=user_id, goal_id=goal_id, diet_data=processed_diet)
            # self.db.add(diet)
            # self.db.commit()
            
            return {
                'success': True,
                'diet': processed_diet,
                'message': f"Dieta procesada: {processed_diet['total_calories']} cal/día"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_reminders(self, user_id: int) -> List[Dict]:
        """
        Verifica qué recordatorios se deben enviar (principalmente para productivity)
        
        Returns:
            Lista de recordatorios a enviar
        """
        
        reminders = []
        
        # Obtener objetivos activos del usuario
        # goals = self.db.query(Goal).filter_by(user_id=user_id, status='active').all()
        
        # Por ahora, ejemplo hardcoded
        goals = [
            {'id': 1, 'goal_type': 'productivity'},
            {'id': 2, 'goal_type': 'fitness'}
        ]
        
        for goal in goals:
            processor = self._get_processor(goal['goal_type'])
            
            if hasattr(processor, 'check_reminder_needed'):
                reminder = processor.check_reminder_needed(goal['id'])
                
                if reminder.get('send_reminder'):
                    reminders.append({
                        'goal_id': goal['id'],
                        'message': reminder['message']
                    })
        
        return reminders
    
    def _get_processor(self, goal_type: str):
        """Obtiene el procesador adecuado para el tipo de objetivo"""
        return self.processors.get(goal_type)
    
    def _get_goal_type(self, goal_id: int) -> Optional[str]:
        """Obtiene el tipo de un objetivo por su ID"""
        
        # En producción, consultar la DB
        # goal = self.db.query(Goal).filter_by(id=goal_id).first()
        # return goal.goal_type if goal else None
        
        # Por ahora, retornar ejemplo
        return 'fitness'
    
    def _generate_creation_message(self, goal_type: str, goal_data: Dict) -> str:
        """Genera mensaje de confirmación al crear objetivo"""
        
        title = goal_data.get('title')
        description = goal_data.get('description')
        
        messages = {
            'fitness': f"✓ Objetivo de fitness creado: {title}\n{description}\n\n¡Vamos a lograrlo! 💪",
            'learning': f"✓ Objetivo de aprendizaje creado: {title}\n{description}\n\n¡A estudiar! 📚",
            'productivity': f"✓ Hábito creado: {title}\n{description}\n\nEmpecemos hoy mismo! ✨"
        }
        
        return messages.get(goal_type, f"✓ Objetivo creado: {title}")
