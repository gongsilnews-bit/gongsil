@echo off
setlocal
cd /d "%~dp0"

echo ================================================== >> update_log.txt
echo [%DATE% %TIME%] Auto Update Started >> update_log.txt

node ingest.js >> update_log.txt 2>&1

echo [%DATE% %TIME%] Auto Update Completed >> update_log.txt
echo ================================================== >> update_log.txt
exit /b
