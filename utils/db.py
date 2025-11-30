"""
Database models and initialization
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import config

# Database setup
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ModuleRegistry(Base):
    """
    Tracks module status in the system
    """
    __tablename__ = "registry"
    
    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, unique=True, index=True)
    enabled = Column(Boolean, default=True)
    route_prefix = Column(String)
    local_data_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Alter(Base):
    """
    Represents an alter in the system
    """
    __tablename__ = "alters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_fronting = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    bio = Column(Text)
    style = Column(String)

class AuditLog(Base):
    """
    Audit log for admin actions
    """
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    user = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(Text)

# Create all tables
def init_db():
    Base.metadata.create_all(bind=engine)