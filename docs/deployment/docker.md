# Docker Deployment

Deploy and run the AI Documentation Agent in a containerized environment for consistent, cross-platform execution.

## Overview

Docker deployment provides an isolated, reproducible environment that works identically across Windows, macOS, and Linux. Perfect for CI/CD pipelines, team collaboration, and production deployments.

## Benefits

✅ **Cross-platform consistency** - Same behavior everywhere  
✅ **Isolated environment** - No conflicts with system packages  
✅ **Easy dependency management** - Everything bundled  
✅ **Reproducible builds** - Same results every time  
✅ **CI/CD ready** - Perfect for automation  
✅ **No Python installation required** - Just Docker

## Prerequisites

### Install Docker

**Windows:**
```bash
# Download Docker Desktop
# https://www.docker.com/products/docker-desktop

# Or using Chocolatey
choco install docker-desktop
```

**macOS:**
```bash
# Download Docker Desktop
# https://www.docker.com/products/docker-desktop

# Or using Homebrew
brew install --cask docker
```

**Linux:**
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Verify Installation

```bash
# Check Docker version
docker --version

# Test Docker
docker run hello-world
```

## Quick Start

### Method 1: Using Dockerfile

```bash
# Navigate to build directory
cd build

# Build the Docker image
docker build -t ai-doc-agent .

# Run on current directory
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=http://host.docker.internal:11434/api/generate \
  ai-doc-agent --directory /workspace
```

### Method 2: Using Docker Compose

```bash
# Navigate to build directory
cd build

# Build and run with docker-compose
docker-compose run --rm ai-doc-agent

# With custom options
docker-compose run --rm ai-doc-agent \
  --directory /workspace \
  --format html \
  --iterations 5
```

## Building the Image

### Build Command

```bash
# From build directory
cd build
docker build -t ai-doc-agent .

# With tag
docker build -t ai-doc-agent:latest .
docker build -t ai-doc-agent:2.0.0 .

# With no cache (clean build)
docker build --no-cache -t ai-doc-agent .
```

### Build Process

The Dockerfile performs these steps:

1. **Base Image**: Uses Python 3.11 slim
2. **Install wkhtmltopdf**: For PDF generation support
3. **Copy Dependencies**: Requirements.txt first (for caching)
4. **Install Python Packages**: All required dependencies
5. **Copy Application**: Source code files
6. **Setup Environment**: Configuration and output directories
7. **Create Entrypoint**: Shell script for execution

### Build Output

```
[+] Building 45.2s (12/12) FINISHED
 => [1/7] FROM python:3.11-slim
 => [2/7] RUN apt-get update && apt-get install -y wkhtmltopdf
 => [3/7] WORKDIR /app
 => [4/7] COPY config/requirements.txt .
 => [5/7] RUN pip install --no-cache-dir -r requirements.txt
 => [6/7] COPY src/ai_agent.py .
 => [7/7] COPY src/doc_generator.py .
 => exporting to image
Successfully built ai-doc-agent
```

## Running the Container

### Basic Usage

```bash
# Analyze current directory
docker run --rm \
  -v "$(pwd):/workspace" \
  ai-doc-agent --directory /workspace

# Analyze specific directory
docker run --rm \
  -v "/path/to/project:/workspace" \
  ai-doc-agent --directory /workspace
```

### With Options

```bash
# Generate HTML documentation
docker run --rm \
  -v "$(pwd):/workspace" \
  ai-doc-agent \
  --directory /workspace \
  --format html \
  --output my_docs

# High-quality documentation
docker run --rm \
  -v "$(pwd):/workspace" \
  ai-doc-agent \
  --directory /workspace \
  --iterations 5 \
  --max-files 100 \
  --verbose

# Generate PDF
docker run --rm \
  -v "$(pwd):/workspace" \
  ai-doc-agent \
  --directory /workspace \
  --format pdf \
  --output professional_docs
```

### Environment Variables

