"""
Pytest configuration and shared fixtures
"""
import pytest
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Add codebase directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'codebase'))

from utils.db import Base
import config


@pytest.fixture(scope="session")
def test_db_engine():
    """Create a test database engine"""
    # Use in-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Create a test database session"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def test_app():
    """Create a test FastAPI application"""
    from fastapi import FastAPI
    app = FastAPI(title="Test Multi-House Application")
    yield app


@pytest.fixture(scope="function")
def test_client(test_app):
    """Create a test client"""
    from fastapi.testclient import TestClient
    return TestClient(test_app)


@pytest.fixture(scope="function")
def temp_test_dir(tmp_path):
    """Create a temporary directory for testing file operations"""
    test_dir = tmp_path / "test_codebase"
    test_dir.mkdir()
    
    # Create subdirectories
    (test_dir / "modules").mkdir()
    (test_dir / "templates").mkdir()
    (test_dir / "static").mkdir()
    
    # Change to test directory
    original_dir = os.getcwd()
    os.chdir(test_dir)
    
    yield test_dir
    
    # Change back to original directory
    os.chdir(original_dir)


@pytest.fixture
def mock_config(monkeypatch):
    """Mock configuration for testing"""
    monkeypatch.setenv("DEBUG", "True")
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("VPS_HOST", "localhost")
    monkeypatch.setenv("PORT", "8000")