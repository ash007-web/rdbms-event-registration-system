@echo off
setlocal

echo ========================================================
echo  Event Registration System Launcher
echo ========================================================
echo.

:: 1. Check if MySQL is running
echo [1/4] Checking MySQL service...
tasklist /FI "IMAGENAME eq mysqld.exe" 2>NUL | find /I /N "mysqld.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo       MySQL is running.
) else (
    echo       [WARNING] MySQL ^(mysqld.exe^) is not running!
    echo       Please start your MySQL server ^(e.g., via XAMPP, WAMP, or Windows Services^)
    echo       and run this launcher again.
    echo.
    pause
    exit /b
)

:: 2. Activate Virtual Environment
echo.
echo [2/4] Checking Virtual Environment...
if exist "venv\Scripts\activate.bat" (
    echo       Activating venv...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo       Activating .venv...
    call .venv\Scripts\activate.bat
) else (
    echo       [WARNING] No virtual environment found at 'venv' or '.venv'.
    echo       Ensure required packages are installed globally.
)

:: 3. Start Flask
echo.
echo [3/4] Starting Flask Server...
start "EventReg Server" cmd /c "python app.py"

:: 4. Wait for Flask to start
echo       Waiting for server to initialize...
timeout /t 3 /nobreak >nul

:: 5. Open Chrome
echo.
echo [4/4] Opening Google Chrome...
start chrome "http://127.0.0.1:5000" || start "http://127.0.0.1:5000"

echo.
echo ========================================================
echo  System is running.
echo  To stop the server, run stop.bat or close the 
echo  "EventReg Server" window.
echo ========================================================
pause
