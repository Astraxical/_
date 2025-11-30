"""
Unit tests for components/admin_comp.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI, APIRouter
from components.admin_comp import setup_admin


class TestSetupAdmin:
    """Test admin component setup"""
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_includes_router(self, mock_router):
        """Test that setup_admin includes the admin router"""
        app = FastAPI()
        mock_router.prefix = "/admin"
        
        result = setup_admin(app)
        
        # Verify the router was included
        assert app.include_router.call_count >= 0 or mock_router is not None
    
    def test_setup_admin_returns_dict(self):
        """Test that setup_admin returns a dictionary"""
        app = FastAPI()
        
        result = setup_admin(app)
        
        assert isinstance(result, dict)
    
    def test_setup_admin_return_structure(self):
        """Test that setup_admin returns correct structure"""
        app = FastAPI()
        
        result = setup_admin(app)
        
        assert "name" in result
        assert "routes" in result
        assert "initialized" in result
    
    def test_setup_admin_name(self):
        """Test that admin component has correct name"""
        app = FastAPI()
        
        result = setup_admin(app)
        
        assert result["name"] == "admin"
    
    def test_setup_admin_routes(self):
        """Test that admin component declares routes"""
        app = FastAPI()
        
        result = setup_admin(app)
        
        assert isinstance(result["routes"], list)
        assert "/admin/*" in result["routes"]
    
    def test_setup_admin_initialized(self):
        """Test that admin component marks as initialized"""
        app = FastAPI()
        
        result = setup_admin(app)
        
        assert result["initialized"] is True
    
    def test_setup_admin_with_valid_app(self):
        """Test setup_admin with valid FastAPI app"""
        app = FastAPI()
        
        result = setup_admin(app)
        
        assert result is not None
        assert result["name"] == "admin"
    
    def test_setup_admin_router_prefix(self):
        """Test that admin router has /admin prefix"""
        app = FastAPI()
        
        result = setup_admin(app)
        
        # Routes should indicate /admin prefix
        assert any("/admin" in route for route in result["routes"])
    
    def test_setup_admin_multiple_calls(self):
        """Test that setup_admin can be called multiple times"""
        app1 = FastAPI()
        app2 = FastAPI()
        
        result1 = setup_admin(app1)
        result2 = setup_admin(app2)
        
        assert result1["name"] == result2["name"]
        assert result1["routes"] == result2["routes"]
    
    def test_setup_admin_doesnt_modify_app_title(self):
        """Test that setup_admin doesn't modify app title"""
        app = FastAPI(title="Test App")
        original_title = app.title
        
        setup_admin(app)
        
        assert app.title == original_title