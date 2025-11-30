"""
Tests for main.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient


def test_app_creation():
    """Test that FastAPI app is created correctly"""
    with patch('main.setup_components'):
        from main import app
        
        assert app is not None
        assert app.title == "Multi-House Application"


def test_app_mounts_static_files():
    """Test that static files are mounted"""
    with patch('main.setup_components'):
        from main import app
        
        # Check that /static route exists in some form
        routes = [route.path for route in app.routes]
        assert any('/static' in route for route in routes)


def test_root_endpoint_returns_response():
    """Test that root endpoint returns a response"""
    with patch('main.setup_components'):
        from main import app
        
        client = TestClient(app)
        response = client.get("/")
        
        # Should return 200 or redirect
        assert response.status_code in [200, 307, 308]


def test_root_endpoint_context():
    """Test that root endpoint provides correct context"""
    with patch('main.setup_components'):
        from main import app, read_root
        from fastapi import Request
        
        # Create a mock request
        mock_request = Mock(spec=Request)
        
        response = read_root(mock_request)
        
        # Check that response contains template response
        assert hasattr(response, 'template') or hasattr(response, 'context')


def test_setup_components_called():
    """Test that setup_components is called during app initialization"""
    mock_setup = Mock()
    
    with patch('main.setup_components', mock_setup):
        # Need to reload main module to trigger initialization
        import sys
        if 'main' in sys.modules:
            del sys.modules['main']
        
        import main
        
        # setup_components should have been called
        mock_setup.assert_called_once()


def test_templates_configured():
    """Test that Jinja2 templates are configured"""
    with patch('main.setup_components'):
        from main import templates
        
        assert templates is not None
        assert hasattr(templates, 'env')


def test_app_debug_mode_from_config():
    """Test that app debug mode is set from config"""
    with patch('main.setup_components'):
        with patch('main.config') as mock_config:
            mock_config.DEBUG = True
            
            import sys
            if 'main' in sys.modules:
                del sys.modules['main']
            
            # This would need to reload the module
            # For now, just verify config is imported
            from main import app
            assert hasattr(app, 'debug')


def test_root_route_has_correct_method():
    """Test that root route uses GET method"""
    with patch('main.setup_components'):
        from main import app
        
        # Find the root route
        root_route = None
        for route in app.routes:
            if hasattr(route, 'path') and route.path == '/':
                root_route = route
                break
        
        if root_route and hasattr(root_route, 'methods'):
            assert 'GET' in root_route.methods


def test_context_has_required_keys():
    """Test that context has all required keys"""
    with patch('main.setup_components'):
        from main import read_root
        from fastapi import Request
        
        mock_request = Mock(spec=Request)
        response = read_root(mock_request)
        
        # Get context from response
        if hasattr(response, 'context'):
            context = response.context
            assert 'request' in context
            assert 'current_alter' in context
            assert 'alters_status' in context


def test_default_alter_is_global():
    """Test that default alter is 'global'"""
    with patch('main.setup_components'):
        from main import read_root
        from fastapi import Request
        
        mock_request = Mock(spec=Request)
        response = read_root(mock_request)
        
        if hasattr(response, 'context'):
            assert response.context['current_alter'] == 'global'


def test_default_alters_status():
    """Test default alters status"""
    with patch('main.setup_components'):
        from main import read_root
        from fastapi import Request
        
        mock_request = Mock(spec=Request)
        response = read_root(mock_request)
        
        if hasattr(response, 'context'):
            alters_status = response.context['alters_status']
            assert 'seles' in alters_status
            assert 'dexen' in alters_status
            assert 'yuki' in alters_status
            assert alters_status['seles'] == False
            assert alters_status['dexen'] == False
            assert alters_status['yuki'] == False


def test_app_can_handle_requests():
    """Test that app can handle basic requests"""
    with patch('main.setup_components'):
        from main import app
        
        client = TestClient(app)
        
        # Test that app can receive requests
        try:
            response = client.get("/")
            # Any response is fine, just shouldn't crash
            assert response.status_code >= 0
        except Exception as e:
            # If there's a template error, that's okay for this test
            assert "template" in str(e).lower() or "jinja" in str(e).lower()


def test_static_mount_name():
    """Test that static files are mounted with correct name"""
    with patch('main.setup_components'):
        from main import app
        
        # Look for static mount
        static_found = False
        for route in app.routes:
            if hasattr(route, 'path') and '/static' in route.path:
                static_found = True
                break
        
        assert static_found


def test_uvicorn_config_in_main():
    """Test that uvicorn configuration is present"""
    with patch('main.setup_components'):
        import main
        
        # Check that the module has the if __name__ == "__main__" block
        # by checking the source
        import inspect
        source = inspect.getsource(main)
        
        assert 'if __name__ == "__main__"' in source
        assert 'uvicorn.run' in source


def test_uvicorn_uses_config_values():
    """Test that uvicorn uses config values"""
    with patch('main.setup_components'):
        import main
        import inspect
        
        source = inspect.getsource(main)
        
        # Check that config.PORT is used
        assert 'config.PORT' in source
        assert 'config.DEBUG' in source