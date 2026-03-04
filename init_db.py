#!/usr/bin/env python3
"""
Script para inicializar la base de datos PostgreSQL
Crea todas las tablas necesarias basadas en los modelos de SQLAlchemy
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from models import Base

# Cargar variables de entorno
load_dotenv()

def init_database():
    """Inicializa la base de datos creando todas las tablas"""

    # Obtener DATABASE_URL
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("ERROR: DATABASE_URL no está configurada en las variables de entorno")
        return False

    # Render PostgreSQL usa 'postgres://' pero SQLAlchemy 1.4+ requiere 'postgresql://'
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        print("INFO: Convertido postgres:// a postgresql://")

    try:
        # Crear engine
        engine = create_engine(database_url)

        # Verificar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"Conectado a PostgreSQL: {version}")

        # Crear todas las tablas
        print("\nCreando tablas...")
        Base.metadata.create_all(bind=engine)

        # Verificar tablas creadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"\nTablas creadas exitosamente:")
        for table in tables:
            print(f"  - {table}")

        print(f"\nTotal: {len(tables)} tablas")
        print("\n✓ Base de datos inicializada correctamente!")
        return True

    except Exception as e:
        print(f"\nERROR al inicializar la base de datos:")
        print(f"  {type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Inicializador de Base de Datos")
    print("Asistente IA Personal")
    print("=" * 50)
    print()

    success = init_database()

    if success:
        exit(0)
    else:
        exit(1)
