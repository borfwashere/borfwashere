@echo off
cd /d "%~dp0"
start http://localhost:8109/web.html
python -m http.server 8109
