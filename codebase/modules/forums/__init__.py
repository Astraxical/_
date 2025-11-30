"""
Forums Module - Community Discussion Platform
"""
from fastapi import APIRouter


# Export the router and services for component integration
router = APIRouter(prefix="/forums")


def get_module_info():
    """Return module-specific information for registry"""
    return {
        "name": "forums",
        "routes": ["/forums/*"],
        "local_data_path": "modules/forums/data"
    }