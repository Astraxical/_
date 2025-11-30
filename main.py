from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from components import setup_components
import config

app = FastAPI(
    title="Multi-House Application",
    debug=config.DEBUG
)

# Mount global static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup components (integration layer)
setup_components(app)

# Add Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    # Get the template engine from app state
    template_engine = getattr(app.state, 'template_engine', None)
    
    if template_engine:
        # Use the template engine's context
        context = {
            "request": request,
            "current_alter": template_engine.current_fronting,
            "alters_status": template_engine.alters_status
        }
    else:
        # Default context
        context = {
            "request": request,
            "current_alter": "global",
            "alters_status": {"seles": True, "dexen": False, "yuki": False}
        }
    
    return templates.TemplateResponse("index.html", context)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.DEBUG
    )