"""
Unit tests for modules/admin/routes/modules.py
Tests for module management routes
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestGetModulesRoute:
    """Tests for get_modules route"""
    
    def test_get_modules_returns_dict(self):
        """Test that get_modules returns a dictionary"""
        from modules.admin.routes.modules import get_modules
        
        result = get_modules()
        
        assert isinstance(result, dict)
    
    def test_get_modules_has_message(self):
        """Test that response includes a message"""
        from modules.admin.routes.modules import get_modules
        
        result = get_modules()
        
        assert "message" in result
        assert isinstance(result["message"], str)
    
    def test_get_modules_has_modules_list(self):
        """Test that response includes modules list"""
        from modules.admin.routes.modules import get_modules
        
        result = get_modules()
        
        assert "modules" in result
        assert isinstance(result["modules"], list)
    
    def test_get_modules_empty_list(self):
        """Test that modules list is empty (placeholder implementation)"""
        from modules.admin.routes.modules import get_modules
        
        result = get_modules()
        
        # Current implementation returns empty list
        assert result["modules"] == []


class TestToggleModuleRoute:
    """Tests for toggle_module route"""
    
    def test_toggle_module_returns_dict(self):
        """Test that toggle_module returns a dictionary"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("forums")
        
        assert isinstance(result, dict)
    
    def test_toggle_module_includes_status(self):
        """Test that response includes status"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("forums")
        
        assert "status" in result
        assert result["status"] == "success"
    
    def test_toggle_module_includes_message(self):
        """Test that response includes message with module name"""
        from modules.admin.routes.modules import toggle_module
        
        module_name = "forums"
        result = toggle_module(module_name)
        
        assert "message" in result
        assert module_name in result["message"]
    
    def test_toggle_module_various_names(self):
        """Test toggling various module names"""
        from modules.admin.routes.modules import toggle_module
        
        test_modules = ["forums", "rtc", "admin", "template"]
        
        for module_name in test_modules:
            result = toggle_module(module_name)
            
            assert result["status"] == "success"
            assert module_name in result["message"]
    
    def test_toggle_module_with_special_characters(self):
        """Test toggling module with special characters in name"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("test-module_123")
        
        assert "test-module_123" in result["message"]
        assert result["status"] == "success"
    
    def test_toggle_module_empty_name(self):
        """Test toggling module with empty name"""
        from modules.admin.routes.modules import toggle_module
        
        result = toggle_module("")
        
        # Should still return success (no validation in current implementation)
        assert result["status"] == "success"


class TestModulesRouterConfiguration:
    """Tests for router configuration"""
    
    def test_router_exists(self):
        """Test that router is properly defined"""
        from modules.admin.routes.modules import router
        from fastapi import APIRouter
        
        assert router is not None
        assert isinstance(router, APIRouter)


class TestModulesRoutesEdgeCases:
    """Tests for edge cases in module management routes"""
    
    def test_toggle_module_case_sensitivity(self):
        """Test that module names are handled as provided"""
        from modules.admin.routes.modules import toggle_module
        
        result1 = toggle_module("Forums")
        result2 = toggle_module("forums")
        
        # Both should succeed
        assert result1["status"] == "success"
        assert result2["status"] == "success"
        assert "Forums" in result1["message"]
        assert "forums" in result2["message"]
    
    def test_get_modules_consistent_response(self):
        """Test that get_modules returns consistent response"""
        from modules.admin.routes.modules import get_modules
        
        result1 = get_modules()
        result2 = get_modules()
        
        assert result1 == result2
    
    def test_toggle_module_idempotent(self):
        """Test that toggling same module twice returns same result"""
        from modules.admin.routes.modules import toggle_module
        
        result1 = toggle_module("forums")
        result2 = toggle_module("forums")
        
        assert result1["status"] == result2["status"]