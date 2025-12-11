@echo off
REM GhostTrack Build Script for Windows
REM This script installs PyInstaller and builds the executable

echo ============================================
echo    GhostTrack Executable Builder
echo ============================================
echo.

echo [1/3] Installing PyInstaller...
pip install pyinstaller
echo.

echo [2/3] Building executable...
pyinstaller --onefile --name GhostTrack --clean GhostTR.py
echo.

echo [3/3] Build complete!
echo.
echo Your executable is located at: dist\GhostTrack.exe
echo.

pause
