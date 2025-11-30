"""
Template Module - Manages the alter system for dynamic UI changes
"""
from fastapi import Request
from fastapi.templating import Jinja2Templates
from typing import Dict, Any, Optional
import csv
import os
from pathlib import Path


class AlterManager:
    """
    Manages the alter system to dynamically change the UI based on which alter is fronting.
    """
    
    def __init__(self, alters_csv_path: str = "modules/template/data/alters.csv"):
        self.alters_csv_path = Path(alters_csv_path)
        self._ensure_alters_file_exists()
    
    def _ensure_alters_file_exists(self):
        """Ensure the alters CSV file exists with default values."""
        if not self.alters_csv_path.parent.exists():
            self.alters_csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.alters_csv_path.exists():
            # Default to seles as fronting, others inactive
            with open(self.alters_csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['alter', 'fronting'])
                writer.writerow(['seles', '1'])
                writer.writerow(['dexen', '0'])
                writer.writerow(['yuki', '0'])
    
    def get_current_alter(self) -> str:
        """Get the currently fronting alter."""
        try:
            with open(self.alters_csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('fronting', '0') == '1':
                        return row['alter']
        except (FileNotFoundError, KeyError):
            pass
        return "global"  # fallback
    
    def set_fronting_alter(self, alter_name: str) -> bool:
        """Set the specified alter as fronting."""
        try:
            alters = []
            with open(self.alters_csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    new_row = dict(row)
                    new_row['fronting'] = '1' if new_row['alter'] == alter_name else '0'
                    alters.append(new_row)
            
            # Write updated data back
            with open(self.alters_csv_path, 'w', newline='') as f:
                fieldnames = ['alter', 'fronting']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(alters)
            return True
        except Exception:
            return False
    
    def get_alters_status(self) -> Dict[str, bool]:
        """Get the status of all alters."""
        status = {}
        try:
            with open(self.alters_csv_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    status[row['alter']] = row.get('fronting', '0') == '1'
        except FileNotFoundError:
            # Return default status if file doesn't exist
            status = {"seles": True, "dexen": False, "yuki": False}
        return status


# Global instance of AlterManager
alter_manager = AlterManager()


def find_template_for_alter(template_name: str, alter_name: Optional[str] = None) -> tuple:
    """
    Find a template file for the given alter following the priority order.
    
    Returns a tuple of (found_path, directory_path) or (None, None) if not found.
    """
    if not alter_name:
        alter_name = alter_manager.get_current_alter()
    
    # Define template search paths prioritizing the current alter
    template_paths = []
    
    # First, try alter-specific templates
    if alter_name and alter_name != "global":
        alter_template_dir = f"modules/template/templates/{alter_name}"
        alter_template_path = f"{alter_template_dir}/{template_name}"
        if Path(alter_template_path).exists():
            return (alter_template_path, alter_template_dir)
    
    # Then try global alter templates (for shared alter content)
    global_alter_template_dir = "modules/template/templates/global"
    global_alter_template_path = f"{global_alter_template_dir}/{template_name}"
    if Path(global_alter_template_path).exists():
        return (global_alter_template_path, global_alter_template_dir)
    
    # Finally, try the global templates
    global_template_dir = "templates"
    global_template_path = f"{global_template_dir}/{template_name}"
    if Path(global_template_path).exists():
        return (global_template_path, global_template_dir)
    
    # Template not found
    return (None, None)


def get_template_context(request: Request) -> Dict[str, Any]:
    """
    Generate template context with current alter information.
    
    Parameters:
        request (Request): The incoming HTTP request
    
    Returns:
        Dict[str, Any]: Context dictionary with alter information
    """
    current_alter = alter_manager.get_current_alter()
    alters_status = alter_manager.get_alters_status()
    
    return {
        "request": request,
        "current_alter": current_alter,
        "alters_status": alters_status
    }


def render_alter_template(request: Request, template_name: str, **kwargs) -> Any:
    """
    Render a template with the appropriate context for the current alter.

    Parameters:
        request (Request): The incoming HTTP request
        template_name (str): Name of the template to render
        **kwargs: Additional context variables

    Returns:
        Any: Rendered template response
    """
    # Find the appropriate template file and directory
    template_path, template_dir = find_template_for_alter(template_name)

    if template_path is None:
        # If template not found, raise an error
        raise ValueError(f"Template {template_name} not found for any alter")

    # Create Jinja2Templates instance with the correct directory
    templates = Jinja2Templates(directory=template_dir)

    # Get the base context with alter information
    context = get_template_context(request)

    # Add any additional context
    context.update(kwargs)

    return templates.TemplateResponse(template_name, context)


# Import the routers to make them accessible when the module is imported
from .routes.switcher import router as switcher_router
from .routes.api import router as api_router