"""
Pytest configuration and shared fixtures
"""
import pytest
import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add codebase directory to Python path
codebase_path = Path(__file__).parent.parent / "codebase"
sys.path.insert(0, str(codebase_path))

@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    with patch('config.DEBUG', True), \
         patch('config.SECRET_KEY', 'test-secret-key'), \
         patch('config.DATABASE_URL', 'sqlite:///:memory:'), \
         patch('config.VPS_HOST', 'localhost'), \
         patch('config.PORT', 8000):
        yield

@pytest.fixture
def temp_test_dir(tmp_path):
    """Create a temporary directory for testing file operations"""
    test_dir = tmp_path / "test_files"
    test_dir.mkdir()
    
    # Create mock directory structure
    (test_dir / "modules").mkdir()
    (test_dir / "modules" / "forums").mkdir()
    (test_dir / "modules" / "forums" / "templates").mkdir()
    (test_dir / "templates").mkdir()
    (test_dir / "static").mkdir()
    
    return test_dir

@pytest.fixture
def mock_db_session():
    """Mock database session for testing"""
    session = MagicMock()
    session.query.return_value = session
    session.filter.return_value = session
    session.first.return_value = None
    session.all.return_value = []
    return session

@pytest.fixture
def mock_fastapi_app():
    """Mock FastAPI application for testing"""
    from fastapi import FastAPI
    app = FastAPI()
    return app