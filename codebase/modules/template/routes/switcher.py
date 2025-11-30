"""
Routes for the template module - alter switching functionality
"""
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from .. import alter_manager, render_alter_template  # Import from parent module to avoid circular import


router = APIRouter()


@router.get("/alters")
def show_alters(request: Request):
    """Display the current alters and allow switching between them."""
    return render_alter_template(request, "alters.html")


@router.post("/switch_alter/{alter_name}")
def switch_alter(alter_name: str):
    """Switch the currently fronting alter."""
    success = alter_manager.set_fronting_alter(alter_name)
    if success:
        # Redirect back to home to see the new alter
        return RedirectResponse(url="/", status_code=303)
    else:
        # If switching failed, redirect back to home anyway
        return RedirectResponse(url="/", status_code=303)