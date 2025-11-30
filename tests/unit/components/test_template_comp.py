"""
Unit tests for components/template_comp.py
Tests for template component setup
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))


class TestSetupTemplate:
    """Tests for setup_template function"""
    
    @patch('components.template_comp.template_router')
    def test_setup_template_includes_router(self, mock_router):
        """Test that setup_template includes the template router"""
        from components.template_comp import setup_template
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_template(app)
        
        app.include_router.assert_called_once_with(mock_router)
    
    @patch('components.template_comp.template_router')
    def test_setup_template_returns_info(self, mock_router):
        """Test that setup_template returns correct component info"""
        from components.template_comp import setup_template
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_template(app)
        
        assert result is not None
        assert isinstance(result, dict)
        assert result["name"] == "template"
        assert result["routes"] == ["/template/*", "/template/alter/*"]
        assert result["initialized"] is True
    
    @patch('components.template_comp.template_router')
    def test_setup_template_with_mock_app(self, mock_router):
        """Test setup_template with a mocked FastAPI app"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        result = setup_template(mock_app)
        
        mock_app.include_router.assert_called_once_with(mock_router)
        assert result["initialized"] is True
    
    @patch('components.template_comp.template_router')
    def test_setup_template_idempotent(self, mock_router):
        """Test that setup_template can be called multiple times"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        
        result1 = setup_template(mock_app)
        result2 = setup_template(mock_app)
        
        assert result1 == result2
        assert mock_app.include_router.call_count == 2
    
    @patch('components.template_comp.template_router')
    def test_setup_template_route_prefix(self, mock_router):
        """Test that template routes use correct prefix"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        result = setup_template(mock_app)
        
        # Verify the routes list contains template prefix
        assert any("/template" in route for route in result["routes"])
    
    @patch('components.template_comp.template_router')
    def test_setup_template_component_name(self, mock_router):
        """Test that component name is correctly set"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        result = setup_template(mock_app)
        
        assert result["name"] == "template"
    
    @patch('components.template_comp.template_router')
    def test_setup_template_returns_dict_keys(self, mock_router):
        """Test that returned dict has all required keys"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        result = setup_template(mock_app)
        
        assert "name" in result
        assert "routes" in result
        assert "initialized" in result
    
    @patch('components.template_comp.template_router')
    def test_setup_template_multiple_routes(self, mock_router):
        """Test that template component registers multiple route patterns"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        result = setup_template(mock_app)
        
        # Template component should have multiple route patterns
        assert len(result["routes"]) >= 2
        assert "/template/*" in result["routes"]
        assert "/template/alter/*" in result["routes"]
    
    @patch('components.template_comp.template_router')
    def test_setup_template_initialized_flag(self, mock_router):
        """Test that initialized flag is always True after setup"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        result = setup_template(mock_app)
        
        assert result["initialized"] is True
        assert isinstance(result["initialized"], bool)
    
    @patch('components.template_comp.template_router')
    def test_setup_template_routes_are_strings(self, mock_router):
        """Test that all returned routes are strings"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        result = setup_template(mock_app)
        
        assert all(isinstance(route, str) for route in result["routes"])
    
    @patch('components.template_comp.template_router')
    def test_setup_template_routes_are_unique(self, mock_router):
        """Test that all returned routes are unique"""
        from components.template_comp import setup_template
        
        mock_app = MagicMock()
        result = setup_template(mock_app)
        
        routes = result["routes"]
        assert len(routes) == len(set(routes))