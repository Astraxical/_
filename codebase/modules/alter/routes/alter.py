"""
Routes for the alter module - handles alter switching and related operations
"""
from fastapi import APIRouter, Request
from modules.alter.engine import TemplateEngine


# Create router for alter module
router = APIRouter()

# Global instance of the template engine
template_engine = TemplateEngine()


@router.get("/switch/{alter_name}")
def switch_alter(alter_name: str):
    """
    Switch the current fronting alter.
    
    Args:
        alter_name: Name of the alter to make front
        
    Returns:
        Success or failure message
    """
    success = template_engine.switch_alter(alter_name)
    if success:
        return {"success": True, "message": f"Switched to alter {alter_name}"}
    else:
        return {"success": False, "message": f"Failed to switch to alter {alter_name}"}


@router.get("/status")
def get_alter_status():
    """
    Get the current status of all alters.
    
    Returns:
        Dictionary with current alter and status of all alters
    """
    return {
        "current_alter": template_engine.current_alter,
        "alters_status": template_engine.alters_status
    }