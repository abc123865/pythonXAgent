@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ================================================
echo              Jump King Game Launcher
echo ================================================
echo.
echo Starting Jump King Game...
echo.

REM Try default python command
python main.py
if not errorlevel 1 goto success

echo Default Python failed, trying py launcher...
py main.py
if not errorlevel 1 goto success

echo py launcher failed, trying virtual environment Python...
if exist ".\.venv\Scripts\python.exe" (
    ".\.venv\Scripts\python.exe" main.py
    if not errorlevel 1 goto success
)

echo Trying to activate virtual environment...
if exist ".\.venv\Scripts\activate.bat" (
    call ".\.venv\Scripts\activate.bat"
    python main.py
    if not errorlevel 1 goto success
)

echo.
echo ================================================
echo              Launch Failed
echo ================================================
echo All launch methods failed. Please check:
echo 1. Python is installed
echo 2. Required packages are installed (pygame)
echo 3. Virtual environment is properly set up
echo.
echo You can manually run:
echo   python main.py
echo or
echo   py main.py
echo.
goto end

:success
echo.
echo ================================================
echo              Game Ended Normally
echo ================================================

:end
echo.
echo Press any key to close window...
pause >nul
