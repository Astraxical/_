"""
Tests for components/__init__.py
"""
import pytest
from fastapi import FastAPI


def test_validate_routes_no_conflicts():
    """Test route validation with no conflicts"""
    from components import validate_routes
    
    components = [
        {"name": "admin", "routes": ["/admin/*"]},
        {"name": "forums", "routes": ["/forums/*"]},
        {"name": "rtc", "routes": ["/rtc/*"]}
    ]
    
    result = validate_routes(components)
    assert result == True


def test_validate_routes_with_conflict():
    """Test route validation detects conflicts"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": ["/api/*", "/admin/*"]},
        {"name": "module2", "routes": ["/users/*", "/admin/*"]}  # Conflict
    ]
    
    with pytest.raises(ValueError, match="Route conflict detected: /admin/\\*"):
        validate_routes(components)


def test_validate_routes_empty_list():
    """Test route validation with empty component list"""
    from components import validate_routes
    
    components = []
    result = validate_routes(components)
    assert result == True


def test_validate_routes_no_routes_key():
    """Test route validation when components have no 'routes' key"""
    from components import validate_routes
    
    components = [
        {"name": "module1"},
        {"name": "module2"}
    ]
    
    result = validate_routes(components)
    assert result == True


def test_validate_routes_empty_routes():
    """Test route validation with empty routes list"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": []},
        {"name": "module2", "routes": []}
    ]
    
    result = validate_routes(components)
    assert result == True


def test_validate_routes_mixed_routes():
    """Test route validation with some components having routes and some not"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": ["/api/*"]},
        {"name": "module2"},
        {"name": "module3", "routes": ["/users/*"]}
    ]
    
    result = validate_routes(components)
    assert result == True


def test_validate_routes_multiple_routes_per_component():
    """Test route validation with multiple routes per component"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": ["/api/*", "/api/v2/*"]},
        {"name": "module2", "routes": ["/users/*", "/profiles/*"]}
    ]
    
    result = validate_routes(components)
    assert result == True


def test_validate_routes_duplicate_in_multiple_routes():
    """Test detecting conflict when one component has duplicate in list"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": ["/api/*", "/users/*"]},
        {"name": "module2", "routes": ["/profiles/*", "/api/*"]}  # Conflict
    ]
    
    with pytest.raises(ValueError, match="Route conflict detected: /api/\\*"):
        validate_routes(components)


def test_setup_components_returns_successfully(test_app, monkeypatch):
    """Test that setup_components completes without error"""
    from components import setup_components
    
    # Mock the component setup functions to avoid import errors
    def mock_setup_admin(app):
        return {"name": "admin", "routes": ["/admin/*"], "initialized": True}
    
    def mock_setup_forums(app):
        return {"name": "forums", "routes": ["/forums/*"], "initialized": True}
    
    def mock_setup_rtc(app):
        return {"name": "rtc", "routes": ["/rtc/*"], "initialized": True}
    
    # Patch the imports
    import sys
    from unittest.mock import MagicMock
    
    mock_admin_comp = MagicMock()
    mock_admin_comp.setup_admin = mock_setup_admin
    
    mock_forums_comp = MagicMock()
    mock_forums_comp.setup_forums = mock_setup_forums
    
    mock_rtc_comp = MagicMock()
    mock_rtc_comp.setup_rtc = mock_setup_rtc
    
    sys.modules['components.admin_comp'] = mock_admin_comp
    sys.modules['components.forums_comp'] = mock_forums_comp
    sys.modules['components.rtc_comp'] = mock_rtc_comp
    
    # Should not raise an exception
    setup_components(test_app)
    
    # Clean up
    del sys.modules['components.admin_comp']
    del sys.modules['components.forums_comp']
    del sys.modules['components.rtc_comp']


def test_validate_routes_preserves_order():
    """Test that route validation preserves component order"""
    from components import validate_routes
    
    components = [
        {"name": "first", "routes": ["/first/*"]},
        {"name": "second", "routes": ["/second/*"]},
        {"name": "third", "routes": ["/third/*"]}
    ]
    
    # Should not raise
    result = validate_routes(components)
    assert result == True


def test_validate_routes_exact_duplicates():
    """Test detection of exact duplicate routes"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": ["/exact/path"]},
        {"name": "module2", "routes": ["/exact/path"]}
    ]
    
    with pytest.raises(ValueError, match="Route conflict detected: /exact/path"):
        validate_routes(components)


def test_validate_routes_case_sensitive():
    """Test that route validation is case-sensitive"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": ["/API/*"]},
        {"name": "module2", "routes": ["/api/*"]}
    ]
    
    # Different cases should not conflict
    result = validate_routes(components)
    assert result == True


def test_validate_routes_with_none_values():
    """Test route validation handles None values gracefully"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": None},
        {"name": "module2", "routes": ["/api/*"]}
    ]
    
    # Should handle None gracefully
    result = validate_routes(components)
    assert result == True


def test_validate_routes_single_component():
    """Test route validation with single component"""
    from components import validate_routes
    
    components = [
        {"name": "only_module", "routes": ["/api/*", "/users/*", "/admin/*"]}
    ]
    
    result = validate_routes(components)
    assert result == True


def test_validate_routes_component_self_conflict():
    """Test detection of conflicts within same component"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": ["/api/*", "/api/*"]}  # Self-conflict
    ]
    
    with pytest.raises(ValueError, match="Route conflict detected: /api/\\*"):
        validate_routes(components)


def test_validate_routes_similar_but_different():
    """Test that similar but different routes don't conflict"""
    from components import validate_routes
    
    components = [
        {"name": "module1", "routes": ["/api/v1/*"]},
        {"name": "module2", "routes": ["/api/v2/*"]},
        {"name": "module3", "routes": ["/api/*"]}
    ]
    
    result = validate_routes(components)
    assert result == True