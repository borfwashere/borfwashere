@echo off
cd /d "%~dp0"
start http://localhost:8108/laberinto/screensaver.html
python -m http.server 8108
