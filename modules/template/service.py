"""
Template Module Services
"""
from typing import Dict, Any
from utils.db import SessionLocal
from modules.template.engine import TemplateEngine


def get_alter_status(alter_name: str) -> Dict[str, Any]:
    """
    Get the status of a specific alter
    """
    template_engine = TemplateEngine()
    is_fronting = template_engine.alters_status.get(alter_name, False)
    
    return {
        "name": alter_name,
        "is_fronting": is_fronting,
        "available": alter_name in template_engine.alters_status
    }


def switch_alter(alter_name: str) -> Dict[str, Any]:
    """
    Switch the currently fronting alter
    """
    template_engine = TemplateEngine()
    
    if alter_name not in template_engine.alters_status:
        return {
            "success": False,
            "message": f"Alter {alter_name} does not exist"
        }
    
    template_engine.switch_alter(alter_name)
    
    return {
        "success": True,
        "message": f"Successfully switched to {alter_name}",
        "current_alter": alter_name
    }


def get_template_context() -> Dict[str, Any]:
    """
    Get the context for template rendering
    """
    template_engine = TemplateEngine()
    
    return {
        "current_alter": template_engine.current_fronting,
        "alters_status": template_engine.alters_status
    }