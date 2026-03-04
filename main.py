from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import anthropic
from datetime import datetime, timedelta
from typing import List, Dict, Any

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
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
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

# ==========================================
# REST API ENDPOINTS FOR DASHBOARD
# ==========================================

@app.get("/api/users/{phone}")
def get_user_by_phone(phone: str):
    """Get user information by phone number"""
    db = SessionLocal()
    try:
        # Normalize phone format (remove spaces, dashes, etc.)
        phone_clean = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

        # Try with and without country code
        user = db.query(User).filter(
            (User.phone_number == phone_clean) |
            (User.phone_number == f"+{phone_clean}") |
            (User.phone_number == phone)
        ).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "phone_number": user.phone_number,
            "name": user.name,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    finally:
        db.close()

@app.get("/api/users/{user_id}/goals")
def get_user_goals(user_id: int):
    """Get all goals for a specific user"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        goals = db.query(Goal).filter(Goal.user_id == user_id).all()

        return {
            "user_id": user_id,
            "total_goals": len(goals),
            "goals": [
                {
                    "id": goal.id,
                    "goal_type": goal.goal_type,
                    "title": goal.title,
                    "description": goal.description,
                    "status": goal.status,
                    "created_at": goal.created_at.isoformat() if goal.created_at else None,
                    "target_date": goal.target_date.isoformat() if goal.target_date else None,
                    "goal_data": goal.goal_data or {}
                }
                for goal in goals
            ]
        }
    finally:
        db.close()

@app.get("/api/goals/{goal_id}/progress")
def get_goal_progress(goal_id: int):
    """Get detailed progress information for a specific goal"""
    db = SessionLocal()
    try:
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        # Get all progress logs for this goal
        logs = db.query(ProgressLog).filter(
            ProgressLog.goal_id == goal_id
        ).order_by(ProgressLog.timestamp.desc()).all()

        # Calculate progress metrics based on goal type
        progress_data: Dict[str, Any] = {
            "goal_id": goal_id,
            "goal_type": goal.goal_type,
            "title": goal.title,
            "status": goal.status,
            "total_logs": len(logs),
            "goal_data": goal.goal_data or {}
        }

        # Add goal-specific data from goal_data JSON
        if goal.goal_data:
            if goal.goal_type == "fitness":
                start_weight = goal.goal_data.get('current_weight', 0)
                target_weight = goal.goal_data.get('target_weight', 0)

                # Get most recent weight from logs
                current_weight = start_weight
                for log in logs:
                    if log.log_data and 'weight' in log.log_data:
                        current_weight = log.log_data['weight']
                        break

                progress_data["start_weight"] = start_weight
                progress_data["target_weight"] = target_weight
                progress_data["current_weight"] = current_weight
                progress_data["weight_change"] = current_weight - start_weight
                progress_data["target_change"] = target_weight - start_weight

                if progress_data["target_change"] != 0:
                    progress_data["progress_percentage"] = round(
                        (progress_data["weight_change"] / progress_data["target_change"]) * 100, 1
                    )
                else:
                    progress_data["progress_percentage"] = 0

            elif goal.goal_type == "learning":
                total_hours = 0
                for log in logs:
                    if log.log_data and 'study_hours' in log.log_data:
                        total_hours += log.log_data['study_hours']

                progress_data["total_study_hours"] = total_hours
                progress_data["target_hours_per_day"] = goal.goal_data.get('study_time_per_day', 0)

            elif goal.goal_type == "productivity":
                total_practice_hours = 0
                completed_tasks = 0
                for log in logs:
                    if log.log_data:
                        if 'practice_hours' in log.log_data:
                            total_practice_hours += log.log_data['practice_hours']
                        if log.log_data.get('task_completed'):
                            completed_tasks += 1

                progress_data["total_practice_hours"] = total_practice_hours
                progress_data["completed_tasks"] = completed_tasks

        return progress_data
    finally:
        db.close()

@app.get("/api/goals/{goal_id}/logs")
def get_goal_logs(goal_id: int, limit: int = 50):
    """Get history logs for a specific goal"""
    db = SessionLocal()
    try:
        goal = db.query(Goal).filter(Goal.id == goal_id).first()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        logs = db.query(ProgressLog).filter(
            ProgressLog.goal_id == goal_id
        ).order_by(ProgressLog.timestamp.desc()).limit(limit).all()

        return {
            "goal_id": goal_id,
            "goal_type": goal.goal_type,
            "total_logs": len(logs),
            "logs": [
                {
                    "id": log.id,
                    "timestamp": log.timestamp.isoformat() if log.timestamp else None,
                    "log_type": log.log_type,
                    "log_data": log.log_data or {}
                }
                for log in logs
            ]
        }
    finally:
        db.close()

@app.get("/api/users/{user_id}/stats")
def get_user_stats(user_id: int):
    """Get general statistics for a user"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get all goals
        goals = db.query(Goal).filter(Goal.user_id == user_id).all()

        # Count goals by status
        active_goals = sum(1 for g in goals if g.status == "active")
        completed_goals = sum(1 for g in goals if g.status == "completed")
        paused_goals = sum(1 for g in goals if g.status == "paused")

        # Get all progress logs
        goal_ids = [g.id for g in goals]
        if goal_ids:
            logs = db.query(ProgressLog).filter(
                ProgressLog.goal_id.in_(goal_ids)
            ).all()
        else:
            logs = []

        # Calculate streak (consecutive days with logs)
        streak = 0
        if logs:
            logs_sorted = sorted(logs, key=lambda x: x.timestamp, reverse=True)
            current_date = datetime.now().date()

            for log in logs_sorted:
                log_date = log.timestamp.date()
                if (current_date - log_date).days <= streak + 1:
                    if (current_date - log_date).days == streak:
                        streak += 1
                        current_date = log_date
                else:
                    break

        # Last activity
        last_log = max(logs, key=lambda x: x.timestamp) if logs else None

        return {
            "user_id": user_id,
            "total_goals": len(goals),
            "active_goals": active_goals,
            "completed_goals": completed_goals,
            "paused_goals": paused_goals,
            "total_logs": len(logs),
            "current_streak": streak,
            "last_activity": last_log.timestamp.isoformat() if last_log else None,
            "member_since": user.created_at.isoformat() if user.created_at else None
        }
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    # Leer puerto de variable de entorno (para desarrollo local y Render)
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
