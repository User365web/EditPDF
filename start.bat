@echo off
cd /d "%~dp0"
echo Starting EditPDF locally...
echo Keep this window open while using the site.
start "" http://localhost:8000
python -m http.server 8000
pause
