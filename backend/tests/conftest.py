"""Pytest configuration and fixtures"""
import os
import sys
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.base import Base
from app.database.session import get_db
from app.main import app
from app.models.lead import Lead, LeadStatus


# Test database URL (in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> TestClient:
    """Create a test client with database override."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_lead(db_session: Session) -> Lead:
    """Create a sample lead for testing."""
    lead = Lead(
        phone="+1234567890",
        name="Test User",
        interest="Testing the product",
        status=LeadStatus.NEW,
    )
    db_session.add(lead)
    db_session.commit()
    db_session.refresh(lead)
    return lead


@pytest.fixture
def engaged_lead(db_session: Session) -> Lead:
    """Create an engaged lead for testing."""
    lead = Lead(
        phone="+1987654321",
        name="Engaged User",
        interest="Very interested in buying",
        status=LeadStatus.ENGAGED,
        last_message="Tell me more about pricing",
    )
    db_session.add(lead)
    db_session.commit()
    db_session.refresh(lead)
    return lead