# GhostTrack Build Script for PowerShell
# This script installs PyInstaller and builds the executable

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   GhostTrack Executable Builder" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller
Write-Host ""

Write-Host "[2/3] Building executable..." -ForegroundColor Yellow
pyinstaller --onefile --name GhostTrack --clean GhostTR.py
Write-Host ""

Write-Host "[3/3] Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Your executable is located at: dist\GhostTrack.exe" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
