# 📝 Instrucciones para Claude Code (VS Code)

Hola Claude Code! Por favor ayuda a Rodolfo a subir este proyecto a GitHub.

## Contexto del Proyecto

Este es un **Asistente de IA Personal** que funciona por WhatsApp para ayudar con objetivos de fitness, aprendizaje y productividad.

- Usuario: Rodolfo
- GitHub: https://github.com/Rodolfo-CWS
- Repositorio nuevo: `asistente-ia`

## Archivos del Proyecto

Todo está listo. Solo necesita subirse a GitHub.

### Archivos principales:
- `main.py` - Servidor FastAPI con webhook de WhatsApp
- `models.py` - Modelos de base de datos SQLAlchemy
- `goal_orchestrator.py` - Orquestador de objetivos
- `whatsapp_handler.py` - Manejo de conversaciones
- `claude_helpers.py` - Integración con Claude API
- `processors/` - Procesadores de 3 tipos de objetivos

### Configuración:
- `requirements.txt` - Dependencias Python
- `.env.example` - Template de variables de entorno
- `.gitignore` - Ya configurado
- `LICENSE` - MIT License

### Documentación:
- `README_GITHUB.md` - README principal para GitHub (renombrar a README.md al subir)
- `README.md` - README técnico
- `EMPIEZA_AQUI.md` - Guía para empezar
- `docs/` - Documentación completa

## Tarea

Por favor ayuda a Rodolfo a:

1. **Inicializar Git** en esta carpeta
2. **Crear repositorio** en GitHub (https://github.com/Rodolfo-CWS/asistente-ia)
3. **Hacer commit inicial** con mensaje: "Initial commit - MVP Asistente IA Personal"
4. **Push al repositorio**

## Notas Importantes

- El archivo `README_GITHUB.md` debe renombrarse a `README.md` en el commit (es el README principal para GitHub)
- El `README.md` actual puede renombrarse a `README_TECNICO.md`
- El archivo `.env.example` NO debe ser `.env` (ese es local y privado)
- Verificar que `.gitignore` esté incluido para evitar subir archivos sensibles

## Siguiente Paso Después de Subir

Una vez en GitHub, Rodolfo necesitará:
1. Clonar el repo localmente
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar `.env` con sus API keys
4. Probar localmente: `python test_local.py`

¡Gracias Claude Code! 🚀
