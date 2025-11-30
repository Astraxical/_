"""
Template Engine - Jinja2 environment and alter template loading
"""
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Dict, Any, Optional
import csv
import os
from pathlib import Path


class AlterTemplateEngine:
    """
    A specialized template engine that supports alter-specific templates.
    """
    
    def __init__(self, global_templates_dir: str = "templates"):
        self.global_templates_dir = global_templates_dir
        self.alters_csv_path = Path("modules/template/data/alters.csv")
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
    
    def get_alter_template_dirs(self, alter_name: Optional[str] = None) -> list:
        """
        Get template directories based on the current or specified alter.
        
        The search order is:
        1. Current alter's template directory (e.g., modules/template/templates/seles/)
        2. Global template directory (modules/template/templates/global/)
        3. Module-specific template directories (e.g., modules/forums/templates/)
        4. Global application templates (templates/)
        """
        if not alter_name:
            alter_name = self.get_current_alter()
        
        template_dirs = []
        
        # First, check alter-specific templates (highest priority)
        if alter_name and alter_name != "global":
            alter_template_dir = f"modules/template/templates/{alter_name}"
            if Path(alter_template_dir).exists():
                template_dirs.append(alter_template_dir)
        
        # Then global alter templates
        global_alter_template_dir = "modules/template/templates/global"
        if Path(global_alter_template_dir).exists():
            template_dirs.append(global_alter_template_dir)
        
        # Finally, default to global templates
        if Path(self.global_templates_dir).exists():
            template_dirs.append(self.global_templates_dir)
        
        # If no directories exist, add the default
        if not template_dirs:
            template_dirs.append(self.global_templates_dir)
        
        return template_dirs
    
    def get_template_response(self, request: Request, template_name: str, context: Dict[str, Any]):
        """
        Get a template response using the appropriate template based on the current alter.
        """
        # Get template directories for the current alter
        template_dirs = self.get_alter_template_dirs()
        
        # Create a Jinja2Templates instance with the first directory
        # For this implementation, we'll try to find the template in the priority order
        for template_dir in template_dirs:
            templates = Jinja2Templates(directory=template_dir)
            template_path = Path(template_dir) / template_name
            
            if template_path.exists():
                # Found the template in this directory, render it
                return templates.TemplateResponse(template_name, context)
        
        # If template not found in alter-specific locations, try the default global templates
        templates = Jinja2Templates(directory=self.global_templates_dir)
        return templates.TemplateResponse(template_name, context)


# Create a global instance of the engine
engine = AlterTemplateEngine()