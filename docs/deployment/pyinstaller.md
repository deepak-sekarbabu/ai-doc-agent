# PyInstaller Deployment

Create standalone executables for the AI Documentation Agent that run without Python installation.

## Overview

PyInstaller bundles the Python application and all its dependencies into a single executable file. Users can run the agent without installing Python, making it perfect for distribution to non-technical users.

## Benefits

✅ **No Python required** - Runs on systems without Python  
✅ **Easy distribution** - Single executable file  
✅ **Simple for users** - Download and run  
✅ **Self-contained** - All dependencies included  
✅ **Professional deployment** - Production-ready

## Prerequisites

### Development System Requirements

- Python 3.8 or higher installed
- pip package manager
- ~500 MB free disk space for build
- Administrative/sudo privileges (for some systems)

### Install PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Verify installation
pyinstaller --version
```

## Quick Build

### Windows

```bash
# Navigate to build directory
cd build

# Run build script
build.bat

# Output: dist/ai-doc-agent-bundle/ai-doc-agent.exe
```

### Linux/macOS

```bash
# Navigate to build directory
cd build

# Make script executable
chmod +x build.sh

# Run build script
./build.sh

# Output: dist/ai-doc-agent-bundle/ai-doc-agent
```

## Manual Build Process

### Step-by-Step Build

#### 1. Install Dependencies

```bash
# From project root
pip install -r config/requirements.txt
pip install pyinstaller
```

#### 2. Build Executable

```bash
# From project root
python -m PyInstaller build/ai_agent.spec --clean
```

#### 3. Create Distribution Bundle

**Windows:**
```bash
# Create bundle directory
mkdir dist\ai-doc-agent-bundle

# Copy executable
copy dist\ai-doc-agent.exe dist\ai-doc-agent-bundle\

# Copy configuration
copy config\.env.example dist\ai-doc-agent-bundle\.env

# Copy documentation
copy README.md dist\ai-doc-agent-bundle\
```

**Linux/macOS:**
```bash
# Create bundle directory
mkdir -p dist/ai-doc-agent-bundle

# Copy executable
cp dist/ai-doc-agent dist/ai-doc-agent-bundle/

# Make executable
chmod +x dist/ai-doc-agent-bundle/ai-doc-agent

# Copy configuration
cp config/.env.example dist/ai-doc-agent-bundle/.env

# Copy documentation
cp README.md dist/ai-doc-agent-bundle/
```

## Build Output

### Directory Structure

```
dist/
└── ai-doc-agent-bundle/
    ├── ai-doc-agent[.exe]    # Executable
    ├── .env                  # Configuration template
    ├── README.md             # Documentation
    └── SETUP.txt             # Setup instructions
```

### File Sizes

| Platform | Executable Size | Bundle Size |
|----------|----------------|-------------|
| Windows | ~45-55 MB | ~50 MB |
| Linux | ~50-60 MB | ~55 MB |
| macOS | ~50-60 MB | ~55 MB |

## PyInstaller Spec File

The `ai_agent.spec` file configures the build:

```python
# build/ai_agent.spec
a = Analysis(
    ['../src/ai_agent.py'],           # Main script
    pathex=['../src'],                # Python path
    binaries=[],                       # Binary dependencies
    datas=[
        ('../config/.env.example', 'config'),  # Data files
        ('../docs/README.md', 'docs'),
    ],
    hiddenimports=[                    # Hidden imports
        'requests',
        'dotenv',
        'markdown',
        'pdfkit',
    ],
    excludes=[],                       # Excluded modules
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='ai-doc-agent',              # Executable name
    debug=False,
    strip=False,
    upx=True,                          # UPX compression
    console=True,                      # Console application
)
```

### Customizing the Spec File

#### Add Hidden Imports

```python
hiddenimports=[
    'requests',
    'dotenv',
    'your_custom_module',  # Add your module
],
```

#### Include Additional Files

```python
datas=[
    ('../config/.env.example', 'config'),
    ('../templates/*.html', 'templates'),  # Add templates
    ('../assets/*', 'assets'),             # Add assets
],
```

#### Change Output Name

```python
exe = EXE(
    ...
    name='my-custom-name',  # Custom executable name
    ...
)
```

#### Disable Console Window (Windows)

```python
exe = EXE(
    ...
    console=False,  # No console window
    ...
)
```

## Distribution

### Creating a Distributable Package

#### Windows - ZIP Archive

```bash
# From project root
cd dist
powershell Compress-Archive -Path ai-doc-agent-bundle -DestinationPath ai-doc-agent-windows.zip

