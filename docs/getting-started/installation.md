# Installation

Complete installation guide for all platforms and deployment methods.

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.8 | 3.11+ |
| RAM | 4 GB | 8 GB+ |
| Disk Space | 500 MB | 2 GB |
| Ollama | Any version | Latest |

## Method 1: Direct Installation

Best for development and customization.

### 1. Install Python

=== "Windows"

    Download from [python.org](https://python.org) and run installer.
    
    ✅ Check "Add Python to PATH"

=== "macOS"

    ```bash
    brew install python@3.11
    ```

=== "Linux"

    ```bash
    sudo apt update
    sudo apt install python3.11 python3-pip
    ```

### 2. Install Ollama

=== "Windows"

    1. Download from [ollama.ai/download](https://ollama.ai/download)
    2. Run the installer
    3. Ollama will start automatically

=== "macOS"

    ```bash
    brew install ollama
    ollama serve
    ```

=== "Linux"

    ```bash
    curl -fsSL https://ollama.ai/install.sh | sh
    ollama serve
    ```

### 3. Clone Repository

```bash
git clone https://github.com/yourusername/ai-doc-agent.git
cd ai-doc-agent
```

### 4. Install Dependencies

```bash
pip install -r config/requirements.txt
```

### 5. Configure

```bash
cp config/.env.example .env
# Edit .env with your settings
```

### 6. Pull LLM Model

```bash
ollama pull llama2:7b
```

### 7. Test Installation

```bash
python run.py --help
python run.py --directory ./examples
```

## Method 2: Standalone Executable

No Python required on target system!

See [Bundling Guide](../deployment/bundling.md) for building executables.

Download pre-built executables:

- [Windows x64](https://github.com/yourusername/ai-doc-agent/releases)
- [Linux x64](https://github.com/yourusername/ai-doc-agent/releases)
- [macOS x64](https://github.com/yourusername/ai-doc-agent/releases)

## Method 3: Docker

Best for consistent cross-platform deployment.

### Prerequisites

- Docker installed
- Docker Compose (optional)

### Using Docker

```bash
cd build
docker build -t ai-doc-agent .

# Run
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=http://host.docker.internal:11434/api/generate \
  ai-doc-agent --directory /workspace
```

### Using Docker Compose

```bash
cd build
docker-compose run --rm ai-doc-agent --directory /workspace
```

See [Docker Guide](../deployment/docker.md) for details.

## Method 4: Python Package

Install as a Python package.

```bash
pip install .

# Now available globally
ai-doc-agent --help
doc-generator --help
```

## Optional: PDF Support

For PDF generation, install wkhtmltopdf:

=== "Windows"

    ```bash
    choco install wkhtmltopdf
    ```
    
    Or download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)

=== "macOS"

    ```bash
    brew install wkhtmltopdf
    ```

=== "Linux"

    ```bash
    sudo apt-get install wkhtmltopdf
    ```

## Verify Installation

```bash
# Check Python
python --version  # Should be 3.8+

# Check Ollama
ollama --version

# Check agent
python run.py --help

# Generate test docs
python run.py --directory ./examples --output test
```

## Troubleshooting

### Python not found

!!! failure "python: command not found"
    
    **Windows:** Reinstall Python with "Add to PATH" checked
    
    **macOS/Linux:** Create symlink:
    ```bash
    sudo ln -s /usr/bin/python3 /usr/bin/python
    ```

### Ollama connection error

!!! failure "Cannot connect to Ollama"
    
    1. Check if Ollama is running: `ollama list`
    2. Start if needed: `ollama serve`
    3. Check URL in `.env`: `OLLAMA_API_URL`

### Permission denied

!!! failure "Permission denied"
    
    **Linux/macOS:**
    ```bash
    chmod +x run.py
    chmod +x build/build.sh
    ```

### Import errors

!!! failure "ModuleNotFoundError"
    
    ```bash
    pip install --upgrade pip
    pip install -r config/requirements.txt
    ```

## Next Steps

✅ Installation complete!

- [Quick Start](quickstart.md) - Generate your first docs
- [Configuration](configuration.md) - Customize the agent
- [User Guide](../guide/overview.md) - Learn all features
