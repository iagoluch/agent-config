@echo off
setlocal
set "BRAIN_SCRIPT=%USERPROFILE%\.claude\brain\hooks\brain_hook.py"
if not exist "%BRAIN_SCRIPT%" exit /b 0
py -3 "%BRAIN_SCRIPT%" %*
if errorlevel 1 python "%BRAIN_SCRIPT%" %*
exit /b 0
