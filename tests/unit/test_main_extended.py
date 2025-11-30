"""
Extended unit tests for main.py focusing on new functionality
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, 'codebase')


class TestMainWithRateLimiting:
    """Tests for rate limiting functionality"""
    
    def test_app_has_rate_limiter_state(self):
        """Test that app has limiter in state"""
        from main import app
        assert hasattr(app.state, 'limiter')
    
    @patch('main.template_engine')
    def test_root_endpoint_with_rate_limit(self, mock_engine):
        """Test root endpoint respects rate limiting"""
        from main import app
        
        mock_engine.render.return_value = {"message": "test"}
        
        client = TestClient(app)
        
        # First request should succeed
        response = client.get("/")
        assert response.status_code == 200
    
    @patch('main.template_engine')
    def test_root_endpoint_calls_template_engine(self, mock_engine):
        """Test that root endpoint uses template engine"""
        from main import app
        
        mock_engine.render.return_value = {"message": "test"}
        
        client = TestClient(app)
        response = client.get("/")
        
        # Verify template_engine.render was called
        assert mock_engine.render.called
        call_args = mock_engine.render.call_args[0]
        assert call_args[0] == "index.html"
    
    def test_app_includes_rate_limit_exception_handler(self):
        """Test that app has rate limit exception handler"""
        from main import app
        from slowapi.errors import RateLimitExceeded
        
        # Check that exception handler is registered
        assert RateLimitExceeded in app.exception_handlers


class TestMainComponentSetup:
    """Tests for component setup in main"""
    
    @patch('main.setup_components')
    def test_setup_components_called_on_import(self, mock_setup):
        """Test that setup_components is called when main is imported"""
        # Re-import to trigger setup
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        # setup_components should have been called
        assert mock_setup.called
    
    def test_app_has_static_files_mounted(self):
        """Test that static files are mounted"""
        from main import app
        
        # Check that static files route exists
        routes = [route.path for route in app.routes]
        assert any('/static' in route for route in routes)


class TestMainTemplateEngine:
    """Tests for template engine integration in main"""
    
    @patch('main.TemplateEngine')
    def test_template_engine_initialized(self, mock_engine_class):
        """Test that template engine is initialized"""
        import importlib
        import main as main_module
        importlib.reload(main_module)
        
        assert mock_engine_class.called
    
    @patch('main.template_engine')
    def test_read_root_passes_request_to_engine(self, mock_engine):
        """Test that read_root passes request object to template engine"""
        from main import read_root
        
        mock_request = Mock(spec=Request)
        mock_engine.render.return_value = "response"
        
        read_root(mock_request)
        
        call_args = mock_engine.render.call_args[0]
        assert call_args[1] == mock_request


class TestMainConfiguration:
    """Tests for main app configuration"""
    
    def test_app_title(self):
        """Test that app has correct title"""
        from main import app
        assert app.title == "Multi-House Application"
    
    def test_app_debug_from_config(self):
        """Test that app debug setting comes from config"""
        from main import app
        import config
        assert app.debug == config.DEBUG
    
    def test_limiter_uses_remote_address(self):
        """Test that limiter is configured with get_remote_address"""
        from main import limiter
        from slowapi.util import get_remote_address
        
        assert limiter._key_func == get_remote_address


class TestReadRootEndpoint:
    """Tests for read_root endpoint function"""
    
    @patch('main.template_engine')
    def test_read_root_returns_template_response(self, mock_engine):
        """Test that read_root returns template engine response"""
        from main import read_root
        
        mock_request = Mock(spec=Request)
        expected_response = "template_response"
        mock_engine.render.return_value = expected_response
        
        result = read_root(mock_request)
        
        assert result == expected_response
    
    @patch('main.template_engine')
    def test_read_root_with_different_requests(self, mock_engine):
        """Test read_root with various request objects"""
        from main import read_root
        
        mock_engine.render.return_value = "response"
        
        for i in range(3):
            mock_request = Mock(spec=Request)
            mock_request.client = Mock()
            mock_request.client.host = f"192.168.1.{i}"
            
            result = read_root(mock_request)
            assert result == "response"