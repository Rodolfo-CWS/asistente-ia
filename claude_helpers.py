"""
Implementación real de IA usando Claude API
"""

import anthropic
import json

def classify_intent_with_claude(claude_client: anthropic.Anthropic, 
                                message: str, 
                                context: dict) -> dict:
    """
    Usa Claude API para clasificar la intención del mensaje.
    """
    
    prompt = f"""Analiza este mensaje de WhatsApp y clasifica la intención del usuario.

Mensaje: "{message}"
Contexto de conversación: {json.dumps(context, ensure_ascii=False)}

Clasifica en UNA de estas categorías:
- create_goal: Usuario quiere crear un objetivo nuevo
- log_progress: Usuario está reportando progreso (peso, sesión completada, etc.)
- view_progress: Usuario quiere ver su progreso actual
- greeting: Saludo inicial
- help: Pide ayuda
- general: Conversación general

Responde SOLO con JSON:
{{"type": "...", "confidence": 0.0-1.0}}"""

    message = claude_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text.strip()
    
    # Parsear JSON
    try:
        result = json.loads(response_text)
        return result
    except:
        return {"type": "general", "confidence": 0.5}


def extract_goal_info_with_claude(claude_client: anthropic.Anthropic,
                                  message: str,
                                  goal_type: str,
                                  current_data: dict) -> dict:
    """
    Extrae información estructurada del mensaje usando Claude.
    """
    
    schemas = {
        'fitness': """
{
    "current_weight": número en kg (si lo menciona),
    "target_weight": número en kg (si lo menciona),
    "height": número en cm (si lo menciona),
    "age": número (si lo menciona),
    "gender": "M" o "F" (si lo menciona),
    "target_date": "YYYY-MM-DD" (si menciona fecha)
}""",
        'learning': """
{
    "target": string (idioma, habilidad, etc),
    "current_level": string (si lo menciona),
    "target_level": string (si lo menciona),
    "study_time_per_day": número en minutos (si lo menciona)
}""",
        'productivity': """
{
    "habit_name": string,
    "frequency": "daily" | "weekdays" | "weekends",
    "target_days": número (si menciona cuántos días),
    "duration_minutes": número (si lo menciona)
}"""
    }
    
    prompt = f"""Extrae información estructurada de este mensaje para un objetivo de {goal_type}.

Mensaje: "{message}"

Datos ya recopilados:
{json.dumps(current_data, ensure_ascii=False, indent=2)}

Esquema esperado:
{schemas[goal_type]}

SOLO extrae información que esté EXPLÍCITA en el mensaje.
Si no hay nueva información, devuelve {{}}.

Responde SOLO con JSON:"""

    message = claude_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text.strip()
    
    try:
        return json.loads(response_text)
    except:
        return {}


def parse_diet_with_claude(claude_client: anthropic.Anthropic, 
                           diet_text: str) -> dict:
    """
    Parsea texto de dieta a estructura JSON usando Claude.
    """
    
    prompt = f"""Convierte esta dieta en formato estructurado JSON.

{diet_text}

Estructura JSON esperada:
{{
    "name": "Nombre de la dieta",
    "total_calories": número total estimado,
    "meals": [
        {{
            "name": "Desayuno/Comida/Cena",
            "time": "HH:MM" o null,
            "foods": ["alimento 1", "alimento 2"],
            "calories": número estimado,
            "macros": {{
                "protein": gramos,
                "carbs": gramos,
                "fats": gramos
            }}
        }}
    ]
}}

Haz tu mejor estimación de calorías y macros basado en porciones típicas.
Responde SOLO con JSON válido:"""

    message = claude_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text.strip()
    
    try:
        return json.loads(response_text)
    except:
        return {
            "name": "Dieta del usuario",
            "total_calories": 0,
            "meals": []
        }


def general_conversation_with_claude(claude_client: anthropic.Anthropic,
                                     message: str,
                                     context: dict) -> str:
    """
    Conversación general usando Claude con personalidad de asistente personal.
    """
    
    system_prompt = """Eres un asistente personal de IA motivador y amigable.
Ayudas a las personas a lograr sus objetivos de fitness, aprendizaje y productividad.

Personalidad:
- Motivador pero no empalagoso
- Usa emojis ocasionalmente (💪 🎯 📚 ✨)
- Respuestas cortas y directas
- Celebra logros
- Da consejos prácticos

Mantén respuestas breves (2-3 oraciones máximo)."""

    messages = []
    
    # Agregar historial si existe
    if context.get('conversation_history'):
        messages.extend(context['conversation_history'])
    
    messages.append({"role": "user", "content": message})
    
    response = claude_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=150,
        system=system_prompt,
        messages=messages
    )
    
    return response.content[0].text
