"""
Routes for the admin module
"""
from fastapi import APIRouter
from . import dashboard, modules


# Create main router for admin module
router = APIRouter()

# Include sub-routes
router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
router.include_router(modules.router, prefix="/modules", tags=["modules"])