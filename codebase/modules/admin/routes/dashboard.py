"""
Routes for the admin module
"""
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_admin_dashboard():
    """
    Get the admin dashboard.
    
    Returns:
        Admin dashboard information
    """
    return {"message": "Admin Dashboard", "stats": {"users": 0, "modules": 3, "system_status": "operational"}}


@router.get("/modules")
def get_module_status():
    """
    Get status of all modules.
    
    Returns:
        Status information for all modules
    """
    return {"message": "Module status", "modules": [
        {"name": "forums", "status": "active"},
        {"name": "rtc", "status": "active"},
        {"name": "admin", "status": "active"},
        {"name": "template", "status": "active"}
    ]}