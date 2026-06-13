"""
Database connection helpers for SQLAlchemy with psycopg2-binary (Windows compatible).

Currently uses in-memory storage for sessions/messages in local dev.
Migrate to actual DB by:
1. Creating Alembic migrations
2. Switching from in-memory dicts to DB queries in models.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

# Create SQLAlchemy engine with psycopg2 driver
# psycopg2-binary is Windows-compatible and doesn't require compilation
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_size=5,
    max_overflow=10,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for FastAPI to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)


# Example: How to use in a route
# from sqlalchemy.orm import Session
# from fastapi import Depends
# from app.db import get_db
#
# @app.get("/users")
# async def list_users(db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users
