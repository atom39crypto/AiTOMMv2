@echo off
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
call .\AiTOMM\Scripts\activate.bat
python run.py
pause
