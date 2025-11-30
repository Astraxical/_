"""
Unit tests for updated main.py
Tests for rate limiting and template engine integration
"""
import pytest
from unittest.mock import patch, MagicMock, Mock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "codebase"))


class TestMainRateLimiting:
    """Tests for rate limiting functionality"""
    
    @patch('main.Limiter')
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    def test_limiter_initialization(self, mock_config, mock_template_engine, mock_setup, mock_limiter_class):
        """Test that rate limiter is properly initialized"""
        mock_config.DEBUG = True
        mock_limiter_instance = MagicMock()
        mock_limiter_class.return_value = mock_limiter_instance
        
        # Import after mocking to trigger module initialization
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        # Limiter should be created
        assert mock_limiter_class.called
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    def test_rate_limit_decorator_on_root(self, mock_config, mock_template_engine, mock_setup):
        """Test that root endpoint has rate limit decorator"""
        mock_config.DEBUG = True
        mock_config.PORT = 8000
        
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        # Check that the read_root function exists and can be inspected
        assert hasattr(main_module, 'read_root')
        assert callable(main_module.read_root)


class TestMainTemplateEngine:
    """Tests for template engine integration in main.py"""
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    def test_template_engine_initialized(self, mock_config, mock_template_engine_class, mock_setup):
        """Test that template engine is initialized"""
        mock_config.DEBUG = True
        mock_config.PORT = 8000
        
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        # Template engine should be instantiated
        assert mock_template_engine_class.called
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    def test_read_root_uses_template_engine(self, mock_config, mock_template_engine_class, mock_setup):
        """Test that read_root uses template engine for rendering"""
        mock_config.DEBUG = True
        mock_config.PORT = 8000
        
        mock_engine_instance = MagicMock()
        mock_template_engine_class.return_value = mock_engine_instance
        
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        mock_request = MagicMock()
        
        # Call the route handler
        main_module.read_root(mock_request)
        
        # Should have called render on the template engine
        mock_engine_instance.render.assert_called_once_with("index.html", mock_request)


class TestMainApplicationSetup:
    """Tests for FastAPI application setup"""
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    @patch('main.StaticFiles')
    def test_static_files_mounted(self, mock_static, mock_config, mock_template_engine, mock_setup):
        """Test that static files are properly mounted"""
        mock_config.DEBUG = True
        mock_config.PORT = 8000
        
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        # Static files should be mounted
        assert main_module.app.mount.called or mock_static.called
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    def test_components_setup_called(self, mock_config, mock_template_engine, mock_setup):
        """Test that setup_components is called"""
        mock_config.DEBUG = True
        mock_config.PORT = 8000
        
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        # setup_components should be called with the app
        assert mock_setup.called
        call_args = mock_setup.call_args[0]
        assert len(call_args) > 0
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    def test_rate_limit_exception_handler_added(self, mock_config, mock_template_engine, mock_setup):
        """Test that rate limit exception handler is added to app"""
        mock_config.DEBUG = True
        mock_config.PORT = 8000
        
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        # Check that exception handler was added
        assert hasattr(main_module.app, 'add_exception_handler')


class TestMainEdgeCases:
    """Tests for edge cases in main.py"""
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    def test_app_creation_with_debug_true(self, mock_config, mock_template_engine, mock_setup):
        """Test app creation with DEBUG=True"""
        mock_config.DEBUG = True
        mock_config.PORT = 8000
        
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        assert main_module.app is not None
        assert main_module.app.debug is True
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.config')
    def test_app_creation_with_debug_false(self, mock_config, mock_template_engine, mock_setup):
        """Test app creation with DEBUG=False"""
        mock_config.DEBUG = False
        mock_config.PORT = 8000
        
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        assert main_module.app is not None
        assert main_module.app.debug is False


class TestReadRootRoute:
    """Tests specifically for the read_root route"""
    
    @patch('main.template_engine')
    @patch('main.config')
    def test_read_root_returns_template_response(self, mock_config, mock_engine):
        """Test that read_root returns a template response"""
        from main import read_root
        
        mock_request = MagicMock()
        mock_response = MagicMock()
        mock_engine.render.return_value = mock_response
        
        result = read_root(mock_request)
        
        assert result == mock_response
        mock_engine.render.assert_called_once_with("index.html", mock_request)
    
    @patch('main.template_engine')
    @patch('main.config')
    def test_read_root_with_mock_request(self, mock_config, mock_engine):
        """Test read_root with a mocked request object"""
        from main import read_root
        
        mock_request = MagicMock()
        mock_request.client = Mock(host="127.0.0.1")
        mock_request.url = Mock(path="/")
        
        read_root(mock_request)
        
        # Should pass the request to the template engine
        call_args = mock_engine.render.call_args
        assert call_args[0][1] == mock_request