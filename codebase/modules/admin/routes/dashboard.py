"""
Routes for the admin dashboard
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Create templates directory if it doesn't exist
templates_dir = "modules/admin/templates"
os.makedirs(templates_dir, exist_ok=True)
templates = Jinja2Templates(directory=templates_dir)


@router.get("/")
def admin_dashboard(request: Request):
    """
    Get the admin dashboard.

    Returns:
        Admin dashboard information
    """
    # Try to render the template, fallback to JSON if template doesn't exist
    try:
        return templates.TemplateResponse("admin/index.html", {"request": request})
    except:
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
