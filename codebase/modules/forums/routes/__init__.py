"""
Routes for the forums module
"""
from fastapi import APIRouter
from . import index, threads, posts


# Create main router for forums module
router = APIRouter()

# Include sub-routes
router.include_router(index.router, tags=["index"])
router.include_router(threads.router, prefix="/threads", tags=["threads"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])