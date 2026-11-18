@echo off
cd /d "%~dp0"
start http://localhost:8107/ruttetra-mobile.html
python -m http.server 8107
