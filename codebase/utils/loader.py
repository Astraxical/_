"""
Utility functions for loading module resources
Validates local/global paths and loads module resources
"""
import os
from pathlib import Path
from typing import Optional, List


def validate_path(path: str) -> bool:
    """
    Validates if a path is safe to access (prevents directory traversal)
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
    Resolves a template path, checking in module-specific then global locations
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
    
    # Finally, check alter-specific templates
    # This would require access to the template engine to know the current alter
    # For now, return None if not found in module or global locations
    return None


def resolve_static_path(static_name: str, module_name: Optional[str] = None) -> Optional[str]:
    """
    Resolves a static asset path, checking in module-specific then global locations
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
    Gets the resource paths for a specific module
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