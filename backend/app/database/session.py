"""Database session and engine configuration"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create engine based on database URL
if settings.database_url.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
        echo=settings.debug,
    )
    logger.info("Using SQLite database")
else:
    # PostgreSQL or other databases
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
    )
    logger.info("Using PostgreSQL database")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()