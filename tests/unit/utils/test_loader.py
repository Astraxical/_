"""
Unit tests for utils/loader.py
Tests for resource loading and path validation utilities
"""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import os
import sys

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))

from utils.loader import (
    validate_path,
    resolve_template_path,
    resolve_static_path,
    get_module_resources
)


class TestValidatePath:
    """Tests for validate_path function"""
    
    def test_validate_path_within_project_root(self, tmp_path):
        """Test that paths within project root are validated"""
        with patch('utils.loader.Path.cwd') as mock_cwd:
            mock_cwd.return_value = tmp_path
            test_file = tmp_path / "test.txt"
            test_file.touch()
            
            result = validate_path(str(test_file))
            assert result is True
    
    def test_validate_path_outside_project_root(self, tmp_path):
        """Test that paths outside project root are rejected"""
        with patch('utils.loader.Path.cwd') as mock_cwd:
            project_root = tmp_path / "project"
            project_root.mkdir()
            mock_cwd.return_value = project_root
            
            outside_path = tmp_path / "outside.txt"
            result = validate_path(str(outside_path))
            assert result is False
    
    def test_validate_path_with_directory_traversal(self, tmp_path):
        """Test that directory traversal attempts are blocked"""
        with patch('utils.loader.Path.cwd') as mock_cwd:
            mock_cwd.return_value = tmp_path
            
            # Try to escape using ../
            traversal_path = str(tmp_path / "subdir" / ".." / ".." / "etc" / "passwd")
            result = validate_path(traversal_path)
            # This should fail because it resolves outside the project root
            assert result is False
    
    def test_validate_path_with_symlink(self, tmp_path):
        """Test path validation with symlinks"""
        with patch('utils.loader.Path.cwd') as mock_cwd:
            mock_cwd.return_value = tmp_path
            
            real_file = tmp_path / "real.txt"
            real_file.touch()
            
            result = validate_path(str(real_file))
            assert result is True
    
    def test_validate_path_nonexistent_path(self, tmp_path):
        """Test validation of non-existent but safe paths"""
        with patch('utils.loader.Path.cwd') as mock_cwd:
            mock_cwd.return_value = tmp_path
            
            nonexistent = tmp_path / "does_not_exist.txt"
            result = validate_path(str(nonexistent))
            assert result is True  # Path is within root, even if doesn't exist


class TestResolveTemplatePath:
    """Tests for resolve_template_path function"""
    
    def test_resolve_template_path_module_specific(self, tmp_path):
        """Test resolving module-specific template"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            
            # Module template exists
            def exists_side_effect(path):
                return "modules/forums/templates" in path
            mock_exists.side_effect = exists_side_effect
            
            result = resolve_template_path("index.html", "forums")
            assert result == "modules/forums/templates/index.html"
    
    def test_resolve_template_path_global_fallback(self, tmp_path):
        """Test fallback to global template when module template doesn't exist"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            
            # Only global template exists
            def exists_side_effect(path):
                return "templates/" in path and "modules/" not in path
            mock_exists.side_effect = exists_side_effect
            
            result = resolve_template_path("base.html", "forums")
            assert result == "templates/base.html"
    
    def test_resolve_template_path_not_found(self, tmp_path):
        """Test when template is not found anywhere"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            mock_exists.return_value = False
            
            result = resolve_template_path("nonexistent.html", "forums")
            assert result is None
    
    def test_resolve_template_path_absolute_path(self, tmp_path):
        """Test resolving absolute template path"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            mock_exists.return_value = True
            
            abs_path = "/absolute/path/template.html"
            result = resolve_template_path(abs_path)
            assert result == abs_path
    
    def test_resolve_template_path_invalid_path(self, tmp_path):
        """Test rejection of invalid paths"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = False
            
            result = resolve_template_path("/etc/passwd")
            assert result is None
    
    def test_resolve_template_path_no_module(self, tmp_path):
        """Test resolving template without module specification"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            mock_exists.return_value = True
            
            result = resolve_template_path("index.html")
            assert result == "templates/index.html"


