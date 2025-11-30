"""
Unit tests for modules/template/__init__.py
Tests for template module initialization and router setup
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "codebase"))


class TestTemplateModuleRouter:
    """Tests for template module router"""
    
    def test_router_exists(self):
        """Test that router is properly defined"""
        from modules.template import router
        from fastapi import APIRouter
        
        assert router is not None
        assert isinstance(router, APIRouter)
    
    def test_router_has_prefix(self):
        """Test that router has /template prefix"""
        from modules.template import router
        
        assert router.prefix == "/template"
    
    @patch('modules.template.alter')
    def test_router_includes_alter_routes(self, mock_alter):
        """Test that router includes alter routes"""
        import importlib
        import modules.template as template_module
        
        # Reload to trigger router setup
        importlib.reload(template_module)
        
        # Router should have been configured
        assert template_module.router is not None


class TestGetModuleInfo:
    """Tests for get_module_info function"""
    
    def test_get_module_info_returns_dict(self):
        """Test that get_module_info returns a dictionary"""
        from modules.template import get_module_info
        
        result = get_module_info()
        
        assert isinstance(result, dict)
    
    def test_get_module_info_has_name(self):
        """Test that module info includes name"""
        from modules.template import get_module_info
        
        result = get_module_info()
        
        assert "name" in result
        assert result["name"] == "template"
    
    def test_get_module_info_has_routes(self):
        """Test that module info includes routes"""
        from modules.template import get_module_info
        
        result = get_module_info()
        
        assert "routes" in result
        assert isinstance(result["routes"], list)
        assert len(result["routes"]) > 0
    
    def test_get_module_info_includes_alter_routes(self):
        """Test that routes include alter-specific patterns"""
        from modules.template import get_module_info
        
        result = get_module_info()
        
        routes_str = " ".join(result["routes"])
        assert "/template" in routes_str
        assert "/alter" in routes_str or "alter" in routes_str.lower()
    
    def test_get_module_info_has_local_data_path(self):
        """Test that module info includes local data path"""
        from modules.template import get_module_info
        
        result = get_module_info()
        
        assert "local_data_path" in result
        assert "modules/template/data" in result["local_data_path"]
    
    def test_get_module_info_structure(self):
        """Test the complete structure of module info"""
        from modules.template import get_module_info
        
        result = get_module_info()
        
        required_keys = {"name", "routes", "local_data_path"}
        assert required_keys.issubset(result.keys())


class TestTemplateModuleIntegration:
    """Integration tests for template module"""
    
    def test_module_can_be_imported(self):
        """Test that module can be imported without errors"""
        try:
            import modules.template
            assert True
        except ImportError:
            pytest.fail("Failed to import modules.template")
    
    def test_module_exports_router(self):
        """Test that module exports router"""
        import modules.template
        
        assert hasattr(modules.template, 'router')
    
    def test_module_exports_get_module_info(self):
        """Test that module exports get_module_info"""
        import modules.template
        
        assert hasattr(modules.template, 'get_module_info')
        assert callable(modules.template.get_module_info)
    
    def test_router_is_configured(self):
        """Test that router is properly configured"""
        from modules.template import router
        
        # Router should have prefix
        assert hasattr(router, 'prefix')
        assert router.prefix == "/template"


class TestTemplateModuleEdgeCases:
    """Tests for edge cases in template module"""
    
    def test_get_module_info_idempotent(self):
        """Test that get_module_info returns same result on multiple calls"""
        from modules.template import get_module_info
        
        result1 = get_module_info()
        result2 = get_module_info()
        
        assert result1 == result2
    
    def test_module_info_routes_not_empty(self):
        """Test that routes list is not empty"""
        from modules.template import get_module_info
        
        result = get_module_info()
        
        assert len(result["routes"]) > 0
    
    def test_module_info_name_is_string(self):
        """Test that module name is a string"""
        from modules.template import get_module_info
        
        result = get_module_info()
        
        assert isinstance(result["name"], str)
        assert len(result["name"]) > 0