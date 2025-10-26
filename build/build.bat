@echo off
REM Build script for Windows - AI Documentation Agent

echo ========================================
echo AI Documentation Agent - Build Script
echo ========================================
echo.

cd /d "%~dp0\.."

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install -r config\requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo.
echo [2/4] Installing PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo ERROR: Failed to install PyInstaller
    exit /b 1
)

echo.
echo [3/4] Building executable...
python -m PyInstaller build\ai_agent.spec --clean
if %errorlevel% neq 0 (
    echo ERROR: Failed to build executable
    exit /b 1
)

echo.
echo [4/4] Creating distribution package...
if not exist "dist\ai-doc-agent-bundle\" mkdir "dist\ai-doc-agent-bundle"
copy "dist\ai-doc-agent.exe" "dist\ai-doc-agent-bundle\"

REM Copy .env if it exists, otherwise use .env.example
if exist ".env" (
    copy ".env" "dist\ai-doc-agent-bundle\.env"
    echo Using existing .env file
) else if exist "config\.env.example" (
    copy "config\.env.example" "dist\ai-doc-agent-bundle\.env"
    echo Created .env from .env.example - Please configure your settings
    echo Please configure your Ollama settings in the .env file > "dist\ai-doc-agent-bundle\SETUP.txt"
) else (
    echo WARNING: No .env file found!
)

copy "README.md" "dist\ai-doc-agent-bundle\"

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Executable location: dist\ai-doc-agent-bundle\ai-doc-agent.exe
echo.
echo Next steps:
echo 1. Navigate to: dist\ai-doc-agent-bundle\
echo 2. Edit .env file with your Ollama configuration
echo 3. Run: ai-doc-agent.exe --help
echo.
pause