class TestResolveStaticPath:
    """Tests for resolve_static_path function"""
    
    def test_resolve_static_path_module_specific(self, tmp_path):
        """Test resolving module-specific static asset"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            
            # Module static exists
            def exists_side_effect(path):
                return "modules/forums/static" in path
            mock_exists.side_effect = exists_side_effect
            
            result = resolve_static_path("css/style.css", "forums")
            assert result == "modules/forums/static/css/style.css"
    
    def test_resolve_static_path_global_fallback(self, tmp_path):
        """Test fallback to global static when module static doesn't exist"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            
            # Only global static exists
            def exists_side_effect(path):
                return "static/" in path and "modules/" not in path
            mock_exists.side_effect = exists_side_effect
            
            result = resolve_static_path("js/main.js", "forums")
            assert result == "static/js/main.js"
    
    def test_resolve_static_path_not_found(self, tmp_path):
        """Test when static asset is not found"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            mock_exists.return_value = False
            
            result = resolve_static_path("nonexistent.js", "forums")
            assert result is None
    
    def test_resolve_static_path_no_module(self, tmp_path):
        """Test resolving static asset without module specification"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.os.path.exists') as mock_exists, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = True
            mock_exists.return_value = True
            
            result = resolve_static_path("css/main.css")
            assert result == "static/css/main.css"
    
    def test_resolve_static_path_invalid_path(self, tmp_path):
        """Test rejection of invalid static paths"""
        with patch('utils.loader.Path.cwd') as mock_cwd, \
             patch('utils.loader.validate_path') as mock_validate:
            
            mock_cwd.return_value = tmp_path
            mock_validate.return_value = False
            
            result = resolve_static_path("../../etc/passwd", "forums")
            assert result is None


class TestGetModuleResources:
    """Tests for get_module_resources function"""
    
    def test_get_module_resources_complete_module(self, tmp_path):
        """Test getting resources for a complete module with all directories"""
        module_path = tmp_path / "modules" / "forums"
        module_path.mkdir(parents=True)
        (module_path / "templates").mkdir()
        (module_path / "static").mkdir()
        (module_path / "data").mkdir()
        (module_path / "routes").mkdir()
        
        with patch('utils.loader.Path') as mock_path_class:
            mock_path = MagicMock()
            mock_path.exists.return_value = True
            mock_path.__truediv__ = lambda self, other: tmp_path / "modules" / "forums" / other
            
            # Setup the path behavior
            def path_side_effect(arg):
                result = tmp_path / arg
                result.exists = lambda: True
                result.__truediv__ = lambda self, other: tmp_path / arg / other
                return result
            
            mock_path_class.side_effect = path_side_effect
            
            with patch('utils.loader.Path', return_value=module_path):
                result = get_module_resources("forums")
                
                assert result['templates'] == str(module_path / "templates")
                assert result['static'] == str(module_path / "static")
                assert result['data'] == str(module_path / "data")
                assert result['routes'] == str(module_path / "routes")
    
    def test_get_module_resources_partial_module(self, tmp_path):
        """Test getting resources for a module with only some directories"""
        module_path = tmp_path / "modules" / "rtc"
        module_path.mkdir(parents=True)
        (module_path / "templates").mkdir()
        # No static, data, or routes directories
        
        with patch('pathlib.Path') as mock_path:
            mock_instance = MagicMock()
            mock_instance.exists.return_value = True
            
            # Mock the subdirectories
            mock_templates = MagicMock()
            mock_templates.exists.return_value = True
            mock_static = MagicMock()
            mock_static.exists.return_value = False
            mock_data = MagicMock()
            mock_data.exists.return_value = False
            mock_routes = MagicMock()
            mock_routes.exists.return_value = False
            
            def truediv(self, other):
                if other == "templates":
                    return mock_templates
                elif other == "static":
                    return mock_static
                elif other == "data":
                    return mock_data
                elif other == "routes":
                    return mock_routes
            
            mock_instance.__truediv__ = truediv
            mock_instance.__str__ = lambda self: str(module_path)
            mock_templates.__str__ = lambda self: str(module_path / "templates")
            
            mock_path.return_value = mock_instance
            
            result = get_module_resources("rtc")
            
            assert result['templates'] == str(module_path / "templates")
            assert result['static'] is None
            assert result['data'] is None
            assert result['routes'] is None
    
    def test_get_module_resources_nonexistent_module(self, tmp_path):
        """Test error handling for non-existent module"""
        with patch('pathlib.Path') as mock_path:
            mock_instance = MagicMock()
            mock_instance.exists.return_value = False
            mock_path.return_value = mock_instance
            
            with pytest.raises(ValueError, match="Module .* does not exist"):
                get_module_resources("nonexistent")
    
    def test_get_module_resources_empty_module(self, tmp_path):
        """Test getting resources for a module with no resource directories"""
        module_path = tmp_path / "modules" / "empty"
        module_path.mkdir(parents=True)
        
        with patch('pathlib.Path') as mock_path:
            mock_instance = MagicMock()
            mock_instance.exists.return_value = True
            
            # All subdirectories don't exist
            mock_sub = MagicMock()
            mock_sub.exists.return_value = False
            mock_instance.__truediv__ = lambda self, other: mock_sub
            
            mock_path.return_value = mock_instance
            
            result = get_module_resources("empty")
            
            assert result['templates'] is None
            assert result['static'] is None
            assert result['data'] is None
            assert result['routes'] is None