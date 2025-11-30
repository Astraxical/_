"""
Template Module - The System's Face
Provides the alter system and template rendering functionality
"""
from fastapi import APIRouter
from .routes import alter


# Create router for template module
router = APIRouter(prefix="/template")

# Include routes
router.include_router(alter.router, prefix="/alter", tags=["alter"])


def get_module_info():
    """
    Provide metadata for the Template module used by external registries.

    Returns:
        module_info (dict): Dictionary with module metadata:
            - name (str): Module identifier ("template").
            - routes (list[str]): Route patterns exposed by the module (e.g., "/template/*").
            - local_data_path (str): Relative path to the module's local data directory ("modules/template/data").
    """
    return {
        "name": "template",
        "routes": ["/template/*", "/template/alter/*"],
        "local_data_path": "modules/template/data"
    }