"""
Unit tests for utils/loader.py
"""
import pytest
import os
import tempfile
from pathlib import Path
from utils.loader import (
    validate_path,
    resolve_template_path,
    resolve_static_path,
    get_module_resources
)


class TestValidatePath:
    """Test path validation function"""
    
    def test_validate_path_within_project(self, tmp_path, monkeypatch):
        """Test that paths within project are valid"""
        monkeypatch.chdir(tmp_path)
        test_file = tmp_path / "test.txt"
        test_file.touch()
        
        assert validate_path(str(test_file))
    
    def test_validate_path_relative(self, tmp_path, monkeypatch):
        """Test that relative paths within project are valid"""
        monkeypatch.chdir(tmp_path)
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        
        assert validate_path("subdir")
    
    def test_validate_path_outside_project(self, tmp_path, monkeypatch):
        """Test that paths outside project are invalid"""
        monkeypatch.chdir(tmp_path)
        outside_path = tmp_path.parent / "outside.txt"
        
        assert not validate_path(str(outside_path))
    
    def test_validate_path_directory_traversal(self, tmp_path, monkeypatch):
        """Test that directory traversal attempts are blocked"""
        monkeypatch.chdir(tmp_path)
        
        assert not validate_path("../../etc/passwd")
    
    def test_validate_path_absolute_outside(self, tmp_path, monkeypatch):
        """Test that absolute paths outside project are invalid"""
        monkeypatch.chdir(tmp_path)
        
        assert not validate_path("/etc/passwd")
    
    def test_validate_path_symlink_outside(self, tmp_path, monkeypatch):
        """Test that symlinks pointing outside are invalid"""
        monkeypatch.chdir(tmp_path)
        
        # Create a symlink pointing outside (if possible)
        try:
            link_path = tmp_path / "link"
            link_path.symlink_to("/etc")
            assert not validate_path(str(link_path))
        except (OSError, NotImplementedError):
            pytest.skip("Symlinks not supported on this system")
    
    def test_validate_path_nested_directories(self, tmp_path, monkeypatch):
        """Test validation of deeply nested paths"""
        monkeypatch.chdir(tmp_path)
        nested = tmp_path / "a" / "b" / "c" / "d"
        nested.mkdir(parents=True)
        
        assert validate_path(str(nested))


class TestResolveTemplatePath:
    """Test template path resolution"""
    
    def test_resolve_template_global_exists(self, tmp_path, monkeypatch):
        """Test resolving a global template that exists"""
        monkeypatch.chdir(tmp_path)
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        template_file = templates_dir / "index.html"
        template_file.write_text("<html></html>")
        
        result = resolve_template_path("index.html")
        assert result == "templates/index.html"
    
    def test_resolve_template_module_exists(self, tmp_path, monkeypatch):
        """Test resolving a module-specific template that exists"""
        monkeypatch.chdir(tmp_path)
        module_templates = tmp_path / "modules" / "forums" / "templates"
        module_templates.mkdir(parents=True)
        template_file = module_templates / "index.html"
        template_file.write_text("<html></html>")
        
        result = resolve_template_path("index.html", "forums")
        assert result == "modules/forums/templates/index.html"
    
    def test_resolve_template_module_fallback_to_global(self, tmp_path, monkeypatch):
        """Test fallback to global template when module template doesn't exist"""
        monkeypatch.chdir(tmp_path)
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        template_file = templates_dir / "base.html"
        template_file.write_text("<html></html>")
        
        result = resolve_template_path("base.html", "forums")
        assert result == "templates/base.html"
    
    def test_resolve_template_not_found(self, tmp_path, monkeypatch):
        """Test that None is returned when template doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        result = resolve_template_path("nonexistent.html")
        assert result is None
    
    def test_resolve_template_absolute_path_valid(self, tmp_path, monkeypatch):
        """Test resolving absolute path within project"""
        monkeypatch.chdir(tmp_path)
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        template_file = templates_dir / "test.html"
        template_file.write_text("<html></html>")
        
        result = resolve_template_path(str(template_file))
        assert result == str(template_file)
    
    def test_resolve_template_absolute_path_invalid(self, tmp_path, monkeypatch):
        """Test that absolute paths outside project return None"""
        monkeypatch.chdir(tmp_path)
        
        result = resolve_template_path("/etc/passwd")
        assert result is None
    
    def test_resolve_template_directory_traversal(self, tmp_path, monkeypatch):
        """Test that directory traversal in template name is blocked"""
        monkeypatch.chdir(tmp_path)
        
        result = resolve_template_path("../../etc/passwd")
        assert result is None


class TestResolveStaticPath:
    """Test static asset path resolution"""
    
    def test_resolve_static_global_exists(self, tmp_path, monkeypatch):
        """Test resolving a global static file that exists"""
        monkeypatch.chdir(tmp_path)
        static_dir = tmp_path / "static" / "css"
        static_dir.mkdir(parents=True)
        css_file = static_dir / "main.css"
        css_file.write_text("body { }")
        
        result = resolve_static_path("css/main.css")
        assert result == "static/css/main.css"
    
    def test_resolve_static_module_exists(self, tmp_path, monkeypatch):
        """Test resolving a module-specific static file that exists"""
        monkeypatch.chdir(tmp_path)
        module_static = tmp_path / "modules" / "forums" / "static" / "css"
        module_static.mkdir(parents=True)
        css_file = module_static / "forums.css"
        css_file.write_text(".forum { }")
        
        result = resolve_static_path("css/forums.css", "forums")
        assert result == "modules/forums/static/css/forums.css"
    
    def test_resolve_static_module_fallback_to_global(self, tmp_path, monkeypatch):
        """Test fallback to global static when module static doesn't exist"""
        monkeypatch.chdir(tmp_path)
        static_dir = tmp_path / "static" / "js"
        static_dir.mkdir(parents=True)
        js_file = static_dir / "htmx.min.js"
        js_file.write_text("// htmx")
        
        result = resolve_static_path("js/htmx.min.js", "forums")
        assert result == "static/js/htmx.min.js"
    
    def test_resolve_static_not_found(self, tmp_path, monkeypatch):
        """Test that None is returned when static file doesn't exist"""
        monkeypatch.chdir(tmp_path)
        
        result = resolve_static_path("css/nonexistent.css")
        assert result is None
    
    def test_resolve_static_nested_path(self, tmp_path, monkeypatch):
        """Test resolving deeply nested static paths"""
        monkeypatch.chdir(tmp_path)
        static_dir = tmp_path / "static" / "assets" / "images" / "icons"
        static_dir.mkdir(parents=True)
        icon_file = static_dir / "logo.svg"
        icon_file.write_text("<svg></svg>")
        
        result = resolve_static_path("assets/images/icons/logo.svg")
        assert result == "static/assets/images/icons/logo.svg"


