"""
Template Component - Integration for Template Module
"""

from fastapi import FastAPI
from modules.template import router as template_router, template_engine


def setup_template(app: FastAPI):
    """
    Setup the template module component
    """
    # Mount the template routes
    app.include_router(template_router)
    
    # Add template engine to app state for other components to access
    app.state.template_engine = template_engine
    
    return {
        "name": "template",
        "routes": ["/template/*"],
        "initialized": True
    }