# Distribute: ai-doc-agent-windows.zip
```

#### Windows - Installer (Optional)

Use tools like:
- [Inno Setup](https://jrsoftware.org/isinfo.php)
- [NSIS](https://nsis.sourceforge.io/)
- [WiX Toolset](https://wixtoolset.org/)

#### Linux - TAR Archive

```bash
# From project root
cd dist
tar -czf ai-doc-agent-linux.tar.gz ai-doc-agent-bundle/

# Distribute: ai-doc-agent-linux.tar.gz
```

#### macOS - DMG (Optional)

```bash
# Create DMG with create-dmg
brew install create-dmg

create-dmg \
  --volname "AI Documentation Agent" \
  --window-pos 200 120 \
  --window-size 600 400 \
  ai-doc-agent.dmg \
  dist/ai-doc-agent-bundle/
```

### Distribution Checklist

Before distributing, ensure bundle includes:

- ✅ Executable file
- ✅ `.env` configuration template
- ✅ `README.md` with usage instructions
- ✅ `SETUP.txt` with setup steps
- ✅ License file (if applicable)

## User Setup Instructions

### Windows Users

```
1. Extract ai-doc-agent-windows.zip
2. Navigate to ai-doc-agent-bundle folder
3. Edit .env file:
   - Set OLLAMA_API_URL
   - Set MODEL_NAME
4. Open Command Prompt in this folder
5. Run: ai-doc-agent.exe --help
```

### Linux/macOS Users

```
1. Extract ai-doc-agent-linux.tar.gz
2. Navigate to ai-doc-agent-bundle folder
3. Make executable: chmod +x ai-doc-agent
4. Edit .env file:
   - Set OLLAMA_API_URL
   - Set MODEL_NAME
5. Run: ./ai-doc-agent --help
```

## Usage After Installation

### Windows

```bash
# Navigate to bundle directory
cd path\to\ai-doc-agent-bundle

# Show help
ai-doc-agent.exe --help

# Generate documentation
ai-doc-agent.exe --directory C:\Projects\MyApp

# With options
ai-doc-agent.exe --directory C:\Projects\MyApp --format html --iterations 5
```

### Linux/macOS

```bash
# Navigate to bundle directory
cd path/to/ai-doc-agent-bundle

# Show help
./ai-doc-agent --help

# Generate documentation
./ai-doc-agent --directory ~/Projects/MyApp

# With options
./ai-doc-agent --directory ~/Projects/MyApp --format html --iterations 5
```

### Add to PATH (Optional)

**Windows:**
```bash
# Add to PATH environment variable
setx PATH "%PATH%;C:\path\to\ai-doc-agent-bundle"

# Now can run from anywhere
ai-doc-agent --help
```

**Linux/macOS:**
```bash
# Add to PATH
echo 'export PATH=$PATH:/path/to/ai-doc-agent-bundle' >> ~/.bashrc
source ~/.bashrc

# Now can run from anywhere
ai-doc-agent --help
```

## Troubleshooting

### Build Issues

#### PyInstaller Not Found

```bash
# Ensure PyInstaller is installed
pip install --upgrade pyinstaller

# Check installation
pyinstaller --version
```

#### Missing Modules Error

```bash
# Add to hiddenimports in ai_agent.spec
hiddenimports=[
    'requests',
    'dotenv',
    'missing_module_name',  # Add here
],

# Rebuild
python -m PyInstaller build/ai_agent.spec --clean
```

#### Import Error During Build

```bash
# Install all dependencies first
pip install -r config/requirements.txt

# Clean build
python -m PyInstaller build/ai_agent.spec --clean
```

#### Large Executable Size

```bash
# Enable UPX compression in spec file
upx=True

# Or use one-folder mode (smaller but multiple files)
python -m PyInstaller build/ai_agent.spec --onedir
```

### Runtime Issues

#### Executable Won't Run

**Windows:**
```bash
# Run from Command Prompt to see errors
cmd
cd path\to\ai-doc-agent-bundle
ai-doc-agent.exe --help
```

**Linux/macOS:**
```bash
# Check permissions
chmod +x ai-doc-agent

