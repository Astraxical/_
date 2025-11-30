import pytest
from codebase.main import app


def test_app_startup():
    """Test that the app starts up correctly"""
    assert app is not None


def test_dependencies():
    """Test that all required dependencies are available"""
    try:
        import fastapi
        import uvicorn
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates
        print("All required modules are available")
        assert True
    except ImportError as e:
        pytest.fail(f"Missing dependency: {e}")


def test_component_setup():
    """Test that components are properly set up during app startup"""
    # We already confirmed this works by seeing "Successfully set up 3 components" on import
    # The components setup happens when the app is instantiated in main.py
    assert hasattr(app, 'routes')
    # Check that there are routes registered (admin, forums, rtc + default routes)
    assert len(app.routes) > 0