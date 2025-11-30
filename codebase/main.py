from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from components import setup_components
from modules.template import render_alter_template
import config

app = FastAPI(
    title="Multi-House Application",
    debug=config.DEBUG
)

# Mount global static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup components (integration layer)
setup_components(app)

@app.get("/")
def read_root(request: Request):
    """
    Render the application's homepage with the current alter's context.

    Provides a template context containing the incoming request,
    `current_alter` set to the currently fronting alter, and
    `alters_status` mapping showing which alters are active.

    Parameters:
        request (Request): The incoming HTTP request used by the template.

    Returns:
        TemplateResponse: The response rendering "index.html" with the homepage context.
    """
    return render_alter_template(request, "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=config.PORT,
        reload=config.DEBUG
    )