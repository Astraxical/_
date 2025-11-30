"""
Unit tests for modules/admin/routes/dashboard.py
Tests for admin dashboard routes
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestAdminDashboardRoute:
    """Tests for admin_dashboard route"""
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_renders_template(self, mock_templates):
        """Test that admin dashboard renders the correct template"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request = MagicMock()
        mock_response = MagicMock()
        mock_templates.TemplateResponse.return_value = mock_response
        
        result = admin_dashboard(mock_request)
        
        mock_templates.TemplateResponse.assert_called_once_with(
            "admin/index.html",
            {"request": mock_request}
        )
        assert result == mock_response
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_fallback_on_template_error(self, mock_templates):
        """Test fallback to JSON when template doesn't exist"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request = MagicMock()
        mock_templates.TemplateResponse.side_effect = Exception("Template not found")
        
        result = admin_dashboard(mock_request)
        
        # Should return JSON response
        assert isinstance(result, dict)
        assert "message" in result
        assert "stats" in result
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_json_structure(self, mock_templates):
        """Test structure of fallback JSON response"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request = MagicMock()
        mock_templates.TemplateResponse.side_effect = Exception()
        
        result = admin_dashboard(mock_request)
        
        assert "message" in result
        assert "stats" in result
        assert "users" in result["stats"]
        assert "modules" in result["stats"]
        assert "system_status" in result["stats"]


class TestGetModuleStatusRoute:
    """Tests for get_module_status route"""
    
    def test_get_module_status_returns_all_modules(self):
        """Test that get_module_status returns all four modules"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        assert "modules" in result
        assert len(result["modules"]) == 4
    
    def test_get_module_status_includes_template_module(self):
        """Test that template module is included in status"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        module_names = [m["name"] for m in result["modules"]]
        assert "template" in module_names
    
    def test_get_module_status_all_active(self):
        """Test that all modules are reported as active"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        for module in result["modules"]:
            assert module["status"] == "active"
    
    def test_get_module_status_structure(self):
        """Test the structure of module status response"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        assert "message" in result
        assert "modules" in result
        assert isinstance(result["modules"], list)
        
        for module in result["modules"]:
            assert "name" in module
            assert "status" in module
    
    def test_get_module_status_includes_all_expected_modules(self):
        """Test that all expected modules are included"""
        from modules.admin.routes.dashboard import get_module_status
        
        result = get_module_status()
        
        expected_modules = {"forums", "rtc", "admin", "template"}
        module_names = {m["name"] for m in result["modules"]}
        
        assert expected_modules == module_names


class TestDashboardRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_exists(self):
        """Test that router is properly defined"""
        from modules.admin.routes.dashboard import router
        from fastapi import APIRouter
        
        assert router is not None
        assert isinstance(router, APIRouter)
    
    @patch('os.makedirs')
    def test_templates_directory_created(self, mock_makedirs):
        """Test that templates directory is created if it doesn't exist"""
        import importlib
        import modules.admin.routes.dashboard as dashboard_module
        
        # Reload to trigger directory creation
        importlib.reload(dashboard_module)
        
        # makedirs should have been called
        assert mock_makedirs.called


class TestAdminDashboardEdgeCases:
    """Tests for edge cases in admin dashboard"""
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_with_none_request(self, mock_templates):
        """Test dashboard with None request"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_templates.TemplateResponse.side_effect = Exception()
        
        # Should not crash, return JSON
        result = admin_dashboard(None)
        
        assert isinstance(result, dict)
    
    @patch('modules.admin.routes.dashboard.templates')
    def test_admin_dashboard_multiple_calls(self, mock_templates):
        """Test multiple calls to dashboard"""
        from modules.admin.routes.dashboard import admin_dashboard
        
        mock_request1 = MagicMock()
        mock_request2 = MagicMock()
        
        admin_dashboard(mock_request1)
        admin_dashboard(mock_request2)
        
        # Should be called twice
        assert mock_templates.TemplateResponse.call_count == 2