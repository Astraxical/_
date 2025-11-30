"""
Threads routes for the forums module
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from ...utils.db import get_db
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

    threads = db.query(ForumThread).all()
    return templates.TemplateResponse("forums/index.html", {"request": request, "threads": threads})


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

    posts = db.query(ForumPost).filter(ForumPost.thread_id == thread_id).all()
    return templates.TemplateResponse("forums/thread.html", {
        "request": request,
        "thread": thread,
        "posts": posts
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