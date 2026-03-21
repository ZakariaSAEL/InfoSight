@echo off
echo Starting InfoSight UI (Streamlit)...

:: Navigate to the project directory
cd /d "%~dp0"

:: Start Streamlit UI directly
info_sight\ocr_api\ocr_env\Scripts\python.exe -m streamlit run info_sight\ocr_api\ui.py

pause
