@echo off
cd /d "%~dp0"

echo ========================================
echo   EVENT REGISTRATION SYSTEM
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not available in PATH.
    echo Please install Python and try again.
    pause
    exit /b
)

python -c "import mysql.connector" >nul 2>&1
if errorlevel 1 (
    echo mysql-connector-python is not installed.
    echo Installing required package...
    python -m pip install mysql-connector-python
    if errorlevel 1 (
        echo.
        echo Failed to install mysql-connector-python.
        pause
        exit /b
    )
)

echo Starting Event Registration System...
echo.

python app.py

echo.
echo ========================================
echo   Application closed
echo ========================================
pause
