"""
Admin Component - Integration for Admin Module
"""

from fastapi import FastAPI
from modules.admin import router as admin_router


def setup_admin(app: FastAPI):
    """
    Setup the admin module component
    """
    # Mount the admin routes
    app.include_router(admin_router)
    
    return {
        "name": "admin",
        "routes": ["/admin/*"],
        "initialized": True
    }