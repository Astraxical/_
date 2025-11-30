"""
Unit tests for config.py
"""
import pytest
import os


class TestConfig:
    """Test configuration settings"""
    
    def test_debug_default_false(self, clean_environment, monkeypatch):
        """Test DEBUG defaults to False"""
        monkeypatch.delenv("DEBUG", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.DEBUG is False
    
    def test_debug_true_when_set(self, clean_environment, monkeypatch):
        """Test DEBUG is True when environment variable is 'true'"""
        monkeypatch.setenv("DEBUG", "true")
        import importlib
        import config
        importlib.reload(config)
        assert config.DEBUG is True
    
    def test_debug_false_when_set_to_false(self, clean_environment, monkeypatch):
        """Test DEBUG is False when environment variable is 'false'"""
        monkeypatch.setenv("DEBUG", "false")
        import importlib
        import config
        importlib.reload(config)
        assert config.DEBUG is False
    
    def test_debug_case_insensitive(self, clean_environment, monkeypatch):
        """Test DEBUG environment variable is case insensitive"""
        monkeypatch.setenv("DEBUG", "TRUE")
        import importlib
        import config
        importlib.reload(config)
        assert config.DEBUG is True
    
    def test_secret_key_default(self, clean_environment, monkeypatch):
        """Test SECRET_KEY has a default value"""
        monkeypatch.delenv("SECRET_KEY", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.SECRET_KEY == "your-secret-key-here"
    
    def test_secret_key_from_env(self, clean_environment, monkeypatch):
        """Test SECRET_KEY can be set from environment"""
        test_key = "custom-secret-key-123"
        monkeypatch.setenv("SECRET_KEY", test_key)
        import importlib
        import config
        importlib.reload(config)
        assert config.SECRET_KEY == test_key
    
    def test_vps_host_default(self, clean_environment, monkeypatch):
        """Test VPS_HOST defaults to localhost"""
        monkeypatch.delenv("VPS_HOST", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.VPS_HOST == "localhost"
    
    def test_vps_host_from_env(self, clean_environment, monkeypatch):
        """Test VPS_HOST can be set from environment"""
        test_host = "example.com"
        monkeypatch.setenv("VPS_HOST", test_host)
        import importlib
        import config
        importlib.reload(config)
        assert config.VPS_HOST == test_host
    
    def test_port_default(self, clean_environment, monkeypatch):
        """Test PORT defaults to 8000"""
        monkeypatch.delenv("PORT", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.PORT == 8000
    
    def test_port_from_env(self, clean_environment, monkeypatch):
        """Test PORT can be set from environment as integer"""
        monkeypatch.setenv("PORT", "3000")
        import importlib
        import config
        importlib.reload(config)
        assert config.PORT == 3000
        assert isinstance(config.PORT, int)
    
    def test_database_url_default(self, clean_environment, monkeypatch):
        """Test DATABASE_URL has correct default path"""
        monkeypatch.delenv("DATABASE_URL", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.DATABASE_URL == "sqlite:///./data/app.db"
    
    def test_database_url_from_env(self, clean_environment, monkeypatch):
        """Test DATABASE_URL can be set from environment"""
        test_url = "postgresql://user:pass@localhost/dbname"
        monkeypatch.setenv("DATABASE_URL", test_url)
        import importlib
        import config
        importlib.reload(config)
        assert config.DATABASE_URL == test_url
    
    def test_registry_db_path_default(self, clean_environment, monkeypatch):
        """Test REGISTRY_DB_PATH has correct default"""
        monkeypatch.delenv("REGISTRY_DB_PATH", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.REGISTRY_DB_PATH == "data/registry.db"
    
    def test_app_db_path_default(self, clean_environment, monkeypatch):
        """Test APP_DB_PATH has correct default"""
        monkeypatch.delenv("APP_DB_PATH", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.APP_DB_PATH == "data/app.db"
    
    def test_upload_folder_default(self, clean_environment, monkeypatch):
        """Test UPLOAD_FOLDER has correct default"""
        monkeypatch.delenv("UPLOAD_FOLDER", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.UPLOAD_FOLDER == "data/uploads"
    
    def test_max_content_length_default(self, clean_environment, monkeypatch):
        """Test MAX_CONTENT_LENGTH defaults to 16MB"""
        monkeypatch.delenv("MAX_CONTENT_LENGTH", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.MAX_CONTENT_LENGTH == 16777216  # 16MB in bytes
    
    def test_max_content_length_from_env(self, clean_environment, monkeypatch):
        """Test MAX_CONTENT_LENGTH can be set from environment"""
        monkeypatch.setenv("MAX_CONTENT_LENGTH", "8388608")  # 8MB
        import importlib
        import config
        importlib.reload(config)
        assert config.MAX_CONTENT_LENGTH == 8388608
        assert isinstance(config.MAX_CONTENT_LENGTH, int)
    
    def test_log_level_default(self, clean_environment, monkeypatch):
        """Test LOG_LEVEL defaults to INFO"""
        monkeypatch.delenv("LOG_LEVEL", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.LOG_LEVEL == "INFO"
    
    def test_log_level_from_env(self, clean_environment, monkeypatch):
        """Test LOG_LEVEL can be set from environment"""
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        import importlib
        import config
        importlib.reload(config)
        assert config.LOG_LEVEL == "DEBUG"
    
    def test_log_file_default(self, clean_environment, monkeypatch):
        """Test LOG_FILE has correct default path"""
        monkeypatch.delenv("LOG_FILE", raising=False)
        import importlib
        import config
        importlib.reload(config)
        assert config.LOG_FILE == "data/app.log"
    
    def test_log_file_from_env(self, clean_environment, monkeypatch):
        """Test LOG_FILE can be set from environment"""
        test_path = "/var/log/app.log"
        monkeypatch.setenv("LOG_FILE", test_path)
        import importlib
        import config
        importlib.reload(config)
        assert config.LOG_FILE == test_path
    
    def test_all_config_values_accessible(self, clean_environment):
        """Test that all expected config values are accessible"""
        import config
        import importlib
        importlib.reload(config)
        
        # Check all expected attributes exist
        assert hasattr(config, 'DEBUG')
        assert hasattr(config, 'SECRET_KEY')
        assert hasattr(config, 'VPS_HOST')
        assert hasattr(config, 'PORT')
        assert hasattr(config, 'DATABASE_URL')
        assert hasattr(config, 'REGISTRY_DB_PATH')
        assert hasattr(config, 'APP_DB_PATH')
        assert hasattr(config, 'UPLOAD_FOLDER')
        assert hasattr(config, 'MAX_CONTENT_LENGTH')
        assert hasattr(config, 'LOG_LEVEL')
        assert hasattr(config, 'LOG_FILE')