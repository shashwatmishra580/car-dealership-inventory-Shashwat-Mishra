"""SQLAlchemy engine/session setup."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def make_engine(url: str):
    """Create an engine; SQLite needs check_same_thread off for FastAPI's threadpool."""
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=connect_args)


engine = make_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db():
    """FastAPI dependency yielding one DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
