"""
Routes for the RTC module
"""
from fastapi import APIRouter
from . import ws


# Create main router for RTC module
router = APIRouter()

# Include sub-routes
router.include_router(ws.router, prefix="/ws", tags=["websocket"])