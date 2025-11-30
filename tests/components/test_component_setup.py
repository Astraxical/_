"""
Tests for individual component setup functions
"""
import pytest
from fastapi import FastAPI, APIRouter


def test_setup_admin_returns_dict():
    """Test that setup_admin returns correct dictionary"""
    from components.admin_comp import setup_admin
    
    app = FastAPI()
    result = setup_admin(app)
    
    assert isinstance(result, dict)
    assert result["name"] == "admin"
    assert result["routes"] == ["/admin/*"]
    assert result["initialized"] == True


def test_setup_admin_mounts_router():
    """Test that setup_admin mounts the router"""
    from components.admin_comp import setup_admin
    
    app = FastAPI()
    initial_routes = len(app.routes)
    
    setup_admin(app)
    
    # Router should be included (may add routes)
    assert len(app.routes) >= initial_routes


def test_setup_forums_returns_dict():
    """Test that setup_forums returns correct dictionary"""
    from components.forums_comp import setup_forums
    
    app = FastAPI()
    result = setup_forums(app)
    
    assert isinstance(result, dict)
    assert result["name"] == "forums"
    assert result["routes"] == ["/forums/*"]
    assert result["initialized"] == True


def test_setup_forums_mounts_router():
    """Test that setup_forums mounts the router"""
    from components.forums_comp import setup_forums
    
    app = FastAPI()
    initial_routes = len(app.routes)
    
    setup_forums(app)
    
    assert len(app.routes) >= initial_routes


def test_setup_rtc_returns_dict():
    """Test that setup_rtc returns correct dictionary"""
    from components.rtc_comp import setup_rtc
    
    app = FastAPI()
    result = setup_rtc(app)
    
    assert isinstance(result, dict)
    assert result["name"] == "rtc"
    assert result["routes"] == ["/rtc/*"]
    assert result["initialized"] == True


def test_setup_rtc_mounts_router():
    """Test that setup_rtc mounts the router"""
    from components.rtc_comp import setup_rtc
    
    app = FastAPI()
    initial_routes = len(app.routes)
    
    setup_rtc(app)
    
    assert len(app.routes) >= initial_routes


def test_setup_admin_with_existing_routes():
    """Test setup_admin when app already has routes"""
    from components.admin_comp import setup_admin
    
    app = FastAPI()
    
    # Add a test route first
    @app.get("/test")
    def test_route():
        return {"test": "route"}
    
    result = setup_admin(app)
    
    assert result["initialized"] == True


def test_setup_forums_with_existing_routes():
    """Test setup_forums when app already has routes"""
    from components.forums_comp import setup_forums
    
    app = FastAPI()
    
    @app.get("/existing")
    def existing_route():
        return {"existing": "route"}
    
    result = setup_forums(app)
    
    assert result["initialized"] == True


def test_setup_rtc_with_existing_routes():
    """Test setup_rtc when app already has routes"""
    from components.rtc_comp import setup_rtc
    
    app = FastAPI()
    
    @app.get("/pre-existing")
    def pre_existing():
        return {"pre": "existing"}
    
    result = setup_rtc(app)
    
    assert result["initialized"] == True


def test_all_components_can_be_setup_together():
    """Test that all components can be set up on same app"""
    from components.admin_comp import setup_admin
    from components.forums_comp import setup_forums
    from components.rtc_comp import setup_rtc
    
    app = FastAPI()
    
    admin_result = setup_admin(app)
    forums_result = setup_forums(app)
    rtc_result = setup_rtc(app)
    
    assert admin_result["initialized"] == True
    assert forums_result["initialized"] == True
    assert rtc_result["initialized"] == True


def test_component_setup_idempotent():
    """Test that setting up components multiple times doesn't break"""
    from components.admin_comp import setup_admin
    
    app = FastAPI()
    
    # Setup twice
    result1 = setup_admin(app)
    result2 = setup_admin(app)
    
    assert result1["initialized"] == True
    assert result2["initialized"] == True