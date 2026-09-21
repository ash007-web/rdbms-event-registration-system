@echo off
echo ========================================================
echo  Stopping Event Registration System...
echo ========================================================
echo.

taskkill /FI "WINDOWTITLE eq EventReg Server*" /T /F >nul 2>&1

echo Server stopped successfully.
echo.
pause
