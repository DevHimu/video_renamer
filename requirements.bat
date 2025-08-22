@echo off
title === Installing Python Requirements ===
echo.
echo ===============================
echo   Installing Required Packages
echo ===============================
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install required libraries
pip install pymediainfo questionary rich

echo.
echo ===============================
echo   Requirements Installed Done!
echo ===============================
pause
