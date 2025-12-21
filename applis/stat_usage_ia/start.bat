@echo off
cd /d "%~dp0"
echo.
echo ============================================================
echo Demarrage Tracker Usage IA
echo ============================================================
echo.
echo Installation dependances...
pip install -r requirements.txt >nul 2>&1
echo.
echo Demarrage serveur...
echo URL: http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo ============================================================
echo.
python server.py
