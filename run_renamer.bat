@echo off
title === HIMU ===

echo.
echo ====================================================
echo                Renamer by HIMU
echo ====================================================
echo.

REM --------------------------
REM Check if Python is installed
REM --------------------------
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.x and try again.
    pause
    exit /b
)

REM --------------------------
REM Check if pip is available
REM --------------------------
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] pip is not installed or not in PATH.
    echo Please install pip and try again.
    pause
    exit /b
)

REM --------------------------
REM Check for pymediainfo
REM --------------------------
python -c "import pymediainfo" >nul 2>&1
IF ERRORLEVEL 1 (
    echo [INFO] pymediainfo not found. Installing...
    pip install pymediainfo
)

REM --------------------------
REM Check for questionary
REM --------------------------
python -c "import questionary" >nul 2>&1
IF ERRORLEVEL 1 (
    echo [INFO] questionary not found. Installing...
    pip install questionary
)

REM --------------------------
REM Check for rich
REM --------------------------
python -c "import rich" >nul 2>&1
IF ERRORLEVEL 1 (
    echo [INFO] rich not found. Installing...
    pip install rich
)

REM --------------------------
REM Check for mkvmerge (MKVToolNix)
REM --------------------------
where mkvmerge >nul 2>&1
IF ERRORLEVEL 1 (
    echo [WARNING] mkvmerge not found!
    echo Please install MKVToolNix and ensure mkvmerge.exe is in PATH.
    pause
    exit /b
)

echo.
echo [INFO] All dependencies satisfied. Starting renamer...
echo.

REM --------------------------
REM Run the renamer script
REM --------------------------
python renamer.py

echo.
echo ====================================================
echo      Task Finished Succesfully
echo ====================================================
pause
