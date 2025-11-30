"""
Basic routes for the RTC module
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Create templates directory if it doesn't exist
templates_dir = "modules/rtc/templates"
os.makedirs(templates_dir, exist_ok=True)

templates = Jinja2Templates(directory=templates_dir)


@router.get("/")
def rtc_index(request: Request):
    return templates.TemplateResponse("rtc/index.html", {"request": request})