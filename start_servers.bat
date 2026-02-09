@echo off
echo Starting Backend and Frontend Servers...
echo.

REM Start Backend Server
echo [1/2] Starting Backend Server (Port 8000)...
start "Backend Server" cmd /k "cd backend && ..\\venv\\Scripts\\python.exe -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak > nul

REM Start Frontend Server
echo [2/2] Starting Frontend Server (Port 5173)...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Servers are starting!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to exit...
pause > nul
