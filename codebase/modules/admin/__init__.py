"""
Admin Module - Control Room
Provides admin interface and system controls
"""
from fastapi import APIRouter
from .routes import router as admin_router


# Export the router for component integration
router = admin_router


def get_module_info():
    """
    Provide module metadata used by the component registry.
    
    The returned dictionary describes the module's identifier, the route patterns it exposes, and the local filesystem path for module-specific data.
    
    Returns:
        dict: {
            "name": module name (str),
            "routes": list of route patterns exposed by the module (list[str]),
            "local_data_path": relative path to the module's local data (str)
        }
    """
    return {
        "name": "admin",
        "routes": ["/admin/*"],
        "local_data_path": "modules/admin/data"
    }