"""
Routes for the alter module
"""
from fastapi import APIRouter
from . import alter


# Create main router for alter module
router = APIRouter()

# Include sub-routes
router.include_router(alter.router)