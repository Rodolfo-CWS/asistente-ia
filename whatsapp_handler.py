"""
Manejador de conversaciones de WhatsApp para crear y gestionar objetivos
"""

from typing import Dict, Any, Optional
from enum import Enum
from goal_orchestrator import GoalOrchestrator

class ConversationState(Enum):
    """Estados de la conversación"""
    IDLE = "idle"
    ONBOARDING = "onboarding"
    CREATING_GOAL = "creating_goal"
    LOGGING_PROGRESS = "logging_progress"
    VIEWING_PROGRESS = "viewing_progress"

class GoalConversationHandler:
    """
    Maneja las conversaciones de WhatsApp para crear objetivos.
    Usa IA (Claude) para entender intenciones y extraer información.
    """
    
    def __init__(self, db_session, claude_client):
        self.db = db_session
        self.claude = claude_client
        self.orchestrator = GoalOrchestrator(db_session)
        
        # Almacenar estado de conversación por usuario
        self.user_states = {}
        self.conversation_context = {}
    
    def handle_message(self, user_id: int, phone: str, message: str) -> str:
        """
        Punto de entrada principal para mensajes de WhatsApp.

        Returns:
            Respuesta a enviar al usuario
        """

        # Obtener o crear estado del usuario
        state = self.user_states.get(user_id, ConversationState.IDLE)
        context = self.conversation_context.get(user_id, {})

        # Clasificar intención del mensaje usando IA
        intent = self._classify_intent(message, context)
        
        # Manejar según intención
        if intent['type'] == 'create_goal':
            return self._handle_goal_creation(user_id, message, intent, context)
        
        elif intent['type'] == 'log_progress':
            return self._handle_progress_logging(user_id, message, intent, context)
        
        elif intent['type'] == 'view_progress':
            return self._handle_view_progress(user_id, intent)
        
        elif intent['type'] == 'greeting':
            return self._handle_greeting(user_id, phone)
        
        elif intent['type'] == 'help':
            return self._handle_help()
        
        else:
            # Conversación general con Claude
            return self._general_conversation(message, context)
    
    def _classify_intent(self, message: str, context: Dict) -> Dict[str, Any]:
        """
        Usa Claude API para clasificar la intención del mensaje.

        En producción, esto llamaría a Claude API con un prompt optimizado.
        Por ahora, lógica simplificada basada en keywords.
        """

        # Si hay un flujo de creación de objetivo en progreso, continuar con él
        if 'goal_creation' in context:
            return {'type': 'create_goal', 'confidence': 1.0}

        message_lower = message.lower()

        # Keywords para crear objetivo
        goal_keywords = ['quiero', 'objetivo', 'meta', 'bajar peso', 'aprender',
                         'hábito', 'meditar', 'ejercicio', 'estudiar']

        # Keywords para registrar progreso
        progress_keywords = ['pesé', 'pese', 'peso', 'completé', 'complete', 'hice',
                            'estudié', 'estudie', 'terminé', 'termine', 'medité',
                            'medite', 'workout']

        # Keywords para ver progreso
        view_keywords = ['progreso', 'cómo voy', 'avance', 'estado', 'resumen']

        if any(kw in message_lower for kw in goal_keywords):
            return {'type': 'create_goal', 'confidence': 0.8}

        elif any(kw in message_lower for kw in progress_keywords):
            return {'type': 'log_progress', 'confidence': 0.7}

        elif any(kw in message_lower for kw in view_keywords):
            return {'type': 'view_progress', 'confidence': 0.9}

        elif message_lower in ['hola', 'hi', 'hey']:
            return {'type': 'greeting', 'confidence': 1.0}

        elif 'ayuda' in message_lower or 'help' in message_lower:
            return {'type': 'help', 'confidence': 1.0}

        return {'type': 'general', 'confidence': 0.5}
    
    def _handle_goal_creation(self, user_id: int, message: str, 
                             intent: Dict, context: Dict) -> str:
        """
        Maneja la creación de un nuevo objetivo.
        Hace preguntas para recopilar información necesaria.
        """
        
        # Si es el primer mensaje sobre el objetivo
        if 'goal_creation' not in context:
            # Detectar tipo de objetivo
            goal_type = self._detect_goal_type(message)
            
            context['goal_creation'] = {
                'type': goal_type,
                'data': {},
                'step': 0
            }
            self.conversation_context[user_id] = context
            
            # Iniciar flujo según tipo
            if goal_type == 'fitness':
                return self._start_fitness_flow(user_id, message)
            elif goal_type == 'learning':
                return self._start_learning_flow(user_id, message)
            elif goal_type == 'productivity':
                return self._start_productivity_flow(user_id, message)
        
        # Continuar flujo existente
        return self._continue_goal_flow(user_id, message, context)
    
    def _detect_goal_type(self, message: str) -> str:
        """Detecta el tipo de objetivo basado en el mensaje"""
        
        message_lower = message.lower()
        
        fitness_keywords = ['peso', 'bajar', 'adelgazar', 'músculo', 'gym', 
                           'ejercicio', 'fit', 'dieta', 'calorías']
        learning_keywords = ['aprender', 'estudiar', 'idioma', 'inglés', 
                            'curso', 'leer', 'certificación']
        productivity_keywords = ['hábito', 'meditar', 'rutina', 'despertar', 
                                'productivo', 'días']
        
        fitness_score = sum(1 for kw in fitness_keywords if kw in message_lower)
        learning_score = sum(1 for kw in learning_keywords if kw in message_lower)
        productivity_score = sum(1 for kw in productivity_keywords if kw in message_lower)
        
        scores = {
            'fitness': fitness_score,
            'learning': learning_score,
            'productivity': productivity_score
        }
        
        return max(scores, key=scores.get)
    
    def _start_fitness_flow(self, user_id: int, message: str) -> str:
        """Inicia flujo de creación de objetivo de fitness"""
        
        # Usar Claude para extraer info del mensaje inicial
        # y determinar qué preguntar
        
        return """¡Perfecto! Vamos a crear tu objetivo de fitness 💪

Para armar el mejor plan necesito saber:

1. ¿Cuál es tu peso actual? (en kg)"""
    
    def _start_learning_flow(self, user_id: int, message: str) -> str:
        """Inicia flujo de creación de objetivo de aprendizaje"""
        
        return """¡Genial! Vamos a crear tu plan de aprendizaje 📚

¿Qué quieres aprender específicamente?
(ej: Inglés, Python, Guitarra, etc.)"""
    
    def _start_productivity_flow(self, user_id: int, message: str) -> str:
        """Inicia flujo de creación de objetivo de productividad"""
        
        return """¡Excelente! Vamos a crear ese hábito ✨

¿Qué hábito quieres desarrollar?
(ej: Meditar, Despertar temprano, Leer, etc.)"""
    
    def _continue_goal_flow(self, user_id: int, message: str, context: Dict) -> str:
        """Continúa el flujo de creación de objetivo"""

        creation_data = context['goal_creation']
        goal_type = creation_data['type']
        step = creation_data['step']

        # Incrementar step primero (porque step 0 ya mostró la primera pregunta)
        creation_data['step'] += 1
        current_step = creation_data['step']

        # Extraer información del mensaje usando IA
        extracted_info = self._extract_info_with_ai(message, goal_type, current_step)

        # Actualizar datos
        creation_data['data'].update(extracted_info)
        
        # Determinar siguiente pregunta o crear objetivo
        if self._has_all_required_info(goal_type, creation_data['data']):
            # Crear objetivo
            result = self.orchestrator.create_goal(
                user_id=user_id,
                goal_type=goal_type,
                conversation_data=creation_data['data']
            )
            
            # Limpiar contexto
            del context['goal_creation']
            self.conversation_context[user_id] = context
            
            if result['success']:
                return result['message']
            else:
                return f"Hubo un error: {result['error']}"
        
        # Hacer siguiente pregunta
        next_question = self._get_next_question(goal_type, creation_data['data'], current_step)
        return next_question
    
    def _extract_info_with_ai(self, message: str, goal_type: str, step: int) -> Dict:
        """
        Extrae información del mensaje usando IA.
        En producción, esto usa Claude API con prompts específicos.
        """

        # Implementación simplificada
        # En producción: llamar a Claude API para extraer info estructurada

        if goal_type == 'fitness':
            # Intentar extraer peso, altura, edad, etc.
            import re

            # Buscar números (peso, altura, edad)
            numbers = re.findall(r'\d+', message)
            message_lower = message.lower()

            if step == 1 and numbers:
                return {'current_weight': int(numbers[0])}
            elif step == 2 and numbers:
                return {'target_weight': int(numbers[0])}
            elif step == 3 and numbers:
                return {'height': int(numbers[0])}
            elif step == 4 and numbers:
                return {'age': int(numbers[0])}
            elif step == 5:
                # Extraer género
                if 'h' in message_lower or 'hombre' in message_lower or 'm' == message_lower.strip():
                    return {'gender': 'M'}
                elif 'mujer' in message_lower or 'f' in message_lower:
                    return {'gender': 'F'}
                return {'gender': message_lower.strip().upper()}
            elif step == 6:
                # Extraer deadline (fecha límite)
                return {'deadline': message}

        elif goal_type == 'learning':
            if step == 1:
                return {'target': message}
            elif step == 2:
                return {'current_level': message}
            elif step == 3:
                return {'target_level': message}
            elif step == 4:
                numbers = re.findall(r'\d+', message)
                if numbers:
                    return {'study_time_per_day': int(numbers[0])}

        elif goal_type == 'productivity':
            if step == 1:
                return {'habit_name': message}
            elif step == 2:
                return {'frequency': message}
            elif step == 3:
                numbers = re.findall(r'\d+', message)
                if numbers:
                    return {'target_days': int(numbers[0])}

        return {}
    
    def _has_all_required_info(self, goal_type: str, data: Dict) -> bool:
        """Verifica si se tiene toda la información necesaria"""

        required_fields = {
            'fitness': ['current_weight', 'target_weight', 'height', 'age', 'gender', 'deadline'],
            'learning': ['target', 'current_level', 'target_level', 'study_time_per_day'],
            'productivity': ['habit_name', 'frequency', 'target_days']
        }

        required = required_fields.get(goal_type, [])
        return all(field in data for field in required)
    
    def _get_next_question(self, goal_type: str, data: Dict, step: int) -> str:
        """Retorna la siguiente pregunta según el tipo y paso"""
        
        if goal_type == 'fitness':
            questions = [
                "¿Cuál es tu peso actual? (kg)",
                "¿Cuál es tu peso objetivo? (kg)",
                "¿Cuál es tu altura? (cm)",
                "¿Cuántos años tienes?",
                "¿Eres hombre o mujer? (H/M)",
                "¿Para cuándo quieres lograrlo? (ej: 2 meses, 29 de marzo)"
            ]
        elif goal_type == 'learning':
            questions = [
                "¿Qué quieres aprender?",
                "¿Cuál es tu nivel actual? (ej: principiante, intermedio)",
                "¿Cuál es tu nivel objetivo?",
                "¿Cuántos minutos al día puedes estudiar?"
            ]
        else:  # productivity
            questions = [
                "¿Qué hábito quieres crear?",
                "¿Con qué frecuencia? (diario, entre semana, etc.)",
                "¿Por cuántos días quieres hacerlo?"
            ]
        
        if step < len(questions):
            return questions[step]
        
        return "¿Algo más que quieras agregar?"
    
    def _handle_progress_logging(self, user_id: int, message: str, 
                                 intent: Dict, context: Dict) -> str:
        """Maneja el registro de progreso"""
        
        # Obtener objetivos activos del usuario
        # En producción: consultar DB
        active_goals = [
            {'id': 1, 'type': 'fitness', 'title': 'Bajar 5kg'}
        ]
        
        if not active_goals:
            return "No tienes objetivos activos. ¿Quieres crear uno?"
        
        # Si solo tiene un objetivo, asumir que es ese
        goal = active_goals[0]
        
        # Extraer datos del progreso usando IA
        log_data = self._extract_progress_data(message, goal['type'])
        
        # Registrar progreso
        result = self.orchestrator.log_progress(goal['id'], log_data)
        
        if result['success']:
            return result['feedback']
        else:
            return f"Error al registrar: {result['error']}"
    
    def _extract_progress_data(self, message: str, goal_type: str) -> Dict:
        """Extrae datos de progreso del mensaje usando IA"""
        
        # Implementación simplificada
        import re
        
        if goal_type == 'fitness':
            # Buscar peso
            numbers = re.findall(r'\d+\.?\d*', message)
            if numbers:
                return {
                    'type': 'weight_update',
                    'weight': float(numbers[0])
                }
        
        return {'type': 'completion'}
    
    def _handle_view_progress(self, user_id: int, intent: Dict) -> str:
        """Maneja solicitud de ver progreso"""
        
        # Obtener objetivos activos
        active_goals = [
            {'id': 1, 'type': 'fitness'}
        ]
        
        if not active_goals:
            return "No tienes objetivos activos."
        
        responses = []
        
        for goal in active_goals:
            progress = self.orchestrator.get_progress(goal['id'])
            if progress['success']:
                responses.append(progress['feedback'])
        
        return "\n\n".join(responses)
    
    def _handle_greeting(self, user_id: int, phone: str) -> str:
        """Maneja saludos iniciales"""
        
        # Verificar si es usuario nuevo
        # is_new = not self.db.query(User).filter_by(phone_number=phone).first()
        is_new = True  # Simulado
        
        if is_new:
            return """¡Hola! 👋 Soy tu asistente personal de IA.

Te ayudo a lograr tus objetivos de:
💪 Fitness y salud
📚 Aprendizaje
✨ Productividad y hábitos

¿Qué objetivo te gustaría trabajar?"""
        else:
            return "¡Hola de nuevo! ¿En qué puedo ayudarte hoy?"
    
    def _handle_help(self) -> str:
        """Maneja solicitudes de ayuda"""
        
        return """Puedo ayudarte con:

✓ Crear objetivos de fitness, aprendizaje o productividad
✓ Hacer seguimiento de tu progreso
✓ Enviarte recordatorios
✓ Darte feedback personalizado

Ejemplos de lo que puedes decir:
• "Quiero bajar 5kg"
• "Quiero aprender inglés"
• "Quiero meditar 30 días seguidos"
• "Pesé 78kg hoy"
• "Cómo voy con mi objetivo?"

¿Qué te gustaría hacer?"""
    
    def _general_conversation(self, message: str, context: Dict) -> str:
        """Conversación general usando Claude"""
        
        # Aquí se llamaría a Claude API para una conversación natural
        return "Interesante. ¿Puedes contarme más sobre eso?"
