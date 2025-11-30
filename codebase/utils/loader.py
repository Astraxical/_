"""
Utility functions for loading module resources
Validates local/global paths and loads module resources
"""
import os
from pathlib import Path
from typing import Optional, List


def validate_path(path: str) -> bool:
    """
    Determine whether the given path is located inside the project root directory.
    
    Parameters:
        path (str): Path to validate; may be absolute or relative.
    
    Returns:
        bool: True if the resolved path is inside the project root, False otherwise.
    """
    # Convert to Path object for easier manipulation
    path_obj = Path(path).resolve()
    
    # Get the project root directory
    project_root = Path.cwd().resolve()
    
    # Check if the path is within the project root
    try:
        path_obj.relative_to(project_root)
        return True
    except ValueError:
        # Path is outside the project root
        return False


def resolve_template_path(template_name: str, module_name: Optional[str] = None) -> Optional[str]:
    """
    Resolve a template filename to an existing, safe filesystem path.

    Checks a module-specific templates directory first (if module_name is provided), then the global templates directory, and also accepts an absolute path when it resides inside the project root. Only returns a path that exists and passes the module's path-safety checks.

    Parameters:
        template_name (str): Template filename or absolute path.
        module_name (Optional[str]): Module name to prefer a module-scoped templates directory.

    Returns:
        Optional[str]: The resolved filesystem path to the template if found and valid, or `None` if not found or not permitted.
    """
    # First, check if it's an absolute path (but still validate)
    if template_name.startswith('/'):
        if validate_path(template_name):
            return template_name if os.path.exists(template_name) else None
        return None

    # If module is specified, check module's templates first
    if module_name:
        module_template_path = f"modules/{module_name}/templates/{template_name}"
        if validate_path(module_template_path) and os.path.exists(module_template_path):
            return module_template_path

    # Then check global templates
    global_template_path = f"templates/{template_name}"
    if validate_path(global_template_path) and os.path.exists(global_template_path):
        return global_template_path

    # Check for alter-specific templates (requires importing template engine)
    try:
        from modules.alter.engine import TemplateEngine
        template_engine = TemplateEngine()

        # Check alter-specific templates
        if template_engine.current_alter and template_engine.current_alter != "global":
            alter_template_path = f"modules/alter/templates/{template_engine.current_alter}/{template_name}"
            if validate_path(alter_template_path) and os.path.exists(alter_template_path):
                return alter_template_path

        # Then check global templates in the template module
        global_template_path = f"modules/alter/templates/global/{template_name}"
        if validate_path(global_template_path) and os.path.exists(global_template_path):
            return global_template_path

    except ImportError:
        # If template engine isn't available, just continue with regular resolution
        pass

    return None


def resolve_static_path(static_name: str, module_name: Optional[str] = None) -> Optional[str]:
    """
    Resolve the filesystem path of a static asset, preferring a module-specific file before falling back to the global static directory.
    
    Parameters:
        static_name (str): The filename or relative path of the static asset to locate (e.g., 'css/app.css' or 'img/logo.png').
        module_name (Optional[str]): Optional module name to search under 'modules/{module_name}/static' first.
    
    Returns:
        Optional[str]: The validated existing filesystem path to the asset if found and located inside the project root, `None` if not found.
    """
    # If module is specified, check module's static files first
    if module_name:
        module_static_path = f"modules/{module_name}/static/{static_name}"
        if validate_path(module_static_path) and os.path.exists(module_static_path):
            return module_static_path
    
    # Then check global static files
    global_static_path = f"static/{static_name}"
    if validate_path(global_static_path) and os.path.exists(global_static_path):
        return global_static_path
    
    return None


def get_module_resources(module_name: str) -> dict:
    """
    Return the filesystem paths for a module's resource directories.
    
    Parameters:
        module_name (str): Name of the module to inspect.
    
    Returns:
        dict: Mapping with keys 'templates', 'static', 'data', and 'routes'. Each value is the string path to the corresponding subdirectory if it exists, or `None` if that resource directory is absent.
    
    Raises:
        ValueError: If the module directory "modules/{module_name}" does not exist.
    """
    module_path = Path(f"modules/{module_name}")
    
    if not module_path.exists():
        raise ValueError(f"Module {module_name} does not exist")
    
    resources = {
        'templates': None,
        'static': None,
        'data': None,
        'routes': None
    }
    
    # Check for each resource type
    if (module_path / "templates").exists():
        resources['templates'] = str(module_path / "templates")
    
    if (module_path / "static").exists():
        resources['static'] = str(module_path / "static")
    
    if (module_path / "data").exists():
        resources['data'] = str(module_path / "data")
    
    if (module_path / "routes").exists():
        resources['routes'] = str(module_path / "routes")
    
    return resources