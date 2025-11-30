"""
Alter Module - The System's Face
Provides the alter system and template rendering functionality
"""
from fastapi import APIRouter
from .routes import alter


# Create router for alter module
router = APIRouter(prefix="/alter")

# Include routes
router.include_router(alter.router, tags=["alter"])


def get_module_info():
    """
    Provide metadata for the Alter module used by external registries.

    Returns:
        module_info (dict): Dictionary with module metadata:
            - name (str): Module identifier ("alter").
            - routes (list[str]): Route patterns exposed by the module (e.g., "/alter/*").
            - local_data_path (str): Relative path to the module's local data directory ("modules/alter/data").
    """
    return {
        "name": "alter",
        "routes": ["/alter/*", "/alter/switch/*", "/alter/status"],
        "local_data_path": "modules/alter/data"
    }