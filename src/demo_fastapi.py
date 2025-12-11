import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

class FastAPIApp:
    """
    FastAPI 애플리케이션을 관리하는 클래스입니다.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """
        FastAPIApp 초기화 메서드입니다.

        Args:
            host (str): 서버 호스트 주소. 기본값은 "127.0.0.1".
            port (int): 서버 포트 번호. 기본값은 8000.
        """
        self.host = host
        self.port = port
        self.app = FastAPI()
        
        # 현재 파일의 디렉토리 경로
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 정적 파일 및 템플릿 디렉토리 설정
        self.static_dir = os.path.join(current_dir, "static")
        self.templates_dir = os.path.join(current_dir, "templates")

        # 디렉토리가 없으면 생성 (데모용)
        os.makedirs(self.static_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)

        self.app.mount("/static", StaticFiles(directory=self.static_dir), name="static")
        self.templates = Jinja2Templates(directory=self.templates_dir)
        
        self.setup_routes()

    def setup_routes(self):
        """
        라우트 설정을 수행합니다.
        """
        @self.app.get("/", response_class=HTMLResponse)
        async def read_root(request: Request):
            """
            루트 경로 핸들러입니다. index.html을 렌더링합니다.
            """
            return self.templates.TemplateResponse("index.html", {"request": request})

    def run(self):
        """
        Uvicorn 서버를 실행합니다.
        """
        uvicorn.run(self.app, host=self.host, port=self.port)

def main():
    """
    프로그램의 진입점입니다.
    """
    api_app = FastAPIApp()
    api_app.run()

if __name__ == "__main__":
    main()
