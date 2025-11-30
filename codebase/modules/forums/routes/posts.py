"""
Posts routes for the forums module
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import os
from sqlalchemy.orm import Session
from ..models import ForumPost, ForumThread
from ...utils.db import get_db


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
def create_post(post: PostCreate, db: Session = None):
    """
    Create a new forum post.

    Args:
        post: Post data to create

    Returns:
        Created post information
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    # Verify that the thread exists
    thread = db.query(ForumThread).filter(ForumThread.id == post.thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    db_post = ForumPost(
        content=post.content,
        thread_id=post.thread_id,
        author=post.author
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


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