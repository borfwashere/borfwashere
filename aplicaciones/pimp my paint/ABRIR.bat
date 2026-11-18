@echo off
cd /d "%~dp0"
start http://localhost:8105/pimpmypaint/index.html
python -m http.server 8105
