@echo off
REM Abre el dashboard en el navegador
cd /d "%~dp0"
.venv\Scripts\python.exe -m streamlit run dashboard.py
