@echo off
title JARVIS Command Prompt
cd /d "%~dp0"
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)
cmd.exe /k "echo ======================================== && echo JARVIS Environment Ready && echo ========================================"
