from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import anthropic

from models import Base, User, Goal, ProgressLog
from whatsapp_handler import GoalConversationHandler

load_dotenv()

# FastAPI app
app = FastAPI()

# Database
# Render PostgreSQL uses 'postgres://' but SQLAlchemy 1.4+ requires 'postgresql://'
database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

# Claude API
claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(From: str = Form(...), Body: str = Form(...)):
    """Endpoint que recibe mensajes de WhatsApp vía Twilio"""
    
    # Crear sesión de DB
    db = SessionLocal()
    
    try:
        # Extraer número de teléfono (quitar "whatsapp:")
        phone = From.replace("whatsapp:", "")
        
        # Buscar o crear usuario
        user = db.query(User).filter_by(phone_number=phone).first()
        if not user:
            user = User(phone_number=phone)
            db.add(user)
            db.commit()
        
        # Procesar mensaje
        handler = GoalConversationHandler(db, claude_client)
        response_text = handler.handle_message(user.id, phone, Body)
        
        # Crear respuesta de Twilio
        resp = MessagingResponse()
        resp.message(response_text)
        
        return Response(content=str(resp), media_type="application/xml")
    
    finally:
        db.close()

@app.get("/health")
def health_check():
    """Health check endpoint - verifies database connectivity"""
    try:
        # Verificar conexión a base de datos
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    # Leer puerto de variable de entorno (para desarrollo local y Render)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
