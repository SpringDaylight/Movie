# 서버 시작 가이드

## 방법 1: 배치 파일 사용 (권장)

Windows 탐색기에서 `start_servers.bat` 파일을 더블클릭하세요.
- 백엔드 서버: http://localhost:8000
- 프론트엔드 서버: http://localhost:5174

## 방법 2: 수동 실행

### 터미널 1 - 백엔드 서버
```cmd
cd backend
..\venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 터미널 2 - 프론트엔드 서버
```cmd
cd frontend
npm run dev
```

## 확인

- 백엔드 API: http://localhost:8000/docs
- 프론트엔드: http://localhost:5174

## 주의사항

- 백엔드는 Python 가상환경(venv)이 활성화되어야 합니다
- 프론트엔드는 npm 패키지가 설치되어 있어야 합니다 (`npm install`)
- 두 서버 모두 실행 중이어야 프론트엔드에서 API를 호출할 수 있습니다
