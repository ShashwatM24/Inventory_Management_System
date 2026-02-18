@echo off
setlocal

echo ========================================
echo   Starting Inventory Management System
echo ========================================

:: Check if venv exists
if not exist "venv" (
    echo [INFO] Virtual environment not found. Creating one...
    python -m venv venv
) else (
    echo [INFO] Virtual environment found.
)

:: Activate venv
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

:: Check for requirements.txt
if exist "requirements.txt" (
    echo [INFO] Installing/Updating dependencies...
    pip install -r requirements.txt > nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b %errorlevel%
    )
    echo [INFO] Dependencies installed.
) else (
    echo [WARNING] requirements.txt not found! Skipping dependency installation.
)

:: Run the app
echo [INFO] Launching Streamlit app...
streamlit run app.py

:: Pause on exit so user can see errors
if %errorlevel% neq 0 (
    echo [ERROR] Application crashed or failed to start.
    pause
)
