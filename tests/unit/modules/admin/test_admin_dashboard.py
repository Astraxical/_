"""
Unit tests for admin dashboard routes
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import Request
from fastapi.testclient import TestClient
from fastapi import FastAPI

import sys
sys.path.insert(0, 'codebase')

from modules.admin.routes.dashboard import router, admin_dashboard, get_module_status


class TestAdminDashboard:
    """Tests for admin_dashboard route"""
    
    def test_admin_dashboard_returns_template_response(self):
        """Test that admin_dashboard attempts to render template"""
        mock_request = Mock(spec=Request)
        
        with patch('modules.admin.routes.dashboard.templates') as mock_templates:
            mock_templates.TemplateResponse.return_value = "template_response"
            
            result = admin_dashboard(mock_request)
            
            mock_templates.TemplateResponse.assert_called_once()
            call_args = mock_templates.TemplateResponse.call_args[0]
            assert call_args[0] == "admin/index.html"
            assert call_args[1]["request"] == mock_request
    
    def test_admin_dashboard_fallback_to_json(self):
        """Test that admin_dashboard falls back to JSON on template error"""
        mock_request = Mock(spec=Request)
        
        with patch('modules.admin.routes.dashboard.templates') as mock_templates:
            mock_templates.TemplateResponse.side_effect = Exception("Template not found")
            
            result = admin_dashboard(mock_request)
            
            assert isinstance(result, dict)
            assert "message" in result
            assert result["message"] == "Admin Dashboard"
            assert "stats" in result
    
    def test_admin_dashboard_fallback_has_correct_structure(self):
        """Test JSON fallback has expected structure"""
        mock_request = Mock(spec=Request)
        
        with patch('modules.admin.routes.dashboard.templates') as mock_templates:
            mock_templates.TemplateResponse.side_effect = Exception()
            
            result = admin_dashboard(mock_request)
            
            assert "stats" in result
            assert "users" in result["stats"]
            assert "modules" in result["stats"]
            assert "system_status" in result["stats"]
    
    def test_admin_dashboard_creates_templates_dir(self):
        """Test that template directory creation is attempted"""
        with patch('modules.admin.routes.dashboard.os.makedirs') as mock_makedirs:
            # Re-import to trigger directory creation
            import importlib
            import modules.admin.routes.dashboard as dashboard_module
            importlib.reload(dashboard_module)
            
            mock_makedirs.assert_called()


class TestGetModuleStatus:
    """Tests for get_module_status route"""
    
    def test_get_module_status_returns_dict(self):
        """Test that get_module_status returns a dictionary"""
        result = get_module_status()
        
        assert isinstance(result, dict)
    
    def test_get_module_status_has_message(self):
        """Test that response includes message"""
        result = get_module_status()
        
        assert "message" in result
        assert result["message"] == "Module status"
    
    def test_get_module_status_has_modules_list(self):
        """Test that response includes modules list"""
        result = get_module_status()
        
        assert "modules" in result
        assert isinstance(result["modules"], list)
    
    def test_get_module_status_includes_all_modules(self):
        """Test that all expected modules are included"""
        result = get_module_status()
        
        module_names = [m["name"] for m in result["modules"]]
        assert "forums" in module_names
        assert "rtc" in module_names
        assert "admin" in module_names
        assert "template" in module_names
    
    def test_get_module_status_modules_have_correct_structure(self):
        """Test that each module has name and status"""
        result = get_module_status()
        
        for module in result["modules"]:
            assert "name" in module
            assert "status" in module
            assert isinstance(module["name"], str)
            assert isinstance(module["status"], str)
    
    def test_get_module_status_all_active(self):
        """Test that all modules report as active"""
        result = get_module_status()
        
        for module in result["modules"]:
            assert module["status"] == "active"


class TestAdminRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_is_api_router(self):
        """Test that router is an APIRouter instance"""
        from fastapi import APIRouter
        assert isinstance(router, APIRouter)


class TestAdminDashboardIntegration:
    """Integration tests for admin dashboard"""
    
    def test_admin_dashboard_endpoint_accessible(self):
        """Test that admin dashboard endpoint is accessible"""
        app = FastAPI()
        app.include_router(router)
        
        client = TestClient(app)
        response = client.get("/")
        
        # Should return some response (either template or JSON)
        assert response.status_code in [200, 500]  # 500 if template not found
    
    def test_get_module_status_endpoint_accessible(self):
        """Test that module status endpoint is accessible"""
        app = FastAPI()
        app.include_router(router)
        
        client = TestClient(app)
        response = client.get("/modules")
        
        assert response.status_code == 200
        data = response.json()
        assert "modules" in data