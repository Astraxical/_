"""
Admin Component - Integration for Admin Module
"""

from fastapi import FastAPI
from modules.admin import router as admin_router


def setup_admin(app: FastAPI):
    """
    Mounts the admin router into the provided FastAPI application and returns metadata about the component.
    
    Parameters:
        app (FastAPI): The FastAPI application instance to attach the admin routes to.
    
    Returns:
        dict: Descriptor for the admin component with keys:
            - name (str): "admin"
            - routes (list[str]): route patterns exposed by the component (e.g., ["/admin/*"])
            - initialized (bool): True if the component was mounted
    """
    # Mount the admin routes
    app.include_router(admin_router)
    
    return {
        "name": "admin",
        "routes": ["/admin/*"],
        "initialized": True
    }