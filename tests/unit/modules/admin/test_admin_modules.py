"""
Unit tests for admin module management routes
"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, 'codebase')

from modules.admin.routes.modules import router, get_modules, toggle_module


class TestGetModules:
    """Tests for get_modules route"""
    
    def test_get_modules_returns_dict(self):
        """Test that get_modules returns a dictionary"""
        result = get_modules()
        
        assert isinstance(result, dict)
    
    def test_get_modules_has_message(self):
        """Test that response includes message"""
        result = get_modules()
        
        assert "message" in result
        assert "modules" in result["message"].lower()
    
    def test_get_modules_has_modules_list(self):
        """Test that response includes modules list"""
        result = get_modules()
        
        assert "modules" in result
        assert isinstance(result["modules"], list)
    
    def test_get_modules_empty_list(self):
        """Test that modules list is empty (placeholder)"""
        result = get_modules()
        
        assert len(result["modules"]) == 0


class TestToggleModule:
    """Tests for toggle_module route"""
    
    def test_toggle_module_returns_dict(self):
        """Test that toggle_module returns a dictionary"""
        result = toggle_module("test_module")
        
        assert isinstance(result, dict)
    
    def test_toggle_module_includes_module_name(self):
        """Test that response includes the module name"""
        module_name = "forums"
        result = toggle_module(module_name)
        
        assert module_name in result["message"]
    
    def test_toggle_module_has_status(self):
        """Test that response includes status"""
        result = toggle_module("test")
        
        assert "status" in result
        assert result["status"] == "success"
    
    def test_toggle_module_with_various_names(self):
        """Test toggle_module with different module names"""
        test_modules = ["admin", "forums", "rtc", "template", "custom_module"]
        
        for module_name in test_modules:
            result = toggle_module(module_name)
            
            assert "message" in result
            assert module_name in result["message"]
            assert result["status"] == "success"
    
    def test_toggle_module_with_special_characters(self):
        """Test toggle_module with special characters in name"""
        result = toggle_module("module-with-dash")
        
        assert "module-with-dash" in result["message"]
        assert result["status"] == "success"
    
    def test_toggle_module_empty_string(self):
        """Test toggle_module with empty string"""
        result = toggle_module("")
        
        assert isinstance(result, dict)
        assert "status" in result


class TestAdminModulesRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_is_api_router(self):
        """Test that router is an APIRouter instance"""
        from fastapi import APIRouter
        assert isinstance(router, APIRouter)


class TestAdminModulesIntegration:
    """Integration tests for admin modules routes"""
    
    def test_get_modules_endpoint_accessible(self):
        """Test that get modules endpoint is accessible"""
        app = FastAPI()
        app.include_router(router)
        
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "modules" in data
    
    def test_toggle_module_endpoint_accessible(self):
        """Test that toggle module endpoint is accessible"""
        app = FastAPI()
        app.include_router(router)
        
        client = TestClient(app)
        response = client.post("/toggle/test_module")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_toggle_module_endpoint_with_path_parameter(self):
        """Test toggle endpoint with various path parameters"""
        app = FastAPI()
        app.include_router(router)
        
        client = TestClient(app)
        
        test_modules = ["forums", "admin", "rtc"]
        for module in test_modules:
            response = client.post(f"/toggle/{module}")
            assert response.status_code == 200
            data = response.json()
            assert module in data["message"]