"""
Forums Module - Community Discussion Platform
"""
from fastapi import APIRouter


# Export the router and services for component integration
router = APIRouter(prefix="/forums")


def get_module_info():
    """
    Provide module metadata used by the application registry.
    
    Returns:
        info (dict): A dictionary with module metadata:
            - name (str): Module identifier ("forums").
            - routes (list[str]): Public route patterns exposed by the module.
            - local_data_path (str): Relative path to the module's local data directory.
    """
    return {
        "name": "forums",
        "routes": ["/forums/*"],
        "local_data_path": "modules/forums/data"
    }