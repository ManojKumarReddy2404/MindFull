@echo off
echo Starting Zen Focus Application...
echo ===================================

:: Start Backend Server
start "Backend Server" cmd /k "cd /d %~dp0zen_ai && python -m venv venv && call venv\\Scripts\\activate && pip install -r requirements.txt && uvicorn zen_ai.backend.app:app --reload"

:: Wait for backend to start
timeout /t 10 /nobreak >nul

:: Start Frontend
start "Frontend" cmd /k "cd /d %~dp0zen-focus-web && npm install && npm start"

echo.
echo ===================================
echo Both services are starting...
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:19006
echo.
echo Note: The frontend may take a few minutes to start.
pause
