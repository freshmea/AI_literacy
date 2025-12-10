# Agent 모드 지침서

## 개요
Agent 모드는 자율적으로 작업을 수행하는 소프트웨어 에이전트를 구현하기 위한 디자인 패턴입니다. Python 프로젝트에서 AI 에이전트, 자동화 봇, 워크플로우 관리자 등을 개발할 때 활용됩니다.

## 기본 구조

### 1. 클래스 기반 구현
- 모든 Agent는 클래스로 구현해야 합니다
- 상태 관리를 위해 인스턴스 변수를 적극 활용합니다
- 상속을 통한 확장성을 고려합니다

```python
class BaseAgent:
    """기본 에이전트 클래스"""
    
    def __init__(self, name: str, config: dict = None):
        """
        에이전트 초기화
        
        Args:
            name (str): 에이전트 이름
            config (dict, optional): 설정 딕셔너리. Defaults to None.
        """
        self.name = name
        self.config = config or {}
        self.is_active = False
        self.task_queue = []
```

### 2. 필수 메서드 구현
- `start()`: 에이전트 시작
- `stop()`: 에이전트 정지  
- `execute()`: 작업 실행
- `process_task()`: 개별 작업 처리

### 3. 타입 힌트 사용
모든 매개변수와 반환값에 타입 힌트를 명시합니다:

```python
def add_task(self, task: dict, priority: int = 0) -> bool:
    """작업을 큐에 추가"""
    pass

def get_status(self) -> dict:
    """에이전트 상태 반환"""
    pass
```

### 4. Docstring 활용
모든 클래스와 메서드에 docstring을 작성합니다:

```python
class TaskAgent(BaseAgent):
    """
    작업 처리 전용 에이전트
    
    이 클래스는 큐에서 작업을 가져와서 순차적으로 처리하는
    에이전트를 구현합니다.
    
    Attributes:
        max_concurrent_tasks (int): 동시 처리 가능한 최대 작업 수
        completed_tasks (list): 완료된 작업 목록
    """
```

### 5. 기본값 매개변수 활용
디폴트 아규먼트를 적극 활용하여 유연성을 제공합니다:

```python
def configure_agent(self, 
                   max_retries: int = 3, 
                   timeout: float = 30.0,
                   auto_restart: bool = True) -> None:
    """에이전트 설정"""
    pass
```

## Entry Point 설정

### main 함수 구현
프로젝트의 진입점으로 main 함수를 설정합니다:

```python
def main():
    """
    애플리케이션 진입점
    
    에이전트를 초기화하고 실행합니다.
    """
    # 에이전트 설정
    config = {
        'max_workers': 4,
        'log_level': 'INFO'
    }
    
    # 에이전트 생성 및 시작
    agent = TaskAgent("MainAgent", config)
    agent.start()
    
    try:
        agent.run()
    except KeyboardInterrupt:
        print("에이전트 종료 중...")
    finally:
        agent.stop()

if __name__ == "__main__":
    main()
```

## 모범 사례

### 1. 상태 관리
- 에이전트의 상태를 명확히 정의합니다
- 상태 전환을 메서드로 캡슐화합니다

### 2. 오류 처리
- 예외 상황에 대한 적절한 처리를 구현합니다
- 로깅을 통한 디버깅 정보를 제공합니다

### 3. 설정 관리
- 외부 설정 파일을 활용합니다
- 환경변수를 통한 동적 설정을 지원합니다

### 4. 테스트 가능한 코드
- 단위 테스트가 가능하도록 설계합니다
- Mock 객체를 활용한 테스트를 고려합니다

## 예제 구현

```python
class MonitoringAgent(BaseAgent):
    """시스템 모니터링 에이전트"""
    
    def __init__(self, name: str, interval: int = 60):
        """
        모니터링 에이전트 초기화
        
        Args:
            name (str): 에이전트 이름
            interval (int, optional): 모니터링 간격(초). Defaults to 60.
        """
        super().__init__(name)
        self.interval = interval
        self.metrics = {}
        self.alerts = []
    
    def collect_metrics(self) -> dict:
        """시스템 메트릭 수집"""
        # 구현 로직
        pass
    
    def check_thresholds(self, metrics: dict) -> list:
        """임계값 확인 및 알림 생성"""
        # 구현 로직
        pass
```

