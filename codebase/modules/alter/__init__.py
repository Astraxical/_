"""
Alter Module - The System's Face
Provides the alter system and template rendering functionality
"""
from fastapi import APIRouter
from .routes import router as alter_router


# Export the router for component integration
router = APIRouter(prefix="/alter")
router.include_router(alter_router)


def get_module_info():
    """
    Return metadata for the Alter module intended for external registries.
    
    Returns:
        module_info (dict): Mapping containing module metadata:
            - name (str): Module identifier, `"alter"`.
            - routes (list[str]): Route patterns exposed by the module, e.g. `"/alter/*"`, `"/alter/switch/*"`, `"/alter/status"`.
            - local_data_path (str): Relative path to the module's local data directory, `"modules/alter/data"`.
    """
    return {
        "name": "alter",
        "routes": ["/alter/*", "/alter/switch/*", "/alter/status"],
        "local_data_path": "modules/alter/data"
    }