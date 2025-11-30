"""
Posts routes for the forums module
"""
from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_posts():
    """
    Get all forum posts.
    
    Returns:
        List of posts
    """
    return {"message": "List of forum posts", "data": []}


@router.get("/{post_id}")
def get_post(post_id: int):
    """
    Get a specific forum post by ID.
    
    Args:
        post_id: ID of the post to retrieve
    
    Returns:
        Post information
    """
    return {"message": f"Post {post_id}", "data": {}}