"""
Template Component - Integration for Template Module
"""

from fastapi import FastAPI
from modules.template import router as template_router


def setup_template(app: FastAPI):
    """
    Mounts the template router into the provided FastAPI application and returns metadata about the component.

    Parameters:
        app (FastAPI): The FastAPI application instance to attach the template routes to.

    Returns:
        dict: Descriptor for the template component with keys:
            - name (str): "template"
            - routes (list[str]): route patterns exposed by the component (e.g., ["/template/*"])
            - initialized (bool): True if the component was mounted
    """
    # Mount the template routes
    app.include_router(template_router)

    return {
        "name": "template",
        "routes": ["/template/*", "/template/alter/*"],
        "initialized": True
    }