from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from components import setup_components
from modules.template.engine import TemplateEngine
import config

app = FastAPI(
    title="Multi-House Application",
    debug=config.DEBUG
)

# Mount global static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup components (integration layer)
setup_components(app)

# Initialize the template engine
template_engine = TemplateEngine()


@app.get("/")
def read_root(request: Request):
    """
    Render the application's homepage with alter-specific template rendering.

    Uses the template engine to render the index template with appropriate
    alter-specific overrides based on which alter is currently fronting.

    Parameters:
        request (Request): The incoming HTTP request used by the template.

    Returns:
        TemplateResponse: The response rendering "index.html" with the homepage context.
    """
    return template_engine.render("index.html", request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.DEBUG
    )