#!/usr/bin/env pwsh
# PowerShell build script for creating Windows .exe of Pixel-Art Avatar Generator
# Requirements: Python 3.6+, pip

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Pixel-Art Avatar Generator Builder" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.6 or higher from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[1/4] Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install pygame pyinstaller

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/4] Cleaning previous build artifacts..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }

Write-Host ""
Write-Host "[3/4] Building executable with PyInstaller..." -ForegroundColor Yellow
pyinstaller --clean --onefile avatar_generator.spec

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[4/4] Copying required files to dist folder..." -ForegroundColor Yellow
if (-not (Test-Path "dist")) { New-Item -ItemType Directory -Path "dist" }
Copy-Item "color_palette.json" "dist\" -Force

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Executable location: dist\PixelAvatarGenerator.exe" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can distribute the entire 'dist' folder or just the .exe file" -ForegroundColor Yellow
Write-Host "(the color_palette.json must be in the same directory as the .exe)" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
