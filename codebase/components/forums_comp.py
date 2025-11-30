"""
Forums Component - Integration for Forums Module
"""

from fastapi import FastAPI
from modules.forums import router as forums_router


def setup_forums(app: FastAPI):
    """
    Setup the forums module component
    """
    # Mount the forums routes
    app.include_router(forums_router)
    
    return {
        "name": "forums",
        "routes": ["/forums/*"],
        "initialized": True
    }