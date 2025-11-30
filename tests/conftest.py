"""
Pytest configuration and shared fixtures
"""
import pytest
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent / "codebase"))

from utils.db import Base


@pytest.fixture(scope="session")
def test_db_engine():
    """Create a test database engine"""
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Create a new database session for a test"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def clean_environment(monkeypatch):
    """Clean environment variables for testing"""
    # Set test environment variables
    monkeypatch.setenv("DEBUG", "False")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-for-testing")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("VPS_HOST", "localhost")
    monkeypatch.setenv("PORT", "8000")
    yield


@pytest.fixture
def mock_fastapi_app():
    """Create a mock FastAPI app for testing"""
    from fastapi import FastAPI
    app = FastAPI()
    return app


@pytest.fixture
def test_client(mock_fastapi_app):
    """Create a test client for the FastAPI app"""
    from fastapi.testclient import TestClient
    return TestClient(mock_fastapi_app)