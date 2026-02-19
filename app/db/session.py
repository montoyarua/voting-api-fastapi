"""
Capa DB (SQLAlchemy 2.0):
- Engine (MySQL)
- SessionLocal
- Base declarativa
- Dependency get_db() para FastAPI
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Base declarativa para modelos SQLAlchemy."""
    pass


engine = create_engine(
    settings.database_url,
    echo=False,
    future=True,
    pool_pre_ping=True,  # Evita conexiones muertas
    pool_recycle=3600,   # Reduce problemas de timeout
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db():
    """Entrega una sesión por request y la cierra al finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