```bash
# Configure via environment variables
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=http://host.docker.internal:11434/api/generate \
  -e MODEL_NAME=codellama \
  -e API_TIMEOUT=600 \
  -e MAX_RETRIES=5 \
  ai-doc-agent --directory /workspace
```

### Custom Ollama URL

**Local Ollama:**
```bash
# Windows/Mac - Use host.docker.internal
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=http://host.docker.internal:11434/api/generate \
  ai-doc-agent --directory /workspace

# Linux - Use host network
docker run --rm --network host \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=http://localhost:11434/api/generate \
  ai-doc-agent --directory /workspace
```

**Remote Ollama:**
```bash
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=https://your-ollama-server.com/api/generate \
  -e OLLAMA_API_KEY=your_api_key \
  ai-doc-agent --directory /workspace
```

## Docker Compose

### Configuration

The `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  ai-doc-agent:
    build: .
    container_name: ai-doc-agent
    volumes:
      - .:/workspace
      - ./output:/output
    environment:
      - OLLAMA_API_URL=${OLLAMA_API_URL:-http://host.docker.internal:11434/api/generate}
      - MODEL_NAME=${MODEL_NAME:-llama2:7b}
      - API_TIMEOUT=${API_TIMEOUT:-300}
    network_mode: host
    command: ["--directory", "/workspace", "--format", "markdown"]
```

### Using Docker Compose

```bash
# Build the image
docker-compose build

# Run with default settings
docker-compose run --rm ai-doc-agent

# Run with custom command
docker-compose run --rm ai-doc-agent \
  --directory /workspace \
  --format html \
  --iterations 5

# Run in background (detached)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Custom Environment

Create `.env` file in build directory:

```bash
# .env
OLLAMA_API_URL=http://host.docker.internal:11434/api/generate
MODEL_NAME=codellama
API_TIMEOUT=600
MAX_RETRIES=5
RETRY_DELAY=3
```

Docker Compose will automatically load these variables.

## Volume Mounting

### Project Directory

```bash
# Mount current directory
-v "$(pwd):/workspace"

# Mount specific directory (absolute path)
-v "/home/user/my-project:/workspace"

# Windows (PowerShell)
-v "${PWD}:/workspace"

# Windows (CMD)
-v "%cd%:/workspace"
```

### Output Directory

```bash
# Mount output directory separately
docker run --rm \
  -v "$(pwd):/workspace" \
  -v "$(pwd)/docs:/output" \
  ai-doc-agent --directory /workspace
```

### Multiple Directories

```bash
# Mount multiple directories
docker run --rm \
  -v "$(pwd)/project1:/workspace/project1" \
  -v "$(pwd)/project2:/workspace/project2" \
  -v "$(pwd)/output:/output" \
  ai-doc-agent --directory /workspace/project1
```

## Network Configuration

### Host Network (Linux)

```bash
# Use host network for direct access
docker run --rm --network host \
  -v "$(pwd):/workspace" \
  ai-doc-agent --directory /workspace
```

### Bridge Network (Default)

```bash
# Use host.docker.internal for Mac/Windows
docker run --rm \
  -v "$(pwd):/workspace" \
  -e OLLAMA_API_URL=http://host.docker.internal:11434/api/generate \
  ai-doc-agent --directory /workspace
```

### Custom Network

```bash
# Create network
docker network create ai-doc-network

# Run with custom network
docker run --rm \
  --network ai-doc-network \
  -v "$(pwd):/workspace" \
  ai-doc-agent --directory /workspace
```

## Distribution

### Save Image to File

```bash
# Save image
docker save ai-doc-agent:latest | gzip > ai-doc-agent.tar.gz

# Transfer file to target system

# Load on target
gunzip -c ai-doc-agent.tar.gz | docker load
```

### Push to Docker Hub

```bash
# Tag image
docker tag ai-doc-agent:latest yourusername/ai-doc-agent:latest
docker tag ai-doc-agent:latest yourusername/ai-doc-agent:2.0.0

# Login to Docker Hub
docker login

# Push image
docker push yourusername/ai-doc-agent:latest
docker push yourusername/ai-doc-agent:2.0.0
```

### Pull from Docker Hub

```bash
# Pull and run
docker pull yourusername/ai-doc-agent:latest

