"""
Unit tests for config.py
Tests for configuration settings and environment variable handling
"""
import pytest
from unittest.mock import patch
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "codebase"))


class TestConfigDefaults:
    """Tests for default configuration values"""
    
    @patch.dict('os.environ', {}, clear=True)
    def test_debug_default_false(self):
        """Test that DEBUG defaults to False"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DEBUG is False
    
    @patch.dict('os.environ', {}, clear=True)
    def test_secret_key_default(self):
        """Test that SECRET_KEY has a default value"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.SECRET_KEY == "your-secret-key-here"
    
    @patch.dict('os.environ', {}, clear=True)
    def test_vps_host_default(self):
        """Test that VPS_HOST defaults to localhost"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.VPS_HOST == "localhost"
    
    @patch.dict('os.environ', {}, clear=True)
    def test_port_default(self):
        """Test that PORT defaults to 8000"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.PORT == 8000
    
    @patch.dict('os.environ', {}, clear=True)
    def test_database_url_default(self):
        """Test that DATABASE_URL has a default value"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DATABASE_URL == "sqlite:///./data/app.db"
    
    @patch.dict('os.environ', {}, clear=True)
    def test_registry_db_path_default(self):
        """Test that REGISTRY_DB_PATH has a default value"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.REGISTRY_DB_PATH == "data/registry.db"
    
    @patch.dict('os.environ', {}, clear=True)
    def test_upload_folder_default(self):
        """Test that UPLOAD_FOLDER has a default value"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.UPLOAD_FOLDER == "data/uploads"
    
    @patch.dict('os.environ', {}, clear=True)
    def test_max_content_length_default(self):
        """Test that MAX_CONTENT_LENGTH defaults to 16MB"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.MAX_CONTENT_LENGTH == 16777216
    
    @patch.dict('os.environ', {}, clear=True)
    def test_log_level_default(self):
        """Test that LOG_LEVEL defaults to INFO"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.LOG_LEVEL == "INFO"
    
    @patch.dict('os.environ', {}, clear=True)
    def test_log_file_default(self):
        """Test that LOG_FILE has a default value"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.LOG_FILE == "data/app.log"


class TestConfigEnvironmentVariables:
    """Tests for configuration from environment variables"""
    
    @patch.dict('os.environ', {'DEBUG': 'True'})
    def test_debug_from_env_true(self):
        """Test DEBUG set to True from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DEBUG is True
    
    @patch.dict('os.environ', {'DEBUG': 'true'})
    def test_debug_from_env_lowercase_true(self):
        """Test DEBUG with lowercase 'true'"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DEBUG is True
    
    @patch.dict('os.environ', {'DEBUG': 'False'})
    def test_debug_from_env_false(self):
        """Test DEBUG set to False from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DEBUG is False
    
    @patch.dict('os.environ', {'SECRET_KEY': 'custom-secret-key'})
    def test_secret_key_from_env(self):
        """Test SECRET_KEY from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.SECRET_KEY == "custom-secret-key"
    
    @patch.dict('os.environ', {'VPS_HOST': '192.168.1.100'})
    def test_vps_host_from_env(self):
        """Test VPS_HOST from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.VPS_HOST == "192.168.1.100"
    
    @patch.dict('os.environ', {'PORT': '9000'})
    def test_port_from_env(self):
        """Test PORT from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.PORT == 9000
    
    @patch.dict('os.environ', {'DATABASE_URL': 'postgresql://localhost/testdb'})
    def test_database_url_from_env(self):
        """Test DATABASE_URL from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DATABASE_URL == "postgresql://localhost/testdb"
    
    @patch.dict('os.environ', {'UPLOAD_FOLDER': '/var/uploads'})
    def test_upload_folder_from_env(self):
        """Test UPLOAD_FOLDER from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.UPLOAD_FOLDER == "/var/uploads"
    
    @patch.dict('os.environ', {'MAX_CONTENT_LENGTH': '33554432'})
    def test_max_content_length_from_env(self):
        """Test MAX_CONTENT_LENGTH from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.MAX_CONTENT_LENGTH == 33554432
    
    @patch.dict('os.environ', {'LOG_LEVEL': 'DEBUG'})
    def test_log_level_from_env(self):
        """Test LOG_LEVEL from environment"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.LOG_LEVEL == "DEBUG"


class TestConfigEdgeCases:
    """Tests for edge cases and error handling"""
    
    @patch.dict('os.environ', {'DEBUG': 'invalid'})
    def test_debug_invalid_value(self):
        """Test DEBUG with invalid value defaults to False"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DEBUG is False
    
    @patch.dict('os.environ', {'PORT': 'invalid'})
    def test_port_invalid_value(self):
        """Test PORT with invalid value raises error"""
        import importlib
        import config
        
        with pytest.raises(ValueError):
            importlib.reload(config)
    
    @patch.dict('os.environ', {'MAX_CONTENT_LENGTH': 'invalid'})
    def test_max_content_length_invalid_value(self):
        """Test MAX_CONTENT_LENGTH with invalid value raises error"""
        import importlib
        import config
        
        with pytest.raises(ValueError):
            importlib.reload(config)
    
    @patch.dict('os.environ', {'PORT': '0'})
    def test_port_zero(self):
        """Test PORT with zero value"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.PORT == 0
    
    @patch.dict('os.environ', {'PORT': '65535'})
    def test_port_max_value(self):
        """Test PORT with maximum valid value"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.PORT == 65535
    
    @patch.dict('os.environ', {'SECRET_KEY': ''})
    def test_secret_key_empty(self):
        """Test SECRET_KEY with empty string"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.SECRET_KEY == ""
    
    @patch.dict('os.environ', {'DATABASE_URL': ''})
    def test_database_url_empty(self):
        """Test DATABASE_URL with empty string"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.DATABASE_URL == ""


class TestConfigTypeConversions:
    """Tests for type conversions in config"""
    
    @patch.dict('os.environ', {'PORT': '  8080  '})
    def test_port_with_whitespace(self):
        """Test PORT with whitespace is properly converted"""
        import importlib
        import config
        importlib.reload(config)
        
        assert config.PORT == 8080
    
    @patch.dict('os.environ', {'DEBUG': '  True  '})
    def test_debug_with_whitespace(self):
        """Test DEBUG with whitespace"""
        import importlib
        import config
        importlib.reload(config)
        
        # Lower case with strip should work
        assert config.DEBUG is True
    
    @patch.dict('os.environ', {'MAX_CONTENT_LENGTH': '1000000'})
    def test_max_content_length_conversion(self):
        """Test MAX_CONTENT_LENGTH integer conversion"""
        import importlib
        import config
        importlib.reload(config)
        
        assert isinstance(config.MAX_CONTENT_LENGTH, int)
        assert config.MAX_CONTENT_LENGTH == 1000000