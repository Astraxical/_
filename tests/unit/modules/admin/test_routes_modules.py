"""
Unit tests for modules/admin/routes/modules.py
Tests for module management routes
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestGetModules:
    """Tests for get_modules route"""
    
    def test_get_modules_returns_dict(self):
        """Test that get_modules returns dictionary"""
        from modules.admin.routes.modules import get_modules
        
        result = get_modules()
        
        assert isinstance(result, dict)
    
    def test_get_modules_has_message(self):
        """Test that response includes message"""
        from modules.admin.routes.modules import get_modules
        
        result = get_modules()
        
        assert "message" in result
    
    def test_get_modules_has_modules_list(self):
        """Test that response includes modules list"""
        from modules.admin.routes.modules import get_modules
        
        result = get_modules()
        
        assert "modules" in result
        assert isinstance(result["modules"], list)
    
    def test_get_modules_empty_list_default(self):
        """Test that modules list is empty by default"""
        from modules.admin.routes.modules import get_modules
        
        result = get_modules()
        
        assert len(result["modules"]) == 0


class TestToggleModule:
    """Tests for toggle_module route"""
    
    def test_toggle_module_returns_dict(self):
        """Test that toggle_module returns dictionary"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("test_module")
        
        assert isinstance(result, dict)
    
    def test_toggle_module_has_message(self):
        """Test that response includes message"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("test_module")
        
        assert "message" in result
    
    def test_toggle_module_has_status(self):
        """Test that response includes status"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("test_module")
        
        assert "status" in result
    
    def test_toggle_module_includes_module_name(self):
        """Test that message includes module name"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("forums")
        
        assert "forums" in result["message"]
    
    def test_toggle_module_returns_success(self):
        """Test that toggle returns success status"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("forums")
        
        assert result["status"] == "success"
    
    def test_toggle_module_with_empty_name(self):
        """Test toggle with empty module name"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("")
        
        assert "message" in result
        assert "status" in result
    
    def test_toggle_module_with_special_chars(self):
        """Test toggle with special characters"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("module@#$")
        
        assert isinstance(result, dict)


class TestRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_exists(self):
        """Test that router is defined"""
        from modules.admin.routes.modules import router
        
        assert router is not None
    
    def test_router_is_api_router(self):
        """Test that router is an APIRouter instance"""
        from fastapi import APIRouter
        from modules.admin.routes.modules import router
        
        assert isinstance(router, APIRouter)


class TestModulesRouteIntegration:
    """Integration tests for module management routes"""
    
    def test_get_modules_with_test_client(self):
        """Test get modules with FastAPI TestClient"""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from modules.admin.routes.modules import router
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "modules" in data
    
    def test_toggle_module_with_test_client(self):
        """Test toggle module with TestClient"""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from modules.admin.routes.modules import router
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.post("/toggle/forums")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_toggle_different_modules(self):
        """Test toggling different modules"""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from modules.admin.routes.modules import router
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        modules = ["forums", "rtc", "admin"]
        for module in modules:
            response = client.post(f"/toggle/{module}")
            assert response.status_code == 200