## 모듈 구조 및 Import 방식

### 1. 디렉토리 구조
권장하는 프로젝트 구조:

```
project/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── task_agent.py
│   └── monitoring_agent.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   └── logger.py
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_utils.py
├── docs/
│   ├── README.md
│   ├── ChangeLog.md
│   └── Project.md
├── main.py
└── requirements.txt
```

### 2. 모듈 Import 규칙

#### 절대 Import 사용
상대 import 대신 절대 import를 사용합니다:

```python
# 권장
from agents.base_agent import BaseAgent
from agents.task_agent import TaskAgent
from utils.config import load_config
from utils.logger import setup_logger

# 비권장
from .base_agent import BaseAgent
from ..utils.config import load_config
```

#### __init__.py 활용
각 패키지의 `__init__.py`에서 주요 클래스를 노출합니다:

```python
# agents/__init__.py
"""에이전트 모듈 패키지"""

from .base_agent import BaseAgent
from .task_agent import TaskAgent
from .monitoring_agent import MonitoringAgent

__all__ = ['BaseAgent', 'TaskAgent', 'MonitoringAgent']
```

#### 타입 Import 분리
타입 힌트용 import는 TYPE_CHECKING으로 분리합니다:

```python
from typing import TYPE_CHECKING, Dict, List, Optional
import logging

if TYPE_CHECKING:
    from agents.base_agent import BaseAgent

class AgentManager:
    def __init__(self):
        self.agents: List['BaseAgent'] = []
```

### 3. 모듈 간 통신

#### 이벤트 시스템 활용
```python
from typing import Callable, Dict, List
import threading

class EventBus:
    """에이전트 간 이벤트 통신을 위한 버스"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """이벤트 구독"""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
    
    def publish(self, event_type: str, data: dict = None) -> None:
        """이벤트 발행"""
        with self._lock:
            callbacks = self._subscribers.get(event_type, [])
            for callback in callbacks:
                callback(data or {})
```

## 문서 운영 방식

### 1. 문서 종류 및 역할

#### README.md
- 프로젝트 개요 및 설치 방법
- 빠른 시작 가이드
- 기본 사용 예제

#### Project.md
- 프로젝트 아키텍처 상세 설명
- 설계 결정사항 및 근거
- API 문서 및 클래스 다이어그램

#### ChangeLog.md
- 버전별 변경사항 기록
- 버그 수정 및 새로운 기능 추가
- 호환성 변경사항

### 2. 문서 작성 규칙

#### 버전 관리
모든 문서는 의미적 버전 관리(Semantic Versioning)를 따릅니다:
- MAJOR.MINOR.PATCH (예: 1.2.3)
- 호환성 깨지는 변경: MAJOR 증가
- 새 기능 추가: MINOR 증가  
- 버그 수정: PATCH 증가

#### 문서 업데이트 주기
- 코드 변경 시 즉시 관련 문서 업데이트
- 릴리스 전 모든 문서 검토 및 정리
- 월 단위 문서 품질 점검

### 3. 코드 내 문서화

#### 모듈 수준 docstring
```python
"""
agents.task_agent 모듈

이 모듈은 작업 처리를 위한 TaskAgent 클래스를 제공합니다.
주요 기능으로는 작업 큐 관리, 우선순위 처리, 결과 수집이 있습니다.

Classes:
    TaskAgent: 작업 처리 전용 에이전트

Examples:
    >>> from agents.task_agent import TaskAgent
    >>> agent = TaskAgent("Worker", max_workers=4)
    >>> agent.start()
"""
```