docker run --rm \
  -v "$(pwd):/workspace" \
  yourusername/ai-doc-agent:latest \
  --directory /workspace
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on: [push]

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: |
          cd build
          docker build -t ai-doc-agent .
      
      - name: Generate documentation
        run: |
          docker run --rm \
            -v "$(pwd):/workspace" \
            ai-doc-agent \
            --directory /workspace \
            --format markdown \
            --output docs/API
      
      - name: Commit documentation
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/API.md
          git commit -m "Auto-generate documentation" || exit 0
          git push
```

### GitLab CI

```yaml
# .gitlab-ci.yml
generate-docs:
  image: docker:latest
  services:
    - docker:dind
  script:
    - cd build
    - docker build -t ai-doc-agent .
    - docker run --rm 
        -v "$(pwd):/workspace" 
        ai-doc-agent 
        --directory /workspace 
        --format markdown
  artifacts:
    paths:
      - output/*.md
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'cd build && docker build -t ai-doc-agent .'
            }
        }
        stage('Generate Docs') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$(pwd):/workspace" \
                      ai-doc-agent \
                      --directory /workspace \
                      --format markdown
                '''
            }
        }
    }
}
```

## Troubleshooting

### Cannot Connect to Ollama

**Problem:** Container can't reach Ollama on host

**Solution (Windows/Mac):**
```bash
# Use host.docker.internal
-e OLLAMA_API_URL=http://host.docker.internal:11434/api/generate
```

**Solution (Linux):**
```bash
# Use host network
docker run --network host ...

# Or use host IP
-e OLLAMA_API_URL=http://192.168.1.100:11434/api/generate
```

### Permission Denied

**Problem:** Cannot write to mounted volumes

**Solution:**
```bash
# Run with user permissions
docker run --user $(id -u):$(id -g) ...

# Or set permissions on output directory
chmod -R 777 output/
```

### Large Image Size

**Problem:** Docker image is too large

**Solution:**
```bash
# Use multi-stage build
# Optimize Dockerfile to reduce layers
# Remove unnecessary dependencies

# Check image size
docker images ai-doc-agent
```

### Build Fails

**Problem:** Docker build fails

**Solution:**
```bash
# Clean build with no cache
docker build --no-cache -t ai-doc-agent .

# Check logs
docker logs <container-id>

# Verify Dockerfile syntax
docker build -t ai-doc-agent . --progress=plain
```

## Best Practices

### 1. Use Specific Tags

```bash
# Tag with version
docker build -t ai-doc-agent:2.0.0 .
docker build -t ai-doc-agent:latest .
```

### 2. Minimize Image Size

```bash
# Use slim base images
FROM python:3.11-slim

# Clean up in same layer
RUN apt-get update && \
    apt-get install -y wkhtmltopdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Security Scanning

```bash
# Scan image for vulnerabilities
docker scan ai-doc-agent

# Use official base images
FROM python:3.11-slim
```

### 4. Resource Limits

```bash
# Limit memory and CPU
docker run --rm \
  --memory="2g" \
  --cpus="2" \
  -v "$(pwd):/workspace" \
  ai-doc-agent --directory /workspace
```

### 5. Logging

```bash
# View logs
docker logs <container-id>

# Follow logs
docker logs -f <container-id>

# Save logs
docker logs <container-id> > docker.log
```

## Performance

### Image Size

- Base image: ~150 MB
- With dependencies: ~250 MB
- Total size: ~250-300 MB

### Build Time

- First build: ~3-5 minutes
- Cached build: ~10-30 seconds

### Runtime Performance

Similar to native Python execution with ~5% overhead for containerization.

## Next Steps

- [PyInstaller Deployment](pyinstaller.md) - Standalone executables
- [Bundling Guide](bundling.md) - All deployment methods
- [Configuration](../getting-started/configuration.md) - Environment setup
- [Quick Start](../getting-started/quickstart.md) - Getting started

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
