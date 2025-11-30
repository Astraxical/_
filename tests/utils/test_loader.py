"""
Tests for utils/loader.py
"""
import pytest
import os
from pathlib import Path


def test_validate_path_within_project(temp_test_dir):
    """Test that paths within project root are valid"""
    from utils.loader import validate_path
    
    # Create a test file
    test_file = temp_test_dir / "test.txt"
    test_file.touch()
    
    assert validate_path(str(test_file)) == True
    assert validate_path("modules/test") == True
    assert validate_path("templates/base.html") == True


def test_validate_path_prevents_directory_traversal(temp_test_dir):
    """Test that directory traversal is prevented"""
    from utils.loader import validate_path
    
    # Try to access parent directory
    assert validate_path("../../../etc/passwd") == False
    assert validate_path("../../outside") == False


def test_validate_path_absolute_outside_project(temp_test_dir):
    """Test that absolute paths outside project are invalid"""
    from utils.loader import validate_path
    
    assert validate_path("/etc/passwd") == False
    assert validate_path("/tmp/outside") == False


def test_validate_path_relative_paths(temp_test_dir):
    """Test various relative path formats"""
    from utils.loader import validate_path
    
    # Create nested directories
    nested = temp_test_dir / "modules" / "test"
    nested.mkdir(parents=True, exist_ok=True)
    
    assert validate_path("modules/test") == True
    assert validate_path("./modules/test") == True


def test_resolve_template_path_module_first(temp_test_dir):
    """Test that module templates take precedence over global"""
    from utils.loader import resolve_template_path
    
    # Create module template
    module_templates = temp_test_dir / "modules" / "forums" / "templates"
    module_templates.mkdir(parents=True)
    module_template = module_templates / "test.html"
    module_template.write_text("module template")
    
    # Create global template
    global_templates = temp_test_dir / "templates"
    global_templates.mkdir(parents=True, exist_ok=True)
    global_template = global_templates / "test.html"
    global_template.write_text("global template")
    
    result = resolve_template_path("test.html", module_name="forums")
    
    assert result is not None
    assert "modules/forums/templates" in result


def test_resolve_template_path_fallback_to_global(temp_test_dir):
    """Test fallback to global templates when module template doesn't exist"""
    from utils.loader import resolve_template_path
    
    # Only create global template
    global_templates = temp_test_dir / "templates"
    global_templates.mkdir(parents=True, exist_ok=True)
    global_template = global_templates / "base.html"
    global_template.write_text("global template")
    
    result = resolve_template_path("base.html", module_name="forums")
    
    assert result is not None
    assert "templates/base.html" in result


def test_resolve_template_path_not_found(temp_test_dir):
    """Test that None is returned when template not found"""
    from utils.loader import resolve_template_path
    
    result = resolve_template_path("nonexistent.html", module_name="forums")
    
    assert result is None


def test_resolve_template_path_absolute_path(temp_test_dir):
    """Test handling of absolute paths"""
    from utils.loader import resolve_template_path
    
    # Create a template with absolute path
    template_file = temp_test_dir / "absolute.html"
    template_file.write_text("absolute template")
    
    result = resolve_template_path(str(template_file))
    
    assert result is not None


def test_resolve_template_path_absolute_outside_project(temp_test_dir):
    """Test that absolute paths outside project are rejected"""
    from utils.loader import resolve_template_path
    
    result = resolve_template_path("/etc/passwd")
    
    assert result is None


def test_resolve_static_path_module_first(temp_test_dir):
    """Test that module static files take precedence"""
    from utils.loader import resolve_static_path
    
    # Create module static file
    module_static = temp_test_dir / "modules" / "forums" / "static"
    module_static.mkdir(parents=True)
    module_file = module_static / "style.css"
    module_file.write_text("module style")
    
    # Create global static file
    global_static = temp_test_dir / "static"
    global_static.mkdir(parents=True, exist_ok=True)
    global_file = global_static / "style.css"
    global_file.write_text("global style")
    
    result = resolve_static_path("style.css", module_name="forums")
    
    assert result is not None
    assert "modules/forums/static" in result


