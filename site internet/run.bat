@echo off
title Je Geek Utile - Site Web
cd /d "%~dp0"

echo Installation des dependances...
pip install -r requirements.txt -q

echo.
echo Lancement du site...
echo Acces: http://localhost:5000
echo.

python app.py

pause
