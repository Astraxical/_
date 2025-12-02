"""
Posts routes for the forums module
"""
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import os
from sqlalchemy.orm import Session
from ..models import ForumPost, ForumThread
# For the project structure, we need to ensure the codebase directory is in the path
import sys
import os

# Add the codebase directory to sys.path if not already present
codebase_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..')
abs_codebase_dir = os.path.abspath(codebase_dir)
if abs_codebase_dir not in sys.path:
    sys.path.insert(0, abs_codebase_dir)

from utils.db import get_db


router = APIRouter()

# Create templates directory if it doesn't exist
templates_dir = "modules/forums/templates"
os.makedirs(templates_dir, exist_ok=True)
templates = Jinja2Templates(directory=templates_dir)


class PostCreate(BaseModel):
    content: str
    thread_id: int
    author: str


@router.get("/")
def get_posts(request: Request, db: Session = None):
    """
    Get all forum posts.

    Returns:
        List of posts
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    posts = db.query(ForumPost).all()

    # Get thread details for each post
    posts_with_threads = []
    for post in posts:
        thread = db.query(ForumThread).filter(ForumThread.id == post.thread_id).first()
        posts_with_threads.append({
            "post": post,
            "thread": thread
        })

    return templates.TemplateResponse("forums/posts.html", {
        "request": request,
        "posts_with_threads": posts_with_threads
    })


@router.get("/{post_id}")
def get_post(request: Request, post_id: int, db: Session = None):
    """
    Get a specific forum post by ID.

    Args:
        post_id: ID of the post to retrieve

    Returns:
        Post information
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    thread = db.query(ForumThread).filter(ForumThread.id == post.thread_id).first()
    return templates.TemplateResponse("forums/post.html", {
        "request": request,
        "post": post,
        "thread": thread
    })


@router.post("/")
async def create_post(content: str = Form(...), thread_id: int = Form(...), author: str = Form(...), parent_post_id: int = Form(None), db: Session = None):
    """
    Create a new forum post or reply.

    Args:
        content: Content of the post
        thread_id: ID of the thread to post in
        author: Author of the post
        parent_post_id: ID of the parent post if this is a reply (optional)

    Returns:
        Redirect to the thread page
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    # Verify that the thread exists
    thread = db.query(ForumThread).filter(ForumThread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    # If this is a reply, verify the parent post exists
    if parent_post_id:
        parent_post = db.query(ForumPost).filter(ForumPost.id == parent_post_id).first()
        if not parent_post:
            raise HTTPException(status_code=404, detail="Parent post not found")

    db_post = ForumPost(
        content=content,
        thread_id=thread_id,
        author=author,
        parent_post_id=parent_post_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # Redirect back to the thread page
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/forums/threads/{thread_id}", status_code=303)


@router.put("/{post_id}")
def update_post(post_id: int, post: PostCreate, db: Session = None):
    """
    Update a forum post by ID.

    Args:
        post_id: ID of the post to update
        post: Updated post data

    Returns:
        Updated post information
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    db_post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Verify that the thread exists
    thread = db.query(ForumThread).filter(ForumThread.id == post.thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    db_post.content = post.content
    db_post.thread_id = post.thread_id
    db_post.author = post.author

    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = None):
    """
    Delete a forum post by ID.

    Args:
        post_id: ID of the post to delete

    Returns:
        Success message
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    post = db.query(ForumPost).filter(ForumPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"message": f"Post {post_id} deleted successfully"}