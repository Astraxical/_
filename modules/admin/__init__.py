"""
Admin Module - Control Room
Provides admin interface and system controls
"""
from fastapi import APIRouter


# Export the router for component integration
router = APIRouter(prefix="/admin")


def get_module_info():
    """Return module-specific information for registry"""
    return {
        "name": "admin",
        "routes": ["/admin/*"],
        "local_data_path": "modules/admin/data"
    }