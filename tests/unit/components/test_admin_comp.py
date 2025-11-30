"""
Unit tests for components/admin_comp.py
Tests for admin component setup
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))


class TestSetupAdmin:
    """Tests for setup_admin function"""
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_includes_router(self, mock_router):
        """Test that setup_admin includes the admin router"""
        from components.admin_comp import setup_admin
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_admin(app)
        
        app.include_router.assert_called_once_with(mock_router)
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_returns_info(self, mock_router):
        """Test that setup_admin returns correct component info"""
        from components.admin_comp import setup_admin
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_admin(app)
        
        assert result is not None
        assert isinstance(result, dict)
        assert result["name"] == "admin"
        assert result["routes"] == ["/admin/*"]
        assert result["initialized"] is True
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_with_mock_app(self, mock_router):
        """Test setup_admin with a mocked FastAPI app"""
        from components.admin_comp import setup_admin
        
        mock_app = MagicMock()
        result = setup_admin(mock_app)
        
        mock_app.include_router.assert_called_once_with(mock_router)
        assert result["initialized"] is True
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_idempotent(self, mock_router):
        """Test that setup_admin can be called multiple times"""
        from components.admin_comp import setup_admin
        
        mock_app = MagicMock()
        
        result1 = setup_admin(mock_app)
        result2 = setup_admin(mock_app)
        
        assert result1 == result2
        assert mock_app.include_router.call_count == 2
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_route_prefix(self, mock_router):
        """Test that admin routes use correct prefix"""
        from components.admin_comp import setup_admin
        
        mock_app = MagicMock()
        result = setup_admin(mock_app)
        
        # Verify the routes list contains admin prefix
        assert any("/admin" in route for route in result["routes"])
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_component_name(self, mock_router):
        """Test that component name is correctly set"""
        from components.admin_comp import setup_admin
        
        mock_app = MagicMock()
        result = setup_admin(mock_app)
        
        assert result["name"] == "admin"
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_returns_dict_keys(self, mock_router):
        """Test that returned dict has all required keys"""
        from components.admin_comp import setup_admin
        
        mock_app = MagicMock()
        result = setup_admin(mock_app)
        
        assert "name" in result
        assert "routes" in result
        assert "initialized" in result
    
    @patch('components.admin_comp.admin_router')
    def test_setup_admin_router_imported(self, mock_router):
        """Test that admin router is properly imported"""
        from components.admin_comp import setup_admin
        
        # This test verifies the import happens correctly
        # by checking that the function can be called
        mock_app = MagicMock()
        result = setup_admin(mock_app)
        
        assert result is not None