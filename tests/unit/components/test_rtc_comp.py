"""
Unit tests for components/rtc_comp.py
"""
import pytest
from unittest.mock import Mock, patch
from fastapi import FastAPI
from components.rtc_comp import setup_rtc


class TestSetupRTC:
    """Test RTC component setup"""
    
    def test_setup_rtc_returns_dict(self):
        """Test that setup_rtc returns a dictionary"""
        app = FastAPI()
        
        result = setup_rtc(app)
        
        assert isinstance(result, dict)
    
    def test_setup_rtc_return_structure(self):
        """Test that setup_rtc returns correct structure"""
        app = FastAPI()
        
        result = setup_rtc(app)
        
        assert "name" in result
        assert "routes" in result
        assert "initialized" in result
    
    def test_setup_rtc_name(self):
        """Test that rtc component has correct name"""
        app = FastAPI()
        
        result = setup_rtc(app)
        
        assert result["name"] == "rtc"
    
    def test_setup_rtc_routes(self):
        """Test that rtc component declares routes"""
        app = FastAPI()
        
        result = setup_rtc(app)
        
        assert isinstance(result["routes"], list)
        assert "/rtc/*" in result["routes"]
    
    def test_setup_rtc_initialized(self):
        """Test that rtc component marks as initialized"""
        app = FastAPI()
        
        result = setup_rtc(app)
        
        assert result["initialized"] is True
    
    def test_setup_rtc_with_valid_app(self):
        """Test setup_rtc with valid FastAPI app"""
        app = FastAPI()
        
        result = setup_rtc(app)
        
        assert result is not None
        assert result["name"] == "rtc"
    
    def test_setup_rtc_router_prefix(self):
        """Test that rtc router has /rtc prefix"""
        app = FastAPI()
        
        result = setup_rtc(app)
        
        # Routes should indicate /rtc prefix
        assert any("/rtc" in route for route in result["routes"])
    
    def test_setup_rtc_multiple_calls(self):
        """Test that setup_rtc can be called multiple times"""
        app1 = FastAPI()
        app2 = FastAPI()
        
        result1 = setup_rtc(app1)
        result2 = setup_rtc(app2)
        
        assert result1["name"] == result2["name"]
        assert result1["routes"] == result2["routes"]