class TestGetModuleResources:
    """Test module resource retrieval"""
    
    def test_get_module_resources_all_present(self, tmp_path, monkeypatch):
        """Test getting resources when all directories exist"""
        monkeypatch.chdir(tmp_path)
        module_path = tmp_path / "modules" / "forums"
        
        # Create all resource directories
        (module_path / "templates").mkdir(parents=True)
        (module_path / "static").mkdir(parents=True)
        (module_path / "data").mkdir(parents=True)
        (module_path / "routes").mkdir(parents=True)
        
        result = get_module_resources("forums")
        
        assert result['templates'] == "modules/forums/templates"
        assert result['static'] == "modules/forums/static"
        assert result['data'] == "modules/forums/data"
        assert result['routes'] == "modules/forums/routes"
    
    def test_get_module_resources_partial(self, tmp_path, monkeypatch):
        """Test getting resources when only some directories exist"""
        monkeypatch.chdir(tmp_path)
        module_path = tmp_path / "modules" / "rtc"
        
        # Create only templates and data
        (module_path / "templates").mkdir(parents=True)
        (module_path / "data").mkdir(parents=True)
        
        result = get_module_resources("rtc")
        
        assert result['templates'] == "modules/rtc/templates"
        assert result['static'] is None
        assert result['data'] == "modules/rtc/data"
        assert result['routes'] is None
    
    def test_get_module_resources_none_present(self, tmp_path, monkeypatch):
        """Test getting resources when no resource directories exist"""
        monkeypatch.chdir(tmp_path)
        module_path = tmp_path / "modules" / "empty"
        module_path.mkdir(parents=True)
        
        result = get_module_resources("empty")
        
        assert result['templates'] is None
        assert result['static'] is None
        assert result['data'] is None
        assert result['routes'] is None
    
    def test_get_module_resources_nonexistent_module(self, tmp_path, monkeypatch):
        """Test that ValueError is raised for nonexistent module"""
        monkeypatch.chdir(tmp_path)
        
        with pytest.raises(ValueError, match="Module nonexistent does not exist"):
            get_module_resources("nonexistent")
    
    def test_get_module_resources_returns_dict(self, tmp_path, monkeypatch):
        """Test that function returns a dictionary with expected keys"""
        monkeypatch.chdir(tmp_path)
        module_path = tmp_path / "modules" / "test"
        module_path.mkdir(parents=True)
        
        result = get_module_resources("test")
        
        assert isinstance(result, dict)
        assert 'templates' in result
        assert 'static' in result
        assert 'data' in result
        assert 'routes' in result