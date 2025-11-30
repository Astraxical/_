"""
Template Engine for Alter-Specific Rendering
Loads alters.csv and provides render_alter functionality
"""
import csv
import os
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path


class TemplateEngine:
    def __init__(self):
        self.alters_status = self._load_alters_status()
        self.current_fronting = self._get_current_fronting()
        self.jinja_env = self._create_jinja_environment()
        
    def _load_alters_status(self) -> Dict[str, bool]:
        """
        Load alter status from alters.csv
        Format: alter_name,status (e.g., "seles,1"; "dexen,0"; "yuki,0")
        """
        alters_file = Path("modules/template/data/alters.csv")
        alters_status = {}
        
        if alters_file.exists():
            with open(alters_file, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for row in reader:
                    if len(row) == 2:
                        alter_name, status = row
                        alters_status[alter_name.strip()] = status.strip() == '1'
        else:
            # Default values if file doesn't exist
            alters_status = {"seles": True, "dexen": False, "yuki": False}
            
        return alters_status
    
    def _get_current_fronting(self) -> str:
        """Get the currently fronting alter"""
        for alter, is_fronting in self.alters_status.items():
            if is_fronting:
                return alter
        return "global"  # Default to global if no alter is fronting
    
    def _create_jinja_environment(self) -> Environment:
        """Create Jinja2 environment with template search paths"""
        # Search paths: current fronting alter -> global templates -> main templates
        search_paths = [
            f"modules/template/templates/{self.current_fronting}",  # Alter-specific templates
            "modules/template/templates/global",  # Global templates for this module
            "templates"  # Main global templates
        ]
        
        # Filter out paths that don't exist
        existing_paths = [path for path in search_paths if Path(path).exists()]
        
        return Environment(
            loader=FileSystemLoader(existing_paths),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def render_alter(self, template_name: str, **context) -> str:
        """
        Render a template with alter-specific context
        """
        # Add alter-specific context
        context['current_alter'] = self.current_fronting
        context['alters_status'] = self.alters_status
        
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            print(f"Template rendering error: {e}")
            # Fallback to global template if specific one doesn't exist
            if self.current_fronting != 'global':
                global_env = Environment(
                    loader=FileSystemLoader(['templates']),
                    autoescape=select_autoescape(['html', 'xml'])
                )
                template = global_env.get_template(template_name)
                return template.render(**context)
            else:
                raise e
    
    def switch_alter(self, alter_name: str):
        """Switch the currently fronting alter"""
        if alter_name in self.alters_status:
            # Update status dict
            for key in self.alters_status:
                self.alters_status[key] = (key == alter_name)
            self.current_fronting = alter_name
            
            # Update alters.csv file
            alters_file = Path("modules/template/data/alters.csv")
            with open(alters_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                for name, status in self.alters_status.items():
                    writer.writerow([name, '1' if status else '0'])
            
            # Recreate Jinja environment with new fronting alter
            self.jinja_env = self._create_jinja_environment()