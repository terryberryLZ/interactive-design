# Quick Start Script for AI Avatar Generator
# This script helps you get started quickly

Write-Host "🎨 AI Fantasy Avatar Generator - Quick Start" -ForegroundColor Cyan
Write-Host "=" -repeat 50 -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "   Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if LoRA file exists
Write-Host "Checking LoRA model file..." -ForegroundColor Yellow
if (Test-Path "pixel-art-xl-v1.1.safetensors") {
    $fileSize = (Get-Item "pixel-art-xl-v1.1.safetensors").Length / 1MB
    Write-Host "✅ Found: pixel-art-xl-v1.1.safetensors ($([math]::Round($fileSize, 2)) MB)" -ForegroundColor Green
} else {
    Write-Host "⚠️  Warning: pixel-art-xl-v1.1.safetensors not found!" -ForegroundColor Yellow
    Write-Host "   The generator will work with base SDXL model" -ForegroundColor Yellow
    Write-Host "   but results may not be as pixel-art styled." -ForegroundColor Yellow
}

Write-Host ""

# Ask user what to do
Write-Host "What would you like to do?" -ForegroundColor Cyan
Write-Host "1. Install dependencies (first time setup)" -ForegroundColor White
Write-Host "2. Run AI Avatar Generator" -ForegroundColor White
Write-Host "3. Install dependencies AND run generator" -ForegroundColor White
Write-Host "4. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
        Write-Host "   This may take 5-10 minutes..." -ForegroundColor Yellow
        Write-Host ""
        
        pip install -r requirements.txt
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Installation complete!" -ForegroundColor Green
            Write-Host ""
            Write-Host "You can now run: python ai_avatar_generator.py" -ForegroundColor Cyan
        } else {
            Write-Host ""
            Write-Host "❌ Installation failed. Please check the errors above." -ForegroundColor Red
        }
    }
    "2" {
        Write-Host ""
        Write-Host "🚀 Starting AI Avatar Generator..." -ForegroundColor Green
        Write-Host ""
        python ai_avatar_generator.py
    }
    "3" {
        Write-Host ""
        Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
        Write-Host "   This may take 5-10 minutes..." -ForegroundColor Yellow
        Write-Host ""
        
        pip install -r requirements.txt
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Installation complete!" -ForegroundColor Green
            Write-Host ""
            Write-Host "🚀 Starting AI Avatar Generator..." -ForegroundColor Green
            Write-Host ""
            python ai_avatar_generator.py
        } else {
            Write-Host ""
            Write-Host "❌ Installation failed. Cannot start generator." -ForegroundColor Red
        }
    }
    "4" {
        Write-Host ""
        Write-Host "Goodbye! 👋" -ForegroundColor Cyan
        exit 0
    }
    default {
        Write-Host ""
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
