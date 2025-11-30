"""
Template Component - Integration for Template Module (Alter System)
"""

from fastapi import FastAPI
from modules.template.routes.switcher import router as switcher_router


def setup_template(app: FastAPI):
    """
    Mounts the template module router into the provided FastAPI application and returns metadata about the component.

    Parameters:
        app (FastAPI): The FastAPI application instance to attach the template routes to.

    Returns:
        dict: Descriptor for the template component with keys:
            - name (str): "template"
            - routes (list[str]): route patterns exposed by the component (e.g., ["/alters", "/switch_alter/*"])
            - initialized (bool): True if the component was mounted
    """
    # Mount the switcher routes directly to have /switch_alter endpoint available
    app.include_router(switcher_router)

    return {
        "name": "template",
        "routes": ["/alters", "/switch_alter/*"],
        "initialized": True
    }