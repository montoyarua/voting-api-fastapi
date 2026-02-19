"""
Punto de entrada (FastAPI).

- Incluye routers
- Crea tablas al iniciar (rápido para prueba técnica)
  Para producción: usar migraciones (Alembic).
"""
from fastapi import FastAPI

from app.core.config import settings
from app.db.session import engine, Base
from app.api.routers import voters_router, candidates_router, votes_router

# Importa modelos para registrarlos antes de create_all
from app import models  # noqa: F401


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="API RESTful de votaciones (FastAPI + SQLAlchemy + MySQL local).",
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(voters_router)
    app.include_router(candidates_router)
    app.include_router(votes_router)

    return app


app = create_app()
