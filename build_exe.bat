@echo off
REM Build script for creating Windows .exe of Pixel-Art Avatar Generator
REM Requirements: Python 3.6+, pip

echo ====================================
echo Pixel-Art Avatar Generator Builder
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install pygame pyinstaller

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Cleaning previous build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo [3/4] Building executable with PyInstaller...
pyinstaller --clean --onefile avatar_generator.spec

if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [4/4] Copying required files to dist folder...
if not exist dist mkdir dist
copy color_palette.json dist\ >nul

echo.
echo ====================================
echo Build completed successfully!
echo ====================================
echo.
echo Executable location: dist\PixelAvatarGenerator.exe
echo.
echo You can distribute the entire 'dist' folder or just the .exe file
echo (the color_palette.json must be in the same directory as the .exe)
echo.
pause
