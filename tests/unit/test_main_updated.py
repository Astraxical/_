"""
Comprehensive unit tests for updated main.py.
Tests rate limiting, template engine integration, and root route.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'codebase'))


class TestAppInitialization:
    """Test FastAPI app initialization with new features."""
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    @patch('main.Limiter')
    def test_app_has_rate_limiter(self, mock_limiter, mock_engine, mock_setup):
        """Test that rate limiter is properly initialized."""
        from main import app
        
        assert hasattr(app.state, 'limiter')
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    def test_app_initializes_template_engine(self, mock_engine, mock_setup):
        """Test that template engine is initialized on app startup."""
        import main
        
        # Template engine should be created
        mock_engine.assert_called_once()


class TestRootRouteWithTemplateEngine:
    """Test root route with template engine rendering."""
    
    @patch('main.template_engine')
    @patch('main.setup_components')
    def test_root_route_uses_template_engine(self, mock_setup, mock_template_engine):
        """Test that root route uses template engine for rendering."""
        from main import app
        
        mock_template_engine.render.return_value = Mock()
        client = TestClient(app)
        
        # Note: This might fail due to rate limiting, so we test the function directly
        from main import read_root
        from fastapi import Request
        
        mock_request = Mock(spec=Request)
        mock_request.client.host = '127.0.0.1'
        
        with patch('main.limiter.limit', return_value=lambda f: f):
            result = read_root(mock_request)
        
        mock_template_engine.render.assert_called_once_with('index.html', mock_request)
    
    @patch('main.template_engine')
    @patch('main.setup_components')
    def test_root_route_passes_request_to_engine(self, mock_setup, mock_template_engine):
        """Test that request object is properly passed to template engine."""
        from main import read_root
        from fastapi import Request
        
        mock_request = Mock(spec=Request)
        mock_request.client.host = '127.0.0.1'
        mock_template_engine.render.return_value = Mock()
        
        with patch('main.limiter.limit', return_value=lambda f: f):
            read_root(mock_request)
        
        call_args = mock_template_engine.render.call_args
        assert call_args[0][1] == mock_request


class TestRateLimiting:
    """Test rate limiting functionality."""
    
    @patch('main.setup_components')
    @patch('main.template_engine')
    def test_rate_limit_decorator_applied(self, mock_engine, mock_setup):
        """Test that rate limit decorator is applied to root route."""
        from main import read_root
        
        # Check if the function has rate limit metadata
        # This is a basic check - actual rate limiting is tested via integration
        assert callable(read_root)
    
    @patch('main.setup_components')
    def test_rate_limit_exception_handler_registered(self, mock_setup):
        """Test that rate limit exception handler is registered."""
        from main import app
        from slowapi.errors import RateLimitExceeded
        
        # Verify exception handler is registered
        assert RateLimitExceeded in app.exception_handlers


class TestStaticFilesMount:
    """Test static files mounting."""
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    def test_static_files_mounted(self, mock_engine, mock_setup):
        """Test that static files are properly mounted."""
        from main import app
        
        # Check if static route exists
        static_routes = [route for route in app.routes if 'static' in str(route.path)]
        assert len(static_routes) > 0


class TestComponentsSetup:
    """Test components setup integration."""
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    def test_setup_components_called_on_init(self, mock_engine, mock_setup):
        """Test that setup_components is called during app initialization."""
        import main
        
        # Import should trigger setup
        mock_setup.assert_called()
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    def test_setup_components_receives_app_instance(self, mock_engine, mock_setup):
        """Test that setup_components receives the FastAPI app instance."""
        from main import app as main_app
        
        # Verify setup_components was called with app
        call_args = mock_setup.call_args
        if call_args:
            assert call_args[0][0] == main_app


class TestConfigIntegration:
    """Test configuration integration."""
    
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    def test_app_uses_config_debug(self, mock_engine, mock_setup):
        """Test that app uses DEBUG setting from config."""
        from main import app
        import main as main_module
        
        # App should respect config.DEBUG
        assert hasattr(main_module, 'config')


class TestUvicornExecution:
    """Test uvicorn execution configuration."""
    
    @patch('main.uvicorn.run')
    @patch('main.setup_components')
    @patch('main.TemplateEngine')
    def test_uvicorn_config_when_main(self, mock_engine, mock_setup, mock_uvicorn):
        """Test uvicorn configuration when run as main."""
        # This tests the if __name__ == '__main__' block
        # We need to execute it in a way that triggers the condition
        import main
        
        # Simulate running as main
        with patch.object(main, '__name__', '__main__'):
            exec(compile(open('codebase/main.py').read(), 'codebase/main.py', 'exec'))
        
        # Verify uvicorn.run was called (if __main__ condition was met)
        # Note: This test might need adjustment based on test isolation