def test_resolve_static_path_fallback_to_global(temp_test_dir):
    """Test fallback to global static files"""
    from utils.loader import resolve_static_path
    
    # Only create global static file
    global_static = temp_test_dir / "static"
    global_static.mkdir(parents=True, exist_ok=True)
    global_file = global_static / "main.css"
    global_file.write_text("global style")
    
    result = resolve_static_path("main.css", module_name="forums")
    
    assert result is not None
    assert "static/main.css" in result


def test_resolve_static_path_not_found(temp_test_dir):
    """Test that None is returned when static file not found"""
    from utils.loader import resolve_static_path
    
    result = resolve_static_path("nonexistent.css", module_name="forums")
    
    assert result is None


def test_get_module_resources_all_present(temp_test_dir):
    """Test getting all resources when they all exist"""
    from utils.loader import get_module_resources
    
    # Create module with all resources
    module_path = temp_test_dir / "modules" / "test_module"
    module_path.mkdir(parents=True)
    
    (module_path / "templates").mkdir()
    (module_path / "static").mkdir()
    (module_path / "data").mkdir()
    (module_path / "routes").mkdir()
    
    resources = get_module_resources("test_module")
    
    assert resources['templates'] is not None
    assert resources['static'] is not None
    assert resources['data'] is not None
    assert resources['routes'] is not None
    assert "test_module/templates" in resources['templates']
    assert "test_module/static" in resources['static']
    assert "test_module/data" in resources['data']
    assert "test_module/routes" in resources['routes']


def test_get_module_resources_partial(temp_test_dir):
    """Test getting resources when only some exist"""
    from utils.loader import get_module_resources
    
    # Create module with only some resources
    module_path = temp_test_dir / "modules" / "partial_module"
    module_path.mkdir(parents=True)
    
    (module_path / "templates").mkdir()
    (module_path / "static").mkdir()
    # Don't create data and routes
    
    resources = get_module_resources("partial_module")
    
    assert resources['templates'] is not None
    assert resources['static'] is not None
    assert resources['data'] is None
    assert resources['routes'] is None


def test_get_module_resources_nonexistent_module(temp_test_dir):
    """Test that ValueError is raised for nonexistent module"""
    from utils.loader import get_module_resources
    
    with pytest.raises(ValueError, match="Module .* does not exist"):
        get_module_resources("nonexistent_module")


def test_get_module_resources_empty_module(temp_test_dir):
    """Test getting resources from empty module directory"""
    from utils.loader import get_module_resources
    
    # Create empty module directory
    module_path = temp_test_dir / "modules" / "empty_module"
    module_path.mkdir(parents=True)
    
    resources = get_module_resources("empty_module")
    
    assert resources['templates'] is None
    assert resources['static'] is None
    assert resources['data'] is None
    assert resources['routes'] is None


def test_resolve_template_path_without_module_name(temp_test_dir):
    """Test resolving template path without specifying module"""
    from utils.loader import resolve_template_path
    
    # Create only global template
    global_templates = temp_test_dir / "templates"
    global_templates.mkdir(parents=True, exist_ok=True)
    global_template = global_templates / "index.html"
    global_template.write_text("global index")
    
    result = resolve_template_path("index.html")
    
    assert result is not None
    assert "templates/index.html" in result


def test_resolve_static_path_without_module_name(temp_test_dir):
    """Test resolving static path without specifying module"""
    from utils.loader import resolve_static_path
    
    # Create only global static file
    global_static = temp_test_dir / "static"
    global_static.mkdir(parents=True, exist_ok=True)
    global_file = global_static / "app.js"
    global_file.write_text("global js")
    
    result = resolve_static_path("app.js")
    
    assert result is not None
    assert "static/app.js" in result


def test_validate_path_with_dots_in_name(temp_test_dir):
    """Test that paths with dots in filename are valid"""
    from utils.loader import validate_path
    
    # Create file with dots
    test_file = temp_test_dir / "file.test.html"
    test_file.touch()
    
    assert validate_path(str(test_file)) == True
    assert validate_path("templates/base.min.css") == True


def test_resolve_template_nested_paths(temp_test_dir):
    """Test resolving nested template paths"""
    from utils.loader import resolve_template_path
    
    # Create nested template
    nested_path = temp_test_dir / "templates" / "errors"
    nested_path.mkdir(parents=True)
    nested_template = nested_path / "404.html"
    nested_template.write_text("error page")
    
    result = resolve_template_path("errors/404.html")
    
    assert result is not None
    assert "templates/errors/404.html" in result