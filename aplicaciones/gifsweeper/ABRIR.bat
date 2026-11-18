@echo off
cd /d "%~dp0"
start http://localhost:8102/index.html
python -m http.server 8102
