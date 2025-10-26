# AI Documentation Agent - Bundling Guide

This guide explains different ways to bundle and distribute the AI Documentation Agent.

**Note:** All paths updated for the new organized project structure.

## Table of Contents

1. [Standalone Executable (PyInstaller)](#1-standalone-executable-pyinstaller)
2. [Docker Container](#2-docker-container)
3. [Python Package (pip)](#3-python-package-pip)
4. [Portable Zip Bundle](#4-portable-zip-bundle)

---

## 1. Standalone Executable (PyInstaller)

Creates a single executable file that can run without Python installed.

### Windows

```bash
# Run the build script from project root
cd build
build.bat

# Or manually from project root:
pip install pyinstaller
python -m PyInstaller build/ai_agent.spec --clean
```

**Output**: `dist\ai-doc-agent-bundle\ai-doc-agent.exe`

### Linux/Mac

```bash
# Make script executable and run from build directory
cd build
chmod +x build.sh
./build.sh

# Or manually from project root:
pip3 install pyinstaller
python3 -m PyInstaller build/ai_agent.spec --clean
```

**Output**: `dist/ai-doc-agent-bundle/ai-doc-agent`

### Distribution

The bundle includes:
- Executable file
- `.env` configuration file
- `README.md`
- `SETUP.txt` with instructions

Share the entire `ai-doc-agent-bundle` folder.

### Pros & Cons

✅ No Python required on target system  
✅ Easy to distribute  
✅ Single executable  
❌ Large file size (~50-100 MB)  
❌ Platform-specific (need separate builds for Windows/Linux/Mac)  
❌ Some antivirus software may flag it

---

## 2. Docker Container

Containerized deployment for consistent cross-platform execution.

### Build Docker Image

```bash
# Build the image from build directory
cd build
docker build -t ai-doc-agent .

# Or use docker-compose
docker-compose build
```

### Run with Docker

```bash
# Basic usage
docker run --rm -v "$(pwd):/workspace" ai-doc-agent --directory /workspace

# With custom options
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=http://host.docker.internal:11434/api/generate \
  -e MODEL_NAME=llama2:7b \
  ai-doc-agent --directory /workspace --format html --iterations 5
```

### Run with Docker Compose

```bash
# Start and run
docker-compose run --rm ai-doc-agent --directory /workspace

# With custom command
docker-compose run --rm ai-doc-agent --directory /workspace --format pdf --verbose
```

### Distribution

```bash
# Save image to file
docker save ai-doc-agent:latest | gzip > ai-doc-agent.tar.gz

# Load on target system
gunzip -c ai-doc-agent.tar.gz | docker load

# Or push to Docker Hub
docker tag ai-doc-agent deepak-sekarbabu/ai-doc-agent
docker push deepak-sekarbabu/ai-doc-agent
```

### Pros & Cons

✅ Cross-platform consistency  
✅ Isolated environment  
✅ Easy dependency management  
✅ Reproducible builds  
❌ Requires Docker installed  
❌ Larger download size  
❌ Learning curve for Docker

---

## 3. Python Package (pip)

Install as a Python package for easy distribution via PyPI or direct installation.

### Create Package

```bash
# Install build tools
pip install build twine

# Build package from project root
python -m build

# This creates:
# - dist/ai-doc-agent-2.0.0.tar.gz
# - dist/ai_doc_agent-2.0.0-py3-none-any.whl
```

### Install Locally

```bash
# From source directory
pip install .

# From wheel file
pip install dist/ai_doc_agent-2.0.0-py3-none-any.whl

# Editable mode (for development)
pip install -e .
```

### Use After Installation

```bash
# Commands are now available globally
ai-doc-agent --help
doc-generator --help

# Run from anywhere
ai-doc-agent --directory ~/my-project --format html
```

### Publish to PyPI (Optional)

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*

# Users can then install via:
pip install ai-doc-agent
```

### Distribution

Share the wheel file or publish to PyPI for `pip install`.

### Pros & Cons

✅ Easy installation with pip  
✅ Proper Python packaging  
✅ Easy updates  
✅ Small file size  
❌ Requires Python installed  
❌ Manual dependency management for users  
✅ Can be published to PyPI

---

## 4. Portable Zip Bundle

Simple portable bundle without compilation.

### Create Bundle

**Windows:**
```bash
# Create bundle directory (from project root)
mkdir ai-doc-agent-portable
mkdir ai-doc-agent-portable\src
mkdir ai-doc-agent-portable\config

copy src\*.py ai-doc-agent-portable\src\
copy config\requirements.txt ai-doc-agent-portable\config\
copy config\.env.example ai-doc-agent-portable\.env
copy README.md ai-doc-agent-portable\

# Create run script
echo @echo off > ai-doc-agent-portable\run.bat
echo python src\ai_agent.py %%* >> ai-doc-agent-portable\run.bat

# Zip it
powershell Compress-Archive -Path ai-doc-agent-portable -DestinationPath ai-doc-agent-portable.zip
```

**Linux/Mac:**
```bash
# Create bundle directory (from project root)
mkdir -p ai-doc-agent-portable/src
mkdir -p ai-doc-agent-portable/config

cp src/*.py ai-doc-agent-portable/src/
cp config/requirements.txt ai-doc-agent-portable/config/
cp config/.env.example ai-doc-agent-portable/.env
cp README.md ai-doc-agent-portable/

# Create run script
cat > ai-doc-agent-portable/run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 src/ai_agent.py "$@"
EOF
chmod +x ai-doc-agent-portable/run.sh

# Tar it
tar -czf ai-doc-agent-portable.tar.gz ai-doc-agent-portable/
```

### Usage

1. Extract the zip/tar.gz
2. Install dependencies: `pip install -r config/requirements.txt`
3. Configure `.env` file
4. Run: `./run.sh --help` (or `run.bat --help` on Windows)

### Pros & Cons

✅ Simplest method  
✅ Small file size  
✅ Easy to modify  
❌ Requires Python installed  
❌ Users must install dependencies  
❌ Platform-specific scripts

---

## Comparison Table

| Method | File Size | Python Required | Cross-Platform | Ease of Use | Best For |
|--------|-----------|-----------------|----------------|-------------|----------|
| **PyInstaller** | ~50-100 MB | ❌ No | ⚠️ Per-platform | ⭐⭐⭐⭐⭐ | Non-technical users |
| **Docker** | ~200-300 MB | ❌ No* | ✅ Yes | ⭐⭐⭐ | Developers, CI/CD |
| **pip Package** | ~50 KB | ✅ Yes | ✅ Yes | ⭐⭐⭐⭐ | Python developers |
| **Zip Bundle** | ~50 KB | ✅ Yes | ⚠️ With scripts | ⭐⭐ | Quick sharing |

*Requires Docker installed

---

## Recommended Approach by Use Case

### For End Users (Non-Developers)
→ **PyInstaller Executable**
- No setup required
- Just download and run

### For Development Teams
→ **Docker Container**
- Consistent environment
- Easy CI/CD integration

### For Python Developers
→ **pip Package**
- Familiar workflow
- Easy integration with other tools

### For Quick Testing/Sharing
→ **Zip Bundle**
- Fastest to create
- Easy to modify

---

## Security Considerations

### PyInstaller
- Executables may be flagged by antivirus
- Use code signing on Windows
- Verify checksums when distributing

### Docker
- Keep base images updated
- Scan images for vulnerabilities: `docker scan ai-doc-agent`
- Use minimal base images

### pip Package
- Use virtual environments
- Verify package integrity
- Pin dependency versions

---

## Testing Your Bundle

After creating any bundle, test it:

```bash
# Test basic functionality
[your-bundle-command] --help

# Test with a small project
[your-bundle-command] --directory ./test-project --max-files 5

# Test different formats
[your-bundle-command] --format markdown
[your-bundle-command] --format html
[your-bundle-command] --format pdf

# Test with verbose logging
[your-bundle-command] --verbose
```

---

## Troubleshooting

### PyInstaller Issues

**Problem**: Missing modules
```bash
# Add to hiddenimports in build/ai_agent.spec
hiddenimports=['missing_module']
```

**Problem**: Large executable size
```bash
# Use one-folder mode instead
python -m PyInstaller build/ai_agent.spec --onedir
```

### Docker Issues

**Problem**: Cannot connect to host Ollama
```bash
# Use host network mode
docker run --network host ...
```

**Problem**: Permission issues
```bash
# Run with user permissions
docker run --user $(id -u):$(id -g) ...
```

### pip Package Issues

**Problem**: Dependencies not installing
```bash
# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel
```

---

## Next Steps

1. Choose your bundling method
2. Follow the appropriate section above
3. Test thoroughly
4. Distribute to users
5. Provide documentation and support

For questions or issues, check the [complete guide](../guide.md).

## Project Structure Reference

With the new organized structure:

```
Docgenerator/
├── src/              # Source code (ai_agent.py, doc_generator.py)
├── config/           # Configuration (.env.example, requirements.txt)
├── build/            # Build scripts and configs
├── docs/             # Documentation
├── examples/         # Sample projects
├── tests/            # Unit tests
├── output/           # Generated documentation
├── run.py            # Quick launcher
└── setup.py          # Package configuration
```

All build scripts automatically handle the new structure.

---

**Quick Navigation:**
- [Complete Guide](../guide.md)
