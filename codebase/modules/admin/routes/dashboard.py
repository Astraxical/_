"""
Basic routes for the admin module
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Create templates directory if it doesn't exist
templates_dir = "modules/admin/templates"
os.makedirs(templates_dir, exist_ok=True)

templates = Jinja2Templates(directory=templates_dir)


@router.get("/")
def admin_dashboard(request: Request):
    return templates.TemplateResponse("admin/index.html", {"request": request})