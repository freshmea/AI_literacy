# AI Literacy Project

## 프로젝트 개요

AI Literacy는 인공지능 에이전트 시스템을 구현하고 학습하기 위한 Python 프로젝트입니다. 다양한 타입의 에이전트를 클래스 기반으로 구현하여 자동화된 작업 처리, 모니터링, 데이터 분석 등의 기능을 제공합니다.

## 주요 기능

- **모듈형 에이전트 시스템**: 확장 가능한 클래스 기반 아키텍처
- **작업 큐 관리**: 우선순위 기반 작업 스케줄링
- **이벤트 기반 통신**: 에이전트 간 느슨한 결합 통신
- **설정 관리**: YAML/JSON 기반 외부 설정 지원
- **로깅 및 모니터링**: 상세한 실행 로그 및 성능 메트릭

## 설치 방법

### 필수 요구사항
- Python 3.8 이상
- pip 또는 conda 패키지 관리자

### 설치 단계

1. 저장소 복제
```bash
git clone https://github.com/username/AI_literacy.git
cd AI_literacy
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

## 빠른 시작

### 기본 사용법

```python
from agents import TaskAgent
from utils.config import load_config

def main():
    """기본 에이전트 실행 예제"""
    # 설정 로드
    config = load_config("config/default.yaml")
    
    # 에이전트 생성
    agent = TaskAgent(
        name="QuickStartAgent",
        config=config,
        max_workers=2,
        timeout=30.0
    )
    
    # 작업 추가
    agent.add_task({
        'type': 'data_processing',
        'input_file': 'data/sample.csv',
        'output_file': 'results/processed.csv'
    }, priority=1)
    
    # 에이전트 실행
    try:
        agent.start()
        agent.run()
    except KeyboardInterrupt:
        print("사용자에 의해 중단됨")
    finally:
        agent.stop()

if __name__ == "__main__":
    main()
```

### 설정 파일 예제

```yaml
# config/default.yaml
agent:
  max_workers: 4
  timeout: 60.0
  retry_count: 3
  
logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  
database:
  url: "sqlite:///data/agents.db"
  pool_size: 5
```

## 프로젝트 구조

```
AI_literacy/
├── agents/              # 에이전트 모듈
│   ├── base_agent.py   # 기본 에이전트 클래스
│   ├── task_agent.py   # 작업 처리 에이전트
│   └── monitoring_agent.py  # 모니터링 에이전트
├── utils/              # 유틸리티 모듈
│   ├── config.py       # 설정 관리
│   ├── logger.py       # 로깅 설정
│   └── database.py     # 데이터베이스 연동
├── tests/              # 테스트 코드
├── docs/               # 문서
├── config/             # 설정 파일
├── data/               # 데이터 파일
└── main.py            # 진입점
```

## 문서

- [프로젝트 상세 문서](docs/Project.md)
- [변경 사항](docs/ChangeLog.md)
- [에이전트 모드 지침](.github/AGENT.md)

## 기여 방법

1. Fork 저장소
2. 기능 브랜치 생성 (`git checkout -b feature/새기능`)
3. 변경사항 커밋 (`git commit -am '새기능 추가'`)
4. 브랜치에 Push (`git push origin feature/새기능`)
5. Pull Request 생성

## 라이센스

이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 연락처

- 이메일: maintainer@example.com
- 이슈 트래커: [GitHub Issues](https://github.com/username/AI_literacy/issues)
