@echo off
cd /d "%~dp0"
start http://localhost:8101/3dexp.html
python -m http.server 8101
