"""
Template Module - The System's Face
Handles alter-specific rendering and template management
"""
from fastapi import APIRouter
from .engine import TemplateEngine


# Export the router and services for component integration
router = APIRouter(prefix="/template")
template_engine = TemplateEngine()


def get_module_info():
    """Return module-specific information for registry"""
    return {
        "name": "template",
        "routes": ["/template/*"],  # Placeholder for actual routes
        "local_data_path": "modules/template/data"
    }