# Run from terminal to see errors
./ai-doc-agent --help
```

#### Antivirus False Positive

**Problem:** Antivirus flags executable as malware

**Solutions:**
1. Add exception in antivirus software
2. Code sign the executable (Windows)
3. Build on clean system
4. Report false positive to antivirus vendor

#### Missing DLL/Library Error

**Windows:**
```bash
# Install Visual C++ Redistributable
# Download from Microsoft website
```

**Linux:**
```bash
# Install missing libraries
sudo apt-get install libpython3.11

# Check dependencies
ldd ai-doc-agent
```

#### Configuration Not Loading

**Problem:** `.env` file not found

**Solution:**
```bash
# Ensure .env is in same directory as executable
ls .env

# Or specify full path in .env
OLLAMA_API_URL=http://localhost:11434/api/generate
```

## Advanced Options

### One-File vs One-Folder

**One-File (Default):**
```bash
python -m PyInstaller build/ai_agent.spec --onefile
```
- Single executable
- Slower startup (extracts to temp)
- Easier distribution

**One-Folder:**
```bash
python -m PyInstaller build/ai_agent.spec --onedir
```
- Multiple files in folder
- Faster startup
- Larger distribution

### Debug Mode

```bash
# Build with debug information
python -m PyInstaller build/ai_agent.spec --debug all

# Run executable to see debug output
./ai-doc-agent --verbose
```

### UPX Compression

```bash
# Install UPX
# Windows: choco install upx
# Linux: sudo apt-get install upx
# macOS: brew install upx

# Enable in spec file
upx=True
upx_exclude=[],
```

### Code Signing (Windows)

```bash
# Sign executable with certificate
signtool sign /f certificate.pfx /p password ai-doc-agent.exe

# Verify signature
signtool verify /pa ai-doc-agent.exe
```

## Platform-Specific Builds

### Build for Multiple Platforms

**Note:** Must build on target platform (Windows exe must be built on Windows)

**Cross-Platform Strategy:**
1. Build on Windows → Windows .exe
2. Build on Linux → Linux binary
3. Build on macOS → macOS binary

**Using CI/CD:**
```yaml
# GitHub Actions - Build matrix
strategy:
  matrix:
    os: [windows-latest, ubuntu-latest, macos-latest]
runs-on: ${{ matrix.os }}
```

### Platform-Specific Notes

**Windows:**
- Builds to `.exe`
- May trigger antivirus
- Consider code signing

**Linux:**
- Builds to binary
- May need `chmod +x`
- Check library dependencies

**macOS:**
- Builds to binary
- May need `chmod +x`
- Consider notarization for distribution

## Performance

### Build Time

| Platform | First Build | Subsequent Build |
|----------|-------------|------------------|
| Windows | 3-5 minutes | 1-2 minutes |
| Linux | 2-4 minutes | 1-2 minutes |
| macOS | 3-5 minutes | 1-2 minutes |

### Runtime Performance

- **Startup**: ~2-3 seconds (one-file), ~0.5 seconds (one-folder)
- **Execution**: Same as Python script
- **Memory**: ~100-200 MB

## Best Practices

### 1. Test Before Distribution

```bash
# Test on clean system (VM)
# Test all command options
# Test with different project types
ai-doc-agent.exe --help
ai-doc-agent.exe --directory test-project
```

### 2. Version Your Builds

```bash
# Tag builds with version
python -m PyInstaller build/ai_agent.spec --clean

# Rename output
mv dist/ai-doc-agent.exe dist/ai-doc-agent-v2.0.0.exe
```

### 3. Provide Clear Instructions

Include `SETUP.txt`:
```
AI Documentation Agent - Setup Instructions

1. Configuration
   - Edit .env file
   - Set OLLAMA_API_URL to your Ollama instance
   - Set MODEL_NAME (e.g., llama2:7b)

2. Usage
   - Open terminal/command prompt
   - Run: ai-doc-agent --help
   - Generate docs: ai-doc-agent --directory /path/to/project

3. Support
   - Documentation: README.md
   - Issues: github.com/your-repo/issues
```

### 4. Clean Builds

```bash
# Always clean before final build
python -m PyInstaller build/ai_agent.spec --clean

# Remove old builds
rm -rf dist/ build/
```

## Next Steps

- [Docker Deployment](docker.md) - Containerized deployment
- [Bundling Guide](bundling.md) - All deployment methods
- [Configuration](../getting-started/configuration.md) - Environment setup
- [Quick Start](../getting-started/quickstart.md) - Getting started

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/en/stable/)
- [PyInstaller FAQ](https://pyinstaller.org/en/stable/FAQ.html)
- [Building Better Executables](https://pyinstaller.org/en/stable/usage.html)