#### 클래스 및 메서드 문서화
```python
class ConfigurableAgent(BaseAgent):
    """
    설정 가능한 에이전트 기본 클래스
    
    이 클래스는 외부 설정을 통해 동작을 제어할 수 있는
    에이전트의 기본 구현을 제공합니다.
    
    Attributes:
        config_file (str): 설정 파일 경로
        runtime_config (dict): 런타임 설정 딕셔너리
        
    Examples:
        >>> agent = ConfigurableAgent("TestAgent", "config.yaml")
        >>> agent.load_config()
        >>> agent.start()
    """
    
    def load_config(self, file_path: str = None, 
                   reload: bool = False) -> dict:
        """
        설정 파일을 로드합니다
        
        Args:
            file_path (str, optional): 설정 파일 경로. 
                                     None이면 기본 경로 사용.
            reload (bool, optional): 기존 설정 덮어쓰기 여부.
                                   Defaults to False.
                                   
        Returns:
            dict: 로드된 설정 딕셔너리
            
        Raises:
            FileNotFoundError: 설정 파일이 존재하지 않는 경우
            yaml.YAMLError: YAML 파싱 오류가 발생한 경우
            
        Examples:
            >>> config = agent.load_config("custom_config.yaml")
            >>> print(config['max_workers'])
            4
        """
        pass
```

## 가상환경 및 패키지 관리 (uv 사용)

### 1. uv 설치 및 설정

#### uv 설치
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 또는 pip를 통한 설치
pip install uv
```

#### 설치 확인
```bash
uv --version
```

### 2. 프로젝트 초기화 및 가상환경 생성

#### 새 프로젝트 생성
```bash
# 프로젝트 디렉토리 생성 및 초기화
mkdir ai_literacy_project
cd ai_literacy_project
uv init
```

#### 기존 프로젝트에서 가상환경 생성
```bash
# Python 3.11을 사용하는 가상환경 생성
uv venv --python 3.11

# 기본 Python 버전으로 가상환경 생성
uv venv

# 특정 이름으로 가상환경 생성
uv venv agent_env
```

#### 가상환경 활성화
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# uv를 통한 자동 활성화 (권장)
uv shell
```

### 3. 패키지 관리

#### 의존성 설치
```bash
# pyproject.toml 기반 설치
uv sync

# 특정 패키지 설치
uv add numpy pandas pydantic

# 개발용 의존성 설치
uv add --dev pytest black flake8 mypy

# 특정 버전 설치
uv add "pydantic>=2.0,<3.0"

# 선택적 의존성 그룹 설치
uv add --optional ai torch transformers
```

#### pyproject.toml 예제
```toml
[project]
name = "ai-literacy"
version = "0.1.0"
description = "AI Agent System"
authors = [{name = "Developer", email = "dev@example.com"}]
dependencies = [
    "pydantic>=2.0",
    "pyyaml>=6.0",
    "click>=8.0",
    "loguru>=0.7.0",
]

[project.optional-dependencies]
ai = ["torch>=2.0", "transformers>=4.30"]
db = ["sqlalchemy>=2.0", "asyncpg>=0.28"]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "flake8>=6.0",
    "mypy>=1.0",
    "pre-commit>=3.0",
]

[project.scripts]
ai-agent = "ai_literacy.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.21",
]
```

#### 패키지 업데이트 및 제거
```bash
# 모든 패키지 업데이트
uv sync --upgrade

# 특정 패키지 업데이트
uv add --upgrade numpy

# 패키지 제거
uv remove pandas

# 사용하지 않는 패키지 정리
uv sync --prune
```

### 4. 프로젝트 실행

#### uv를 통한 실행
```bash
# 메인 모듈 실행
uv run python main.py

# 스크립트 실행 (pyproject.toml에 정의된 경우)
uv run ai-agent

# 개발 서버 실행
uv run python -m ai_literacy.server

# 테스트 실행
uv run pytest

# 코드 포맷팅
uv run black .
uv run flake8 .
```

#### 환경별 실행 설정
```python
# main.py
def main():
    """
    uv를 통한 애플리케이션 진입점
    
    환경변수와 설정을 통해 에이전트를 초기화하고 실행합니다.
    """
    import os
    from pathlib import Path
    
    # 프로젝트 루트 디렉토리 설정
    project_root = Path(__file__).parent
    config_path = project_root / "config" / "default.yaml"
    
    # 환경별 설정 로드
    env = os.getenv("ENVIRONMENT", "development")
    if env != "development":
        config_path = project_root / "config" / f"{env}.yaml"
    
    # 에이전트 시스템 초기화
    from agents import AgentManager
    from utils.config import load_config
    
    config = load_config(config_path)
    manager = AgentManager(config)
    
    try:
        manager.start_all()
        manager.wait_for_completion()
    except KeyboardInterrupt:
        print("에이전트 시스템 종료 중...")
    finally:
        manager.stop_all()

if __name__ == "__main__":
    main()
```

