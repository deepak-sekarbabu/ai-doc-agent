#!/bin/bash
# Build script for Linux/Mac - AI Documentation Agent

set -e

# Navigate to project root
cd "$(dirname "$0")/.."

echo "========================================"
echo "AI Documentation Agent - Build Script"
echo "========================================"
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/4] Installing dependencies..."
pip3 install -r config/requirements.txt

echo
echo "[2/4] Installing PyInstaller..."
pip3 install pyinstaller

echo
echo "[3/4] Building executable..."
python3 -m PyInstaller build/ai_agent.spec --clean

echo
echo "[4/4] Creating distribution package..."
mkdir -p dist/ai-doc-agent-bundle
cp dist/ai-doc-agent dist/ai-doc-agent-bundle/

# Copy .env if it exists, otherwise use .env.example
if [ -f .env ]; then
    cp .env dist/ai-doc-agent-bundle/.env
    echo "Using existing .env file"
elif [ -f config/.env.example ]; then
    cp config/.env.example dist/ai-doc-agent-bundle/.env
    echo "Created .env from .env.example - Please configure your settings"
    echo "Please configure your Ollama settings in the .env file" > dist/ai-doc-agent-bundle/SETUP.txt
else
    echo "WARNING: No .env file found!"
fi

cp README.md dist/ai-doc-agent-bundle/
chmod +x dist/ai-doc-agent-bundle/ai-doc-agent

echo
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo
echo "Executable location: dist/ai-doc-agent-bundle/ai-doc-agent"
echo
echo "Next steps:"
echo "1. cd dist/ai-doc-agent-bundle/"
echo "2. Edit .env file with your Ollama configuration"
echo "3. Run: ./ai-doc-agent --help"
echo
