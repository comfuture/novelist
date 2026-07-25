@echo off
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 "%~dp0create_scaffold.py" %*
) else (
  python "%~dp0create_scaffold.py" %*
)
exit /b %ERRORLEVEL%
