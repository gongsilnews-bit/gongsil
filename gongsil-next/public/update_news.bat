@echo off
setlocal
cd /d "%~dp0"

echo.
echo ====================================
echo [Gongsil News] Update Started
echo %date% %time%
echo ====================================
echo.

:: package check
if not exist "node_modules" (
    echo [ERROR] node_modules folder not found.
    echo Please run 'npm install' first.
    pause
    exit /b
)

:: Run script
node ingest.js

echo.
echo ====================================
echo [Gongsil News] Update Complete!
echo %date% %time%
echo ====================================
echo.

:: Wait 5 seconds before closing
timeout /t 5
exit /b
