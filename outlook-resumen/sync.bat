@echo off
REM Sincroniza los correos (para el Programador de tareas de Windows)
cd /d "%~dp0"
.venv\Scripts\python.exe sync.py
