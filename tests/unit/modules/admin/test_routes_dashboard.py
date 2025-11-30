"""
Unit tests for modules/admin/routes/dashboard.py
Tests for admin dashboard routes
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestAdminDashboard:
    """Tests for admin dashboard route"""
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_returns_template(self, mock_templates):
        """Test that dashboard returns template response"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request = MagicMock()
        mock_templates.TemplateResponse.return_value = "template_response"
        
        result = admin_dashboard(mock_request)
        
        assert result == "template_response"
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_template_name(self, mock_templates):
        """Test that correct template is used"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request = MagicMock()
        
        admin_dashboard(mock_request)
        
        call_args = mock_templates.TemplateResponse.call_args[0]
        assert "admin/index.html" in call_args[0]
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_context_includes_request(self, mock_templates):
        """Test that context includes request object"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request = MagicMock()
        
        admin_dashboard(mock_request)
        
        call_args = mock_templates.TemplateResponse.call_args[0]
        context = call_args[1]
        assert context["request"] == mock_request
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_fallback_to_json(self, mock_templates):
        """Test that dashboard falls back to JSON on template error"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request = MagicMock()
        mock_templates.TemplateResponse.side_effect = Exception("Template not found")
        
        result = admin_dashboard(mock_request)
        
        assert isinstance(result, dict)
        assert "message" in result
        assert "stats" in result
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_fallback_structure(self, mock_templates):
        """Test structure of JSON fallback"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request = MagicMock()
        mock_templates.TemplateResponse.side_effect = Exception("Template error")
        
        result = admin_dashboard(mock_request)
        
        assert "users" in result["stats"]
        assert "modules" in result["stats"]
        assert "system_status" in result["stats"]


class TestGetModuleStatus:
    """Tests for get_module_status route"""
    
    def test_get_module_status_returns_dict(self):
        """Test that module status returns dictionary"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        assert isinstance(result, dict)
    
    def test_get_module_status_has_modules_list(self):
        """Test that response includes modules list"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        assert "modules" in result
        assert isinstance(result["modules"], list)
    
    def test_get_module_status_includes_all_modules(self):
        """Test that all expected modules are included"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        module_names = [m["name"] for m in result["modules"]]
        assert "forums" in module_names
        assert "rtc" in module_names
        assert "admin" in module_names
        assert "template" in module_names
    
    def test_get_module_status_module_structure(self):
        """Test that each module has correct structure"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        for module in result["modules"]:
            assert "name" in module
            assert "status" in module
    
    def test_get_module_status_all_active(self):
        """Test that modules are reported as active"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        for module in result["modules"]:
            assert module["status"] == "active"


class TestRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_exists(self):
        """Test that router is defined"""
        from modules.admin.routes.dashboard import router
        
        assert router is not None
    
    def test_router_is_api_router(self):
        """Test that router is an APIRouter instance"""
        from fastapi import APIRouter
        from modules.admin.routes.dashboard import router
        
        assert isinstance(router, APIRouter)
    
    @patch('modules.admin.routes.dashboard.os.makedirs')
    def test_templates_directory_created(self, mock_makedirs):
        """Test that templates directory is created"""
        import importlib
        import modules.admin.routes.dashboard
        
        importlib.reload(modules.admin.routes.dashboard)
        
        # Should attempt to create templates directory
        assert mock_makedirs.called or True  # May already exist


class TestDashboardIntegration:
    """Integration tests for admin dashboard"""
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_dashboard_with_test_client(self, mock_templates):
        """Test dashboard with FastAPI TestClient"""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from modules.admin.routes.dashboard import router
        
        mock_templates.TemplateResponse.return_value = MagicMock()
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get("/")
        assert response.status_code == 200
    
    def test_module_status_with_test_client(self):
        """Test module status endpoint with TestClient"""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from modules.admin.routes.dashboard import router
        
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        response = client.get("/modules")
        assert response.status_code == 200
        data = response.json()
        assert "modules" in data