"""
Unit tests for modules/template/routes/alter.py
Tests for alter switching routes
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestSwitchAlterRoute:
    """Tests for switch_alter route"""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_success(self, mock_engine):
        """Test successful alter switch returns success message"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = True
        
        result = switch_alter("dexen")
        
        assert result["success"] is True
        assert "dexen" in result["message"]
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_failure(self, mock_engine):
        """Test failed alter switch returns failure message"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("nonexistent")
        
        assert result["success"] is False
        assert "Failed" in result["message"]
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_calls_engine(self, mock_engine):
        """Test that route calls template engine switch_alter"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = True
        
        switch_alter("yuki")
        
        mock_engine.switch_alter.assert_called_once_with("yuki")
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_with_empty_name(self, mock_engine):
        """Test switching with empty alter name"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("")
        
        assert result["success"] is False
    
    @patch('modules.template.routes.alter.template_engine')
    def test_switch_alter_with_special_characters(self, mock_engine):
        """Test switching with special characters in name"""
        from modules.template.routes.alter import switch_alter
        
        mock_engine.switch_alter.return_value = False
        
        result = switch_alter("alter@#$")
        
        # Should handle gracefully
        assert "success" in result


class TestGetAlterStatusRoute:
    """Tests for get_alter_status route"""
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_returns_current_alter(self, mock_engine):
        """Test that status endpoint returns current alter"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "seles"
        mock_engine.alters_status = {"seles": True, "dexen": False}
        
        result = get_alter_status()
        
        assert result["current_alter"] == "seles"
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_returns_all_alters(self, mock_engine):
        """Test that status endpoint returns all alters"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "seles"
        mock_engine.alters_status = {"seles": True, "dexen": False, "yuki": False}
        
        result = get_alter_status()
        
        assert "alters_status" in result
        assert len(result["alters_status"]) == 3
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_structure(self, mock_engine):
        """Test that status response has correct structure"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "seles"
        mock_engine.alters_status = {"seles": True}
        
        result = get_alter_status()
        
        assert "current_alter" in result
        assert "alters_status" in result
        assert isinstance(result["alters_status"], dict)
    
    @patch('modules.template.routes.alter.template_engine')
    def test_get_alter_status_with_no_fronting_alter(self, mock_engine):
        """Test status when no alter is fronting"""
        from modules.template.routes.alter import get_alter_status
        
        mock_engine.current_alter = "global"
        mock_engine.alters_status = {"seles": False, "dexen": False}
        
        result = get_alter_status()
        
        assert result["current_alter"] == "global"


class TestRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_exists(self):
        """Test that router is defined"""
        from modules.template.routes.alter import router
        
        assert router is not None
    
    def test_router_is_api_router(self):
        """Test that router is an APIRouter instance"""
        from fastapi import APIRouter
        from modules.template.routes.alter import router
        
        assert isinstance(router, APIRouter)
    
    def test_template_engine_singleton(self):
        """Test that template_engine is initialized"""
        from modules.template.routes.alter import template_engine
        
        assert template_engine is not None


class TestRouteIntegration:
    """Integration tests for template routes"""
    
    @patch('modules.template.routes.alter.TemplateEngine')
    def test_routes_work_with_test_client(self, mock_engine_class):
        """Test routes with FastAPI TestClient"""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from modules.template.routes.alter import router
        
        mock_engine = MagicMock()
        mock_engine.switch_alter.return_value = True
        mock_engine.current_alter = "seles"
        mock_engine.alters_status = {"seles": True}
        mock_engine_class.return_value = mock_engine
        
        app = FastAPI()
        app.include_router(router, prefix="/alter")
        client = TestClient(app)
        
        # Test switch endpoint
        response = client.get("/alter/switch/dexen")
        assert response.status_code == 200
        
        # Test status endpoint
        response = client.get("/alter/status")
        assert response.status_code == 200
        assert "current_alter" in response.json()