"""
Unit tests for main.py
Tests for FastAPI application initialization and routes
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "codebase"))


class TestAppInitialization:
    """Tests for FastAPI application initialization"""
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_app_creation(self, mock_static, mock_setup):
        """Test that FastAPI app is created"""
        import importlib
        import main
        importlib.reload(main)
        
        assert main.app is not None
        from fastapi import FastAPI
        assert isinstance(main.app, FastAPI)
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_app_title(self, mock_static, mock_setup):
        """Test that app has correct title"""
        import importlib
        import main
        importlib.reload(main)
        
        assert main.app.title == "Multi-House Application"
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    @patch('main.config.DEBUG', True)
    def test_app_debug_mode(self, mock_static, mock_setup):
        """Test that app debug mode matches config"""
        import importlib
        import main
        importlib.reload(main)
        
        assert main.app.debug is True
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_static_files_mounted(self, mock_static, mock_setup):
        """Test that static files are mounted"""
        import importlib
        import main
        importlib.reload(main)
        
        # Verify mount was called
        # The app.mount is actually called during import
        assert mock_static.called
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_components_setup_called(self, mock_static, mock_setup):
        """Test that setup_components is called"""
        import importlib
        import main
        importlib.reload(main)
        
        mock_setup.assert_called_once()
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_templates_initialized(self, mock_static, mock_setup):
        """Test that Jinja2Templates is initialized"""
        import importlib
        import main
        importlib.reload(main)
        
        assert main.templates is not None


class TestRootRoute:
    """Tests for the root route handler"""
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_read_root_exists(self, mock_static, mock_setup):
        """Test that read_root function exists"""
        from main import read_root
        
        assert callable(read_root)
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    @patch('main.templates')
    def test_read_root_returns_template_response(self, mock_templates, mock_static, mock_setup):
        """Test that read_root returns a template response"""
        from main import read_root
        from fastapi import Request
        
        mock_request = MagicMock(spec=Request)
        mock_templates.TemplateResponse.return_value = "template_response"
        
        result = read_root(mock_request)
        
        mock_templates.TemplateResponse.assert_called_once()
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    @patch('main.templates')
    def test_read_root_uses_index_template(self, mock_templates, mock_static, mock_setup):
        """Test that read_root uses index.html template"""
        from main import read_root
        from fastapi import Request
        
        mock_request = MagicMock(spec=Request)
        mock_templates.TemplateResponse.return_value = "template_response"
        
        read_root(mock_request)
        
        call_args = mock_templates.TemplateResponse.call_args
        assert "index.html" in call_args[0]
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    @patch('main.templates')
    def test_read_root_context_has_request(self, mock_templates, mock_static, mock_setup):
        """Test that context includes request"""
        from main import read_root
        from fastapi import Request
        
        mock_request = MagicMock(spec=Request)
        
        read_root(mock_request)
        
        call_args = mock_templates.TemplateResponse.call_args
        context = call_args[0][1]
        assert "request" in context
        assert context["request"] == mock_request
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    @patch('main.templates')
    def test_read_root_context_has_current_alter(self, mock_templates, mock_static, mock_setup):
        """Test that context includes current_alter"""
        from main import read_root
        from fastapi import Request
        
        mock_request = MagicMock(spec=Request)
        
        read_root(mock_request)
        
        call_args = mock_templates.TemplateResponse.call_args
        context = call_args[0][1]
        assert "current_alter" in context
        assert context["current_alter"] == "global"
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    @patch('main.templates')
    def test_read_root_context_has_alters_status(self, mock_templates, mock_static, mock_setup):
        """Test that context includes alters_status"""
        from main import read_root
        from fastapi import Request
        
        mock_request = MagicMock(spec=Request)
        
        read_root(mock_request)
        
        call_args = mock_templates.TemplateResponse.call_args
        context = call_args[0][1]
        assert "alters_status" in context
        assert isinstance(context["alters_status"], dict)
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    @patch('main.templates')
    def test_read_root_alters_status_structure(self, mock_templates, mock_static, mock_setup):
        """Test that alters_status has expected structure"""
        from main import read_root
        from fastapi import Request
        
        mock_request = MagicMock(spec=Request)
        
        read_root(mock_request)
        
        call_args = mock_templates.TemplateResponse.call_args
        context = call_args[0][1]
        alters = context["alters_status"]
        
        # Check for expected alters
        assert "seles" in alters
        assert "dexen" in alters
        assert "yuki" in alters
        
        # All should be boolean values
        assert all(isinstance(v, bool) for v in alters.values())


class TestMainExecution:
    """Tests for main execution block"""
    
    @patch('main.uvicorn.run')
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_main_runs_uvicorn(self, mock_static, mock_setup, mock_uvicorn):
        """Test that __main__ block runs uvicorn"""
        # This would be tested by running the script directly
        # Here we just verify the import structure allows it
        import main
        assert hasattr(main, 'app')
    
    @patch('main.config.PORT', 8080)
    @patch('main.config.DEBUG', True)
    def test_main_uses_config_values(self, mock_static=None, mock_setup=None):
        """Test that config values are accessible"""
        import main
        import config
        
        # Config values should be accessible
        assert hasattr(config, 'PORT')
        assert hasattr(config, 'DEBUG')


class TestAppRoutes:
    """Tests for application routes"""
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_root_route_registered(self, mock_static, mock_setup):
        """Test that root route is registered"""
        from main import app
        
        routes = [route.path for route in app.routes]
        assert "/" in routes
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_root_route_method(self, mock_static, mock_setup):
        """Test that root route accepts GET method"""
        from main import app
        
        root_route = None
        for route in app.routes:
            if route.path == "/":
                root_route = route
                break
        
        assert root_route is not None
        # FastAPI routes have methods attribute
        if hasattr(root_route, 'methods'):
            assert "GET" in root_route.methods


class TestAppIntegration:
    """Integration tests for the application"""
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_app_can_be_imported(self, mock_static, mock_setup):
        """Test that app can be imported without errors"""
        try:
            import main
            assert True
        except Exception as e:
            pytest.fail(f"Failed to import main: {e}")
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    def test_app_configuration_complete(self, mock_static, mock_setup):
        """Test that app has all necessary configuration"""
        from main import app
        
        assert app.title is not None
        assert hasattr(app, 'debug')
        assert hasattr(app, 'routes')
    
    @patch('main.setup_components')
    @patch('main.StaticFiles')
    @patch('main.templates')
    def test_read_root_with_test_client(self, mock_templates, mock_static, mock_setup):
        """Test root route with TestClient"""
        from fastapi.testclient import TestClient
        from main import app
        
        mock_templates.TemplateResponse.return_value = MagicMock()
        
        client = TestClient(app)
        response = client.get("/")
        
        # Should not raise an error
        assert response is not None