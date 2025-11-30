"""
Comprehensive unit tests for utils/loader.py
Tests for updated loader functionality including alter system integration
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add codebase to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "codebase"))


class TestResolveTemplatePathWithAlterSystem:
    """Tests for resolve_template_path with alter system integration"""
    
    @patch('utils.loader.TemplateEngine')
    @patch('utils.loader.os.path.exists')
    @patch('utils.loader.validate_path')
    def test_resolves_alter_specific_template(self, mock_validate, mock_exists, mock_engine):
        """Test that alter-specific templates are resolved"""
        from utils.loader import resolve_template_path
        
        mock_engine_instance = MagicMock()
        mock_engine_instance.current_alter = "seles"
        mock_engine.return_value = mock_engine_instance
        
        mock_validate.return_value = True
        mock_exists.return_value = True
        
        result = resolve_template_path("index.html")
        
        assert result is not None
        assert "seles" in result
    
    @patch('utils.loader.TemplateEngine')
    @patch('utils.loader.os.path.exists')
    @patch('utils.loader.validate_path')
    def test_falls_back_to_global_template(self, mock_validate, mock_exists, mock_engine):
        """Test fallback to global template when alter template doesn't exist"""
        from utils.loader import resolve_template_path
        
        mock_engine_instance = MagicMock()
        mock_engine_instance.current_alter = "seles"
        mock_engine.return_value = mock_engine_instance
        
        mock_validate.return_value = True
        # First call (alter-specific) returns False, second (global) returns True
        mock_exists.side_effect = [False, True]
        
        result = resolve_template_path("index.html")
        
        assert result is not None
        assert "global" in result
    
    @patch('utils.loader.TemplateEngine')
    @patch('utils.loader.os.path.exists')
    @patch('utils.loader.validate_path')
    def test_handles_template_engine_import_error(self, mock_validate, mock_exists, mock_engine):
        """Test graceful handling when TemplateEngine can't be imported"""
        from utils.loader import resolve_template_path
        
        mock_engine.side_effect = ImportError("Cannot import")
        mock_validate.return_value = True
        mock_exists.return_value = True
        
        # Should fall back to standard resolution
        result = resolve_template_path("index.html")
        
        # Should still resolve or return None gracefully
        assert result is None or isinstance(result, str)
    
    @patch('utils.loader.TemplateEngine')
    @patch('utils.loader.os.path.exists')
    @patch('utils.loader.validate_path')
    def test_skips_alter_templates_when_global_is_fronting(self, mock_validate, mock_exists, mock_engine):
        """Test that alter-specific lookup is skipped when global is fronting"""
        from utils.loader import resolve_template_path
        
        mock_engine_instance = MagicMock()
        mock_engine_instance.current_alter = "global"
        mock_engine.return_value = mock_engine_instance
        
        mock_validate.return_value = True
        mock_exists.return_value = True
        
        result = resolve_template_path("index.html")
        
        # Should resolve to regular template path
        assert result is not None
    
    @patch('utils.loader.TemplateEngine')
    @patch('utils.loader.os.path.exists')
    @patch('utils.loader.validate_path')
    def test_module_specific_template_takes_precedence(self, mock_validate, mock_exists, mock_engine):
        """Test that module-specific templates take precedence over alter templates"""
        from utils.loader import resolve_template_path
        
        mock_engine_instance = MagicMock()
        mock_engine_instance.current_alter = "seles"
        mock_engine.return_value = mock_engine_instance
        
        mock_validate.return_value = True
        mock_exists.return_value = True
        
        result = resolve_template_path("index.html", module_name="forums")
        
        assert result is not None
        assert "forums" in result


class TestResolveTemplatePathEdgeCases:
    """Tests for edge cases in resolve_template_path"""
    
    @patch('utils.loader.validate_path')
    @patch('utils.loader.os.path.exists')
    def test_absolute_path_outside_project(self, mock_exists, mock_validate):
        """Test that absolute paths outside project are rejected"""
        from utils.loader import resolve_template_path
        
        mock_validate.return_value = False
        mock_exists.return_value = True
        
        result = resolve_template_path("/etc/passwd")
        
        assert result is None
    
    @patch('utils.loader.validate_path')
    @patch('utils.loader.os.path.exists')
    def test_relative_path_traversal_blocked(self, mock_exists, mock_validate):
        """Test that path traversal attempts are blocked"""
        from utils.loader import resolve_template_path
        
        mock_validate.return_value = False
        
        result = resolve_template_path("../../../etc/passwd")
        
        # Should be blocked by validate_path
        assert result is None or not result.startswith("/etc")
    
    @patch('utils.loader.TemplateEngine')
    @patch('utils.loader.validate_path')
    @patch('utils.loader.os.path.exists')
    def test_nonexistent_template(self, mock_exists, mock_validate, mock_engine):
        """Test handling of nonexistent templates"""
        from utils.loader import resolve_template_path
        
        mock_engine_instance = MagicMock()
        mock_engine_instance.current_alter = "seles"
        mock_engine.return_value = mock_engine_instance
        
        mock_validate.return_value = True
        mock_exists.return_value = False
        
        result = resolve_template_path("nonexistent.html")
        
        assert result is None


class TestGetModuleResourcesEnhanced:
    """Enhanced tests for get_module_resources"""
    
    @patch('utils.loader.Path')
    def test_raises_error_for_nonexistent_module(self, mock_path):
        """Test that ValueError is raised for nonexistent modules"""
        from utils.loader import get_module_resources
        
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        with pytest.raises(ValueError, match="does not exist"):
            get_module_resources("nonexistent_module")
    
    @patch('utils.loader.Path')
    def test_returns_all_resource_types(self, mock_path):
        """Test that all resource types are checked"""
        from utils.loader import get_module_resources
        
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        
        # Mock subdirectories
        templates_dir = MagicMock()
        templates_dir.exists.return_value = True
        static_dir = MagicMock()
        static_dir.exists.return_value = True
        data_dir = MagicMock()
        data_dir.exists.return_value = True
        routes_dir = MagicMock()
        routes_dir.exists.return_value = True
        
        mock_path_instance.__truediv__.side_effect = [
            templates_dir, static_dir, data_dir, routes_dir
        ]
        
        result = get_module_resources("test_module")
        
        assert "templates" in result
        assert "static" in result
        assert "data" in result
        assert "routes" in result
    
    @patch('utils.loader.Path')
    def test_returns_none_for_missing_resources(self, mock_path):
        """Test that None is returned for missing resource directories"""
        from utils.loader import get_module_resources
        
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        
        # All subdirectories don't exist
        subdir = MagicMock()
        subdir.exists.return_value = False
        mock_path_instance.__truediv__.return_value = subdir
        
        result = get_module_resources("test_module")
        
        assert result["templates"] is None
        assert result["static"] is None
        assert result["data"] is None
        assert result["routes"] is None