@echo off
REM Blockchain File Sharing System - Startup Script (Windows)

echo ========================================================
echo 🔗 BLOCKCHAIN FILE SHARING SYSTEM - STARTUP
echo ========================================================
echo.

REM Check if IPFS is installed
where ipfs >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ✗ IPFS is not installed!
    echo.
    echo Please install IPFS from: https://docs.ipfs.tech/install/
    echo Download the Windows .zip and extract to your PATH
    pause
    exit /b 1
)

echo ✓ IPFS found
ipfs --version

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ✗ Python is not installed!
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Check/Install dependencies
echo.
echo Checking Python dependencies...
python -c "import flask, requests, cryptography" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️  Missing dependencies. Installing...
    pip install -r requirements.txt
) else (
    echo ✓ All dependencies installed
)

REM Initialize IPFS if needed
if not exist "%USERPROFILE%\.ipfs" (
    echo.
    echo Initializing IPFS...
    ipfs init
)

echo.
echo ========================================================
echo IMPORTANT: You need to run IPFS daemon separately!
echo ========================================================
echo.
echo Open a NEW terminal and run:
echo   ipfs daemon
echo.
echo Then press any key to continue...
pause >nul

echo.
echo ========================================================
echo Starting Flask Web Server...
echo ========================================================
echo.

REM Start Flask app
python web_app.py

pause
