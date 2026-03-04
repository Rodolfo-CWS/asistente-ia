from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, nullable=False)
    name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    goals = relationship("Goal", back_populates="user")
    progress_logs = relationship("ProgressLog", back_populates="user")

class Goal(Base):
    __tablename__ = 'goals'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Tipo de objetivo: 'fitness', 'learning', 'productivity'
    goal_type = Column(String(20), nullable=False)
    
    # Metadata común
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default='active')  # active, completed, paused
    created_at = Column(DateTime, default=datetime.utcnow)
    target_date = Column(DateTime)
    
    # Datos específicos del tipo de objetivo (JSON flexible)
    goal_data = Column(JSON)
    
    # Relaciones
    user = relationship("User", back_populates="goals")
    progress_logs = relationship("ProgressLog", back_populates="goal")
    
class ProgressLog(Base):
    __tablename__ = 'progress_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_id = Column(Integer, ForeignKey('goals.id'), nullable=False)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    log_type = Column(String(50))  # weight_update, workout_completed, study_session, etc.
    
    # Datos del progreso (JSON flexible)
    log_data = Column(JSON)
    
    # Relaciones
    user = relationship("User", back_populates="progress_logs")
    goal = relationship("Goal", back_populates="progress_logs")

class Diet(Base):
    """Para almacenar dietas del usuario"""
    __tablename__ = 'diets'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    goal_id = Column(Integer, ForeignKey('goals.id'))
    
    name = Column(String(100))
    description = Column(Text)
    diet_data = Column(JSON)  # Comidas, calorías, macros, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
