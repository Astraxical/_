"""
Forums Component - Integration for Forums Module
"""

from fastapi import FastAPI
from modules.forums import router as forums_router


def setup_forums(app: FastAPI):
    """
    Configure and mount the forums router into the provided FastAPI application.
    
    Parameters:
        app (FastAPI): The FastAPI application to attach the forums routes to.
    
    Returns:
        dict: Metadata about the mounted component with keys:
            - name: "forums"
            - routes: list of route patterns handled by the component
            - initialized: True when mounting succeeded
    """
    # Mount the forums routes
    app.include_router(forums_router)
    
    return {
        "name": "forums",
        "routes": ["/forums/*"],
        "initialized": True
    }