"""
Threads routes for the forums module
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# For the project structure, we need to ensure the codebase directory is in the path
import sys
import os

# Add the codebase directory to sys.path if not already present
codebase_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..')
abs_codebase_dir = os.path.abspath(codebase_dir)
if abs_codebase_dir not in sys.path:
    sys.path.insert(0, abs_codebase_dir)

from utils.db import get_db
from ..models import ForumThread, ForumPost, ForumCategory


router = APIRouter()

# Create templates directory if it doesn't exist
templates_dir = "modules/forums/templates"
os.makedirs(templates_dir, exist_ok=True)
templates = Jinja2Templates(directory=templates_dir)


class ThreadCreate(BaseModel):
    title: str
    content: str
    author: str
    category_id: Optional[int] = None
    tag_names: str = ""  # Comma-separated tag names


@router.get("/")
def get_threads(request: Request, db: Session = None):
    """
    Get all forum threads.

    Returns:
        List of threads
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    # Get all categories (including nested)
    categories = db.query(ForumCategory).filter(ForumCategory.parent_id == None).all()

    # Get threads, with pinned threads first
    pinned_threads = db.query(ForumThread).filter(ForumThread.is_pinned == True).all()
    regular_threads = db.query(ForumThread).filter(ForumThread.is_pinned == False).all()

    # Combine pinned threads first, then regular threads
    all_threads = pinned_threads + regular_threads

    return templates.TemplateResponse("forums/index.html", {
        "request": request,
        "threads": all_threads,
        "categories": categories
    })


@router.get("/categories/{category_id}")
def get_threads_by_category(request: Request, category_id: int, db: Session = None):
    """
    Get all forum threads in a specific category.

    Args:
        category_id: ID of the category to filter by

    Returns:
        List of threads in the category
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    category = db.query(ForumCategory).filter(ForumCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    threads = db.query(ForumThread).filter(ForumThread.category_id == category_id).all()
    categories = db.query(ForumCategory).filter(ForumCategory.parent_id == category_id).all()

    return templates.TemplateResponse("forums/category.html", {
        "request": request,
        "threads": threads,
        "category": category,
        "categories": categories,
        "parent_category": category.parent
    })


def get_replies_for_post(post_id, db):
    """Recursively get all replies for a post."""
    replies = db.query(ForumPost).filter(ForumPost.parent_post_id == post_id).all()
    for reply in replies:
        reply.replies = get_replies_for_post(reply.id, db)
    return replies


@router.get("/search")
def search_threads(request: Request, q: str = None, db: Session = None):
    """
    Search for threads and posts based on a query string.

    Args:
        q: Search query string

    Returns:
        Search results matching the query
    """
    if not q:
        return templates.TemplateResponse("forums/search.html", {
            "request": request,
            "results": [],
            "query": ""
        })

    if db is None:
        from utils.db import get_db
        db = next(get_db())

    # Search in thread titles and content
    thread_results = db.query(ForumThread).filter(
        ForumThread.title.contains(q) | ForumThread.content.contains(q)
    ).all()

    # Search in post content
    post_results = db.query(ForumPost).filter(
        ForumPost.content.contains(q)
    ).all()

    # Get the threads that contain the matching posts
    post_thread_ids = {post.thread_id for post in post_results}
    post_threads = db.query(ForumThread).filter(
        ForumThread.id.in_(list(post_thread_ids))
    ).all()

    # Combine results
    all_threads = list(set(thread_results + post_threads))

    return templates.TemplateResponse("forums/search.html", {
        "request": request,
        "results": all_threads,
        "query": q
    })


@router.get("/{thread_id}")
def get_thread(request: Request, thread_id: int, db: Session = None):
    """
    Get a specific forum thread by ID.

    Args:
        thread_id: ID of the thread to retrieve

    Returns:
        Thread information
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    thread = db.query(ForumThread).filter(ForumThread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    # Get top-level posts (posts without a parent) and their replies
    posts = db.query(ForumPost).filter(
        ForumPost.thread_id == thread_id,
        ForumPost.parent_post_id == None
    ).all()

    # Include replies for each post
    for post in posts:
        post.replies = get_replies_for_post(post.id, db)

    return templates.TemplateResponse("forums/thread.html", {
        "request": request,
        "thread": thread,
        "posts": posts,
        "thread_id": thread_id
    })


@router.post("/")
def create_thread(thread: ThreadCreate, db: Session = None):
    """
    Create a new forum thread.

    Args:
        thread: Thread data to create

    Returns:
        Created thread information
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    db_thread = ForumThread(
        title=thread.title,
        content=thread.content,
        author=thread.author,
        category_id=thread.category_id
    )

    # Process tags
    if thread.tag_names:
        tag_names = [name.strip() for name in thread.tag_names.split(',') if name.strip()]
        for tag_name in tag_names:
            # Find or create the tag
            tag = db.query(ForumTag).filter(ForumTag.name == tag_name).first()
            if not tag:
                tag = ForumTag(name=tag_name)
                db.add(tag)
            db_thread.tags.append(tag)

    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread


@router.put("/{thread_id}")
def update_thread(thread_id: int, thread: ThreadCreate, db: Session = None):
    """
    Update a forum thread by ID.

    Args:
        thread_id: ID of the thread to update
        thread: Updated thread data

    Returns:
        Updated thread information
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    db_thread = db.query(ForumThread).filter(ForumThread.id == thread_id).first()
    if not db_thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    db_thread.title = thread.title
    db_thread.content = thread.content
    db_thread.author = thread.author
    db_thread.category_id = thread.category_id

    db.commit()
    db.refresh(db_thread)
    return db_thread


@router.delete("/{thread_id}")
def delete_thread(thread_id: int, db: Session = None):
    """
    Delete a forum thread by ID.

    Args:
        thread_id: ID of the thread to delete

    Returns:
        Success message
    """
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    thread = db.query(ForumThread).filter(ForumThread.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")

    db.delete(thread)
    db.commit()
    return {"message": f"Thread {thread_id} deleted successfully"}