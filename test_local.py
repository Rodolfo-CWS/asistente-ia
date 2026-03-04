#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar el bot localmente sin WhatsApp
Simula una conversación completa
"""

import os
import sys

# Configurar la salida para manejar UTF-8
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importar después de cargar .env
load_dotenv()

# Solo importar si está configurado
if not os.getenv("ANTHROPIC_API_KEY"):
    print("WARNING: ANTHROPIC_API_KEY no configurada en .env")
    print("Usando modo simulado...")
    claude_client = None
else:
    import anthropic
    claude_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

from models import Base, User
from whatsapp_handler import GoalConversationHandler

# DB en memoria para testing
engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

def test_conversation():
    """Simula conversación completa de creación de objetivo"""

    db = SessionLocal()

    # Buscar o crear usuario de prueba
    user = db.query(User).filter(User.phone_number == "+1234567890").first()
    if not user:
        user = User(phone_number="+1234567890", name="Test User")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Handler
    handler = GoalConversationHandler(db, claude_client)
    
    # Conversación simulada
    messages = [
        "Hola",
        "Quiero bajar de peso",
        "80",  # peso actual
        "75",  # peso objetivo
        "175", # altura
        "30",  # edad
        "H",   # género
        "2 meses" # cuando
    ]
    
    print("[BOT] Simulando conversacion de WhatsApp\n")
    print("=" * 50)

    for msg in messages:
        print(f"\n[Usuario]: {msg}")

        response = handler.handle_message(user.id, user.phone_number, msg)

        print(f"[Bot]: {response}")
        print("-" * 50)

    # Probar registro de progreso
    print("\n\n[TEST] Probando registro de progreso...")
    print("=" * 50)

    progress_msg = "Hoy pese 79kg"
    print(f"\n[Usuario]: {progress_msg}")
    response = handler.handle_message(user.id, user.phone_number, progress_msg)
    print(f"[Bot]: {response}")

    db.close()

    print("\n\n[OK] Test completado!")
    print(f"Base de datos de prueba: test.db")

if __name__ == "__main__":
    print("""
==========================================
  Test Local - Asistente IA Personal
==========================================
    """)
    
    test_conversation()
