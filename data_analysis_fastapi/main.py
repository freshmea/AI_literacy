from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


BASE_DIR = Path(__file__).resolve().parent
APP_NAME = "AI Literacy FastAPI Demo"
TAGLINE = "A colorful tour of semantic HTML styled with CSS"

app = FastAPI(title=APP_NAME, version="0.1.0")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def render(request: Request, template_name: str, current_page: str) -> HTMLResponse:
    """Render a template with shared context for navigation."""
    return templates.TemplateResponse(
        template_name,
        {
            "request": request,
            "app_name": APP_NAME,
            "tagline": TAGLINE,
            "current_page": current_page,
        },
    )


@app.get("/", response_class=HTMLResponse, name="home")
async def read_root(request: Request) -> HTMLResponse:
    """Serve the landing page with menu links to each sample."""
    return render(request, "index.html", current_page="home")


@app.get("/layout", response_class=HTMLResponse, name="layout_page")
async def layout_page(request: Request) -> HTMLResponse:
    return render(request, "layout.html", current_page="layout")


@app.get("/table", response_class=HTMLResponse, name="table_page")
async def table_page(request: Request) -> HTMLResponse:
    return render(request, "table.html", current_page="table")


@app.get("/forms", response_class=HTMLResponse, name="forms_page")
async def forms_page(request: Request) -> HTMLResponse:
    return render(request, "forms.html", current_page="forms")


@app.get("/code", response_class=HTMLResponse, name="code_page")
async def code_page(request: Request) -> HTMLResponse:
    return render(request, "code.html", current_page="code")


if __name__ == "__main__":
    # Allow running `python main.py` directly for convenience.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
