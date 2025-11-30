"""
Template Engine - Handles alter-based template rendering
"""
import csv
import os
from typing import Dict, Any, Optional
from pathlib import Path
from fastapi.templating import Jinja2Templates
from fastapi import Request


class TemplateEngine:
    """
    Manages template rendering with alter-specific overrides.
    
    The engine maintains a mapping of which alter is currently 'fronting' (active),
    and provides template rendering that can vary based on the current alter.
    Templates are resolved with the following priority:
    1. Current alter's templates (e.g., modules/alter/templates/seles/index.html)
    2. Global templates (e.g., modules/alter/templates/global/index.html)
    3. Standard global templates (e.g., templates/index.html)
    """
    
    def __init__(self):
        self.alters_status: Dict[str, bool] = {}
        self.current_alter: str = "global"
        self._load_alters_status()
        self._setup_templates()
        
    def _load_alters_status(self):
        """Load alter status from CSV file."""
        alters_csv_path = Path("modules/alter/data/alters.csv")
        
        # Create default CSV if it doesn't exist
        if not alters_csv_path.exists():
            alters_csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(alters_csv_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['name', 'is_fronting'])
                writer.writerow(['seles', '1'])
                writer.writerow(['dexen', '0'])
                writer.writerow(['yuki', '0'])
        
        # Read the CSV file to populate alters_status
        with open(alters_csv_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                is_fronting = row['is_fronting'].lower() in ('1', 'true', 'yes', 'on')
                self.alters_status[row['name']] = is_fronting
                # Set the current alter if it's fronting
                if is_fronting:
                    self.current_alter = row['name']
    
    def _setup_templates(self):
        """Set up Jinja2 template environment with appropriate search paths."""
        # Determine template search paths based on current alter
        template_paths = []
        
        # Add alter-specific templates if current alter isn't global
        if self.current_alter != "global":
            alter_template_path = f"modules/alter/templates/{self.current_alter}"
            if os.path.exists(alter_template_path):
                template_paths.append(alter_template_path)

        # Add global templates as fallback
        global_template_path = "modules/alter/templates/global"
        if os.path.exists(global_template_path):
            template_paths.append(global_template_path)
            
        # Add regular global templates as final fallback
        template_paths.append("templates")
        
        self.templates = Jinja2Templates(directory=template_paths)
    
    def render(self, template_name: str, request: Request, **context) -> Any:
        """
        Render a template with the current context and alter information.
        
        Args:
            template_name: Name of the template to render
            request: The incoming request object
            **context: Additional context variables to pass to the template
            
        Returns:
            Rendered template response
        """
        # Add alter information to the context
        full_context = {
            "request": request,
            "current_alter": self.current_alter,
            "alters_status": self.alters_status,
            **context
        }
        return self.templates.TemplateResponse(template_name, full_context)
    
    def switch_alter(self, alter_name: str) -> bool:
        """
        Switch the current fronting alter.
        
        Args:
            alter_name: Name of the alter to make front
            
        Returns:
            True if successful, False otherwise
        """
        if alter_name in self.alters_status:
            # Reset all alters to not fronting
            for name in self.alters_status:
                self.alters_status[name] = False
            
            # Set the selected alter to fronting
            self.alters_status[alter_name] = True
            self.current_alter = alter_name
            
            # Update template paths
            self._setup_templates()
            
            # Save the updated status back to the CSV file
            self._save_alters_status()
            return True
        return False
    
    def _save_alters_status(self):
        """Save the current alter status to the CSV file."""
        alters_csv_path = Path("modules/alter/data/alters.csv")
        
        with open(alters_csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['name', 'is_fronting'])
            for name, is_fronting in self.alters_status.items():
                writer.writerow([name, str(int(is_fronting))])