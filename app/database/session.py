from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 👉 DB URL change pannalaam later (Postgres / MySQL)
DATABASE_URL = "sqlite:///./intrusion.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed only for SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
