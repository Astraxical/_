"""
Unit tests for components/forums_comp.py
Tests for forums component setup
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))


class TestSetupForums:
    """Tests for setup_forums function"""
    
    @patch('components.forums_comp.forums_router')
    def test_setup_forums_includes_router(self, mock_router):
        """Test that setup_forums includes the forums router"""
        from components.forums_comp import setup_forums
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_forums(app)
        
        app.include_router.assert_called_once_with(mock_router)
    
    @patch('components.forums_comp.forums_router')
    def test_setup_forums_returns_info(self, mock_router):
        """Test that setup_forums returns correct component info"""
        from components.forums_comp import setup_forums
        from fastapi import FastAPI
        
        app = FastAPI()
        result = setup_forums(app)
        
        assert result is not None
        assert isinstance(result, dict)
        assert result["name"] == "forums"
        assert result["routes"] == ["/forums/*"]
        assert result["initialized"] is True
    
    @patch('components.forums_comp.forums_router')
    def test_setup_forums_with_mock_app(self, mock_router):
        """Test setup_forums with a mocked FastAPI app"""
        from components.forums_comp import setup_forums
        
        mock_app = MagicMock()
        result = setup_forums(mock_app)
        
        mock_app.include_router.assert_called_once_with(mock_router)
        assert result["initialized"] is True
    
    @patch('components.forums_comp.forums_router')
    def test_setup_forums_idempotent(self, mock_router):
        """Test that setup_forums can be called multiple times"""
        from components.forums_comp import setup_forums
        
        mock_app = MagicMock()
        
        result1 = setup_forums(mock_app)
        result2 = setup_forums(mock_app)
        
        assert result1 == result2
        assert mock_app.include_router.call_count == 2
    
    @patch('components.forums_comp.forums_router')
    def test_setup_forums_route_prefix(self, mock_router):
        """Test that forums routes use correct prefix"""
        from components.forums_comp import setup_forums
        
        mock_app = MagicMock()
        result = setup_forums(mock_app)
        
        # Verify the routes list contains forums prefix
        assert any("/forums" in route for route in result["routes"])
    
    @patch('components.forums_comp.forums_router')
    def test_setup_forums_component_name(self, mock_router):
        """Test that component name is correctly set"""
        from components.forums_comp import setup_forums
        
        mock_app = MagicMock()
        result = setup_forums(mock_app)
        
        assert result["name"] == "forums"
    
    @patch('components.forums_comp.forums_router')
    def test_setup_forums_returns_dict_keys(self, mock_router):
        """Test that returned dict has all required keys"""
        from components.forums_comp import setup_forums
        
        mock_app = MagicMock()
        result = setup_forums(mock_app)
        
        assert "name" in result
        assert "routes" in result
        assert "initialized" in result