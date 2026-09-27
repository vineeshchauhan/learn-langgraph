@echo off
echo ========================================
echo  Python Virtual Environment Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found: 
python --version
echo.

REM Check if virtual environment already exists
if exist "my_env\" (
    echo Virtual environment 'my_env' already exists.
    set /p confirm="Do you want to recreate it? (yes/no): "
    if /i not "%confirm%"=="yes" (
        echo Setup cancelled.
        pause
        exit /b 0
    )
    echo Removing existing environment...
    rmdir /s /q my_env
    echo.
)

echo [2/4] Creating virtual environment...
python -m venv my_env
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [3/4] Activating virtual environment...
call my_env\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Activated!
echo.

echo [4/4] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ========================================
    echo  WARNING: Some packages failed to install
    echo ========================================
    echo.
    echo Installation completed but some packages may be missing.
    echo Check the errors above and try installing manually:
    echo     pip install -r requirements.txt
    echo.
) else (
    echo.
    echo ========================================
    echo  SUCCESS! Environment is ready to use
    echo ========================================
    echo.
    echo To activate this environment in the future, run:
    echo     my_env\Scripts\activate.bat
    echo.
    echo To deactivate, run:
    echo     deactivate
    echo.
)

REM Show installed packages
echo Installed packages:
pip list --format=columns
echo.

pause