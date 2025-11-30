"""
Basic routes for the forums module
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from sqlalchemy.orm import Session
from ..models import ForumThread
from ...utils.db import get_db


router = APIRouter()

# Create templates directory if it doesn't exist
templates_dir = "modules/forums/templates"
os.makedirs(templates_dir, exist_ok=True)

templates = Jinja2Templates(directory=templates_dir)


class ThreadCreate(BaseModel):
    title: str
    content: str
    author: str


@router.get("/")
def forums_index(request: Request, db: Session = None):
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    threads = db.query(ForumThread).all()
    return templates.TemplateResponse("forums/index.html", {"request": request, "threads": threads})


@router.get("/new")
def new_thread_form(request: Request, category_id: int = None, db: Session = None):
    if db is None:
        from utils.db import get_db
        db = next(get_db())

    categories = db.query(ForumCategory).all()
    return templates.TemplateResponse("forums/new_thread.html", {
        "request": request,
        "categories": categories,
        "selected_category_id": category_id
    })


@router.post("/threads")
def create_thread(thread: ThreadCreate, db: Session = None):
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

    # Redirect to the new thread
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/forums/threads/{db_thread.id}", status_code=303)