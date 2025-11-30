"""
Unit tests for modules/rtc/__init__.py
"""
import pytest
from fastapi import APIRouter
from modules.rtc import router, get_module_info


class TestRTCModule:
    """Test RTC module initialization"""
    
    def test_router_exists(self):
        """Test that rtc router is exported"""
        assert router is not None
        assert isinstance(router, APIRouter)
    
    def test_router_has_prefix(self):
        """Test that rtc router has /rtc prefix"""
        assert router.prefix == "/rtc"
    
    def test_get_module_info_returns_dict(self):
        """Test that get_module_info returns a dictionary"""
        info = get_module_info()
        assert isinstance(info, dict)
    
    def test_get_module_info_structure(self):
        """Test that get_module_info returns correct structure"""
        info = get_module_info()
        
        assert "name" in info
        assert "routes" in info
        assert "local_data_path" in info
    
    def test_get_module_info_name(self):
        """Test that module name is 'rtc'"""
        info = get_module_info()
        assert info["name"] == "rtc"
    
    def test_get_module_info_routes(self):
        """Test that module declares rtc routes"""
        info = get_module_info()
        
        assert isinstance(info["routes"], list)
        assert "/rtc/*" in info["routes"]
    
    def test_get_module_info_local_data_path(self):
        """Test that module has correct data path"""
        info = get_module_info()
        assert info["local_data_path"] == "modules/rtc/data"
    
    def test_module_info_consistency(self):
        """Test that module info is consistent across calls"""
        info1 = get_module_info()
        info2 = get_module_info()
        
        assert info1 == info2
    
    def test_router_prefix_matches_routes(self):
        """Test that router prefix matches route declarations"""
        info = get_module_info()
        
        # Router prefix should be consistent with declared routes
        assert router.prefix == "/rtc"
        assert any("/rtc" in route for route in info["routes"])