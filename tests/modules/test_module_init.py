"""
Tests for module __init__.py files
"""
import pytest
from fastapi import APIRouter


def test_admin_module_exports_router():
    """Test that admin module exports a router"""
    from modules.admin import router
    
    assert isinstance(router, APIRouter)
    assert router.prefix == "/admin"


def test_admin_module_get_module_info():
    """Test admin module get_module_info function"""
    from modules.admin import get_module_info
    
    info = get_module_info()
    
    assert isinstance(info, dict)
    assert info["name"] == "admin"
    assert info["routes"] == ["/admin/*"]
    assert info["local_data_path"] == "modules/admin/data"


def test_forums_module_exports_router():
    """Test that forums module exports a router"""
    from modules.forums import router
    
    assert isinstance(router, APIRouter)
    assert router.prefix == "/forums"


def test_forums_module_get_module_info():
    """Test forums module get_module_info function"""
    from modules.forums import get_module_info
    
    info = get_module_info()
    
    assert isinstance(info, dict)
    assert info["name"] == "forums"
    assert info["routes"] == ["/forums/*"]
    assert info["local_data_path"] == "modules/forums/data"


def test_rtc_module_exports_router():
    """Test that rtc module exports a router"""
    from modules.rtc import router
    
    assert isinstance(router, APIRouter)
    assert router.prefix == "/rtc"


def test_rtc_module_get_module_info():
    """Test rtc module get_module_info function"""
    from modules.rtc import get_module_info
    
    info = get_module_info()
    
    assert isinstance(info, dict)
    assert info["name"] == "rtc"
    assert info["routes"] == ["/rtc/*"]
    assert info["local_data_path"] == "modules/rtc/data"


def test_all_modules_have_unique_prefixes():
    """Test that all modules have unique route prefixes"""
    from modules.admin import router as admin_router
    from modules.forums import router as forums_router
    from modules.rtc import router as rtc_router
    
    prefixes = [
        admin_router.prefix,
        forums_router.prefix,
        rtc_router.prefix
    ]
    
    # All prefixes should be unique
    assert len(prefixes) == len(set(prefixes))


def test_all_modules_have_consistent_info_structure():
    """Test that all modules return consistent info structure"""
    from modules.admin import get_module_info as admin_info
    from modules.forums import get_module_info as forums_info
    from modules.rtc import get_module_info as rtc_info
    
    infos = [admin_info(), forums_info(), rtc_info()]
    
    required_keys = ["name", "routes", "local_data_path"]
    
    for info in infos:
        for key in required_keys:
            assert key in info, f"Missing key {key} in module info"


def test_module_routers_are_different_instances():
    """Test that each module has its own router instance"""
    from modules.admin import router as admin_router
    from modules.forums import router as forums_router
    from modules.rtc import router as rtc_router
    
    assert admin_router is not forums_router
    assert forums_router is not rtc_router
    assert admin_router is not rtc_router