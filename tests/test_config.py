"""
Tests for config.py
"""
import pytest
import os


def test_config_defaults(monkeypatch):
    """Test that config uses default values when env vars are not set"""
    # Clear any existing environment variables
    for key in ['DEBUG', 'SECRET_KEY', 'VPS_HOST', 'PORT', 'DATABASE_URL']:
        monkeypatch.delenv(key, raising=False)
    
    # Reload config module to get fresh values
    import sys
    if 'config' in sys.modules:
        del sys.modules['config']
    
    import config
    
    assert config.DEBUG == False
    assert config.SECRET_KEY == "your-secret-key-here"
    assert config.VPS_HOST == "localhost"
    assert config.PORT == 8000
    assert config.DATABASE_URL == "sqlite:///./data/app.db"


def test_config_from_env_vars(monkeypatch):
    """Test that config reads from environment variables"""
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("SECRET_KEY", "custom-secret")
    monkeypatch.setenv("VPS_HOST", "example.com")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/testdb")
    
    # Reload config module
    import sys
    if 'config' in sys.modules:
        del sys.modules['config']
    
    import config
    
    assert config.DEBUG == True
    assert config.SECRET_KEY == "custom-secret"
    assert config.VPS_HOST == "example.com"
    assert config.PORT == 9000
    assert config.DATABASE_URL == "postgresql://localhost/testdb"


def test_debug_flag_parsing(monkeypatch):
    """Test DEBUG flag parses various string values correctly"""
    test_cases = [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("false", False),
        ("False", False),
        ("FALSE", False),
        ("", False),
        ("random", False),
    ]
    
    for env_value, expected in test_cases:
        monkeypatch.setenv("DEBUG", env_value)
        
        import sys
        if 'config' in sys.modules:
            del sys.modules['config']
        
        import config
        assert config.DEBUG == expected, f"Failed for DEBUG={env_value}"


def test_port_conversion(monkeypatch):
    """Test that PORT is properly converted to integer"""
    monkeypatch.setenv("PORT", "3000")
    
    import sys
    if 'config' in sys.modules:
        del sys.modules['config']
    
    import config
    
    assert isinstance(config.PORT, int)
    assert config.PORT == 3000


def test_max_content_length_conversion(monkeypatch):
    """Test that MAX_CONTENT_LENGTH is properly converted to integer"""
    monkeypatch.setenv("MAX_CONTENT_LENGTH", "8388608")
    
    import sys
    if 'config' in sys.modules:
        del sys.modules['config']
    
    import config
    
    assert isinstance(config.MAX_CONTENT_LENGTH, int)
    assert config.MAX_CONTENT_LENGTH == 8388608


def test_all_config_variables_exist():
    """Test that all expected config variables are defined"""
    import config
    
    required_vars = [
        'DEBUG', 'SECRET_KEY', 'VPS_HOST', 'PORT',
        'DATABASE_URL', 'REGISTRY_DB_PATH', 'APP_DB_PATH',
        'UPLOAD_FOLDER', 'MAX_CONTENT_LENGTH',
        'LOG_LEVEL', 'LOG_FILE'
    ]
    
    for var in required_vars:
        assert hasattr(config, var), f"Config missing required variable: {var}"


def test_database_paths():
    """Test database path configurations"""
    import config
    
    assert config.REGISTRY_DB_PATH == "data/registry.db"
    assert config.APP_DB_PATH == "data/app.db"
    assert "app.db" in config.DATABASE_URL


def test_upload_settings():
    """Test upload-related settings"""
    import config
    
    assert config.UPLOAD_FOLDER == "data/uploads"
    assert config.MAX_CONTENT_LENGTH == 16777216  # 16MB default


def test_logging_settings():
    """Test logging-related settings"""
    import config
    
    assert config.LOG_LEVEL == "INFO"
    assert config.LOG_FILE == "data/app.log"