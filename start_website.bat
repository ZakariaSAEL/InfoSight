@echo off
echo Starting InfoSight OCR Services...

:: Navigate to the project directory
cd /d "%~dp0"

:: Start FastAPI backend in a new window
echo Starting Backend (FastAPI)...
start "InfoSight Backend" cmd /k "info_sight\ocr_api\ocr_env\Scripts\python.exe -m uvicorn info_sight.ocr_api.app:app --reload"

:: Wait a moment for the backend to initialize
timeout /t 3 /nobreak > nul

:: Start Streamlit UI
echo Starting UI (Streamlit)...
info_sight\ocr_api\ocr_env\Scripts\python.exe -m streamlit run info_sight\ocr_api\ui.py

pause
