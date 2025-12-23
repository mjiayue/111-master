@echo off
cd /d "%~dp0"

if not exist "database\python_learning.db" (
    echo Initializing database...
    python scripts\init_data.py
    if errorlevel 1 (
        echo Failed to initialize database!
        pause
        exit /b 1
    )
)

echo Starting system...
python main.py

if errorlevel 1 (
    echo.
    echo ================================================
    echo   Startup Failed!
    echo ================================================
    echo.
    echo Possible reasons:
    echo 1. Python not in PATH
    echo 2. Missing dependencies
    echo.
    echo Solution:
    echo Run: pip install -r requirements.txt
    echo.
    pause
)
