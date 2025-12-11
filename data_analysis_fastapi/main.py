from pathlib import Path

from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
APP_NAME = "AI Literacy FastAPI Demo"
TAGLINE = "A colorful tour of semantic HTML styled with CSS"
DATABASE_URL = f"sqlite:///{BASE_DIR / 'chat.db'}"

app = FastAPI(title=APP_NAME, version="0.1.0")

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class ChatMessage(SQLModel, table=True):
    __tablename__ = "chat_messages"
    __table_args__ = {"extend_existing": True}
    id: int | None = Field(default=None, primary_key=True)
    user: str = Field(index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


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


@app.get("/chat", response_class=HTMLResponse, name="chat_page")
def chat_page(
    request: Request,
    session: Session = Depends(get_session),
) -> HTMLResponse:
    messages = session.exec(
        select(ChatMessage).order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc()).limit(40)
    ).all()
    messages = list(reversed(messages))
    error = request.query_params.get("error")
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "app_name": APP_NAME,
            "tagline": TAGLINE,
            "current_page": "chat",
            "messages": messages,
            "error": error,
        },
    )


@app.post("/chat")
def post_chat(
    user: str = Form(...),
    content: str = Form(...),
    session: Session = Depends(get_session),
):
    trimmed_user = user.strip()
    trimmed_content = content.strip()

    if not trimmed_user:
        return RedirectResponse(
            url="/chat?error=이름을 입력해야 채팅을 보낼 수 있습니다.",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    if not trimmed_content:
        return RedirectResponse(url="/chat", status_code=status.HTTP_303_SEE_OTHER)

    message = ChatMessage(user=trimmed_user, content=trimmed_content)
    session.add(message)
    session.commit()
    session.refresh(message)
    return RedirectResponse(url="/chat", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/chat/all", name="chat_all")
def chat_all(session: Session = Depends(get_session)) -> JSONResponse:
    messages = session.exec(
        select(ChatMessage).order_by(ChatMessage.created_at.desc(), ChatMessage.id.desc())
    ).all()
    return JSONResponse(
        [
            {
                "id": msg.id,
                "user": msg.user,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in messages
        ]
    )


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


if __name__ == "__main__":
    # Allow running `python main.py` directly for convenience.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