### 5. 개발 워크플로우

#### 프로젝트 설정 스크립트
```python
# scripts/setup_project.py
"""프로젝트 초기 설정 스크립트"""

import subprocess
import sys
from pathlib import Path

class ProjectSetup:
    """프로젝트 설정 관리 클래스"""
    
    def __init__(self, project_path: Path = None):
        """
        프로젝트 설정 초기화
        
        Args:
            project_path (Path, optional): 프로젝트 경로. Defaults to None.
        """
        self.project_path = project_path or Path.cwd()
        self.uv_available = self._check_uv_installation()
    
    def _check_uv_installation(self) -> bool:
        """uv 설치 확인"""
        try:
            subprocess.run(["uv", "--version"], 
                         capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def install_dependencies(self, include_dev: bool = True) -> None:
        """
        의존성 설치
        
        Args:
            include_dev (bool, optional): 개발 의존성 포함 여부. 
                                        Defaults to True.
        """
        if not self.uv_available:
            print("uv가 설치되지 않았습니다. uv를 먼저 설치하세요.")
            sys.exit(1)
        
        commands = ["uv", "sync"]
        if include_dev:
            commands.append("--dev")
        
        subprocess.run(commands, check=True)
        print("의존성 설치 완료")
    
    def setup_pre_commit(self) -> None:
        """pre-commit 훅 설정"""
        subprocess.run(["uv", "run", "pre-commit", "install"], check=True)
        print("pre-commit 훅 설정 완료")
    
    def run_tests(self) -> None:
        """테스트 실행"""
        subprocess.run(["uv", "run", "pytest", "-v"], check=True)

def main():
    """설정 스크립트 진입점"""
    setup = ProjectSetup()
    setup.install_dependencies()
    setup.setup_pre_commit()
    setup.run_tests()
    print("프로젝트 설정 완료!")

if __name__ == "__main__":
    main()
```

#### Makefile 예제
```makefile
# Makefile
.PHONY: install test lint format clean run

# 의존성 설치
install:
	uv sync --dev

# 테스트 실행
test:
	uv run pytest -v --cov=ai_literacy

# 린터 실행
lint:
	uv run flake8 ai_literacy tests
	uv run mypy ai_literacy

# 코드 포맷팅
format:
	uv run black ai_literacy tests
	uv run isort ai_literacy tests

# 정적 분석
check: lint test

# 환경 정리
clean:
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage

# 애플리케이션 실행
run:
	uv run python main.py

# 개발 서버 실행
dev:
	uv run python main.py --debug

# 프로덕션 실행
prod:
	ENVIRONMENT=production uv run python main.py
```

### 6. CI/CD 통합

#### GitHub Actions 예제
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v2
      with:
        version: "latest"
    
    - name: Set up Python ${{ matrix.python-version }}
      run: uv python install ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: uv sync --dev
    
    - name: Run tests
      run: uv run pytest --cov=ai_literacy
    
    - name: Run linting
      run: |
        uv run flake8 ai_literacy tests
        uv run mypy ai_literacy
```

### 7. 환경별 설정 관리

#### 환경 설정 파일
```yaml
# config/development.yaml
environment: development

agent:
  max_workers: 2
  timeout: 30.0
  debug: true

logging:
  level: DEBUG
  handlers: ["console"]

database:
  url: "sqlite:///data/dev.db"
```

```yaml
# config/production.yaml
environment: production

agent:
  max_workers: 8
  timeout: 300.0
  debug: false

logging:
  level: INFO
  handlers: ["file", "syslog"]

database:
  url: "${DATABASE_URL}"
  pool_size: 20
```

#### 환경별 실행
```bash
# 개발 환경
uv run python main.py

# 테스트 환경
ENVIRONMENT=testing uv run python main.py

# 프로덕션 환경
ENVIRONMENT=production uv run python main.py
```

이러한 uv 기반 워크플로우를 통해 빠르고 일관된 개발 환경을 유지하며, 의존성 관리의 복잡성을 크게 줄일 수 있습니다.
