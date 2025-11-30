"""
API routes for getting alter status
"""
from fastapi import APIRouter
from modules.template import alter_manager


router = APIRouter()


@router.get("/api/alter-status")
def get_alter_status():
    """Get the current status of all alters in JSON format."""
    current_alter = alter_manager.get_current_alter()
    alters_status = alter_manager.get_alters_status()
    
    return {
        "current_alter": current_alter,
        "alters_status": alters_status
    }