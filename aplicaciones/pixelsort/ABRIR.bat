@echo off
cd /d "%~dp0"
start http://localhost:8106/pixelborf.html
python -m http.server 8106
