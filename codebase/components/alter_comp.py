"""
Alter Component - Integration for Alter Module
"""

from fastapi import FastAPI
from modules.alter import router as alter_router


def setup_alter(app: FastAPI):
    """
    Mounts the alter router into the provided FastAPI application and returns metadata about the component.

    Parameters:
        app (FastAPI): The FastAPI application instance to attach the alter routes to.

    Returns:
        dict: Descriptor for the alter component with keys:
            - name (str): "alter"
            - routes (list[str]): route patterns exposed by the component (e.g., ["/alter/*"])
            - initialized (bool): True if the component was mounted
    """
    # Mount the alter routes
    app.include_router(alter_router)

    return {
        "name": "alter",
        "routes": ["/alter/*", "/alter/switch/*", "/alter/status"],
        "initialized": True
    }