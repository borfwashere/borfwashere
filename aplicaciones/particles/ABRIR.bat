@echo off
cd /d "%~dp0"
start http://localhost:8104/dit.html
python -m http.server 8104
