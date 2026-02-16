from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database.models import IntrusionLog
from .models import Base

DATABASE_URL = "sqlite:///./app/database/db.sqlite3"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = Session(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    Base.metadata.create_all(bind=engine)

# 🔥 NEW: Dependency function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_intrusion_log(db: Session, data: dict):
    log = IntrusionLog(**data)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
