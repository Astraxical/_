"""
Unit tests for components/forums_comp.py
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import FastAPI
from components.forums_comp import setup_forums


class TestSetupForums:
    """Test forums component setup"""
    
    def test_setup_forums_returns_dict(self):
        """Test that setup_forums returns a dictionary"""
        app = FastAPI()
        
        result = setup_forums(app)
        
        assert isinstance(result, dict)
    
    def test_setup_forums_return_structure(self):
        """Test that setup_forums returns correct structure"""
        app = FastAPI()
        
        result = setup_forums(app)
        
        assert "name" in result
        assert "routes" in result
        assert "initialized" in result
    
    def test_setup_forums_name(self):
        """Test that forums component has correct name"""
        app = FastAPI()
        
        result = setup_forums(app)
        
        assert result["name"] == "forums"
    
    def test_setup_forums_routes(self):
        """Test that forums component declares routes"""
        app = FastAPI()
        
        result = setup_forums(app)
        
        assert isinstance(result["routes"], list)
        assert "/forums/*" in result["routes"]
    
    def test_setup_forums_initialized(self):
        """Test that forums component marks as initialized"""
        app = FastAPI()
        
        result = setup_forums(app)
        
        assert result["initialized"] is True
    
    def test_setup_forums_with_valid_app(self):
        """Test setup_forums with valid FastAPI app"""
        app = FastAPI()
        
        result = setup_forums(app)
        
        assert result is not None
        assert result["name"] == "forums"
    
    def test_setup_forums_router_prefix(self):
        """Test that forums router has /forums prefix"""
        app = FastAPI()
        
        result = setup_forums(app)
        
        # Routes should indicate /forums prefix
        assert any("/forums" in route for route in result["routes"])
    
    def test_setup_forums_multiple_calls(self):
        """Test that setup_forums can be called multiple times"""
        app1 = FastAPI()
        app2 = FastAPI()
        
        result1 = setup_forums(app1)
        result2 = setup_forums(app2)
        
        assert result1["name"] == result2["name"]
        assert result1["routes"] == result2["routes"]