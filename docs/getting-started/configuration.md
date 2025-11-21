# Configuration

Complete guide to configuring the AI Documentation Agent for optimal performance.

## Configuration File

The agent uses a `.env` file for configuration located in the project root.

### Creating Your Configuration

```bash
# Copy the example configuration
cp .env.example .env

# Edit with your preferred editor
nano .env  # or vim, code, notepad++, etc.
```

## Environment Variables

### Ollama API Configuration

#### OLLAMA_API_URL

The URL endpoint for the Ollama API.

**Default:** `http://localhost:11434/api/generate`  
**Cloud:** `https://ollama.com/api/generate`

```bash
# For local Ollama installation
OLLAMA_API_URL=http://localhost:11434/api/generate

# For remote Ollama server
OLLAMA_API_URL=https://your-ollama-server.com/api/generate

# For cloud-hosted Ollama
OLLAMA_API_URL=https://ollama.com/api/generate
```

!!! tip "Local vs Remote"
    - **Local** → Faster, free, private, requires local installation
    - **Remote** → Accessible anywhere, may have costs, requires network

#### OLLAMA_API_KEY

Optional API key for authenticated Ollama instances.

**Default:** Empty (not required for local Ollama)

```bash
# Leave empty for local installation
OLLAMA_API_KEY=

# Set for authenticated remote servers
OLLAMA_API_KEY=your_api_key_here
```

#### MODEL_NAME

The LLM model to use for documentation generation.

**Default:** `gpt-oss:120b-cloud`

```bash
# Fast and efficient (recommended for testing)
MODEL_NAME=llama2:7b

# Better quality
MODEL_NAME=mistral

# Best for code documentation
MODEL_NAME=codellama

# High quality, slower
MODEL_NAME=llama2:13b

# Cloud model (requires internet)
MODEL_NAME=gpt-oss:120b-cloud
```

**Model Comparison:**

| Model | Speed | Quality | RAM | Best For |
|-------|-------|---------|-----|----------|
| `llama2:7b` | ⚡⚡⚡ | ⭐⭐⭐ | 4-8 GB | Quick docs, testing |
| `mistral` | ⚡⚡ | ⭐⭐⭐⭐ | 8 GB | Balanced quality/speed |
| `codellama` | ⚡⚡ | ⭐⭐⭐⭐⭐ | 8 GB | Code documentation |
| `llama2:13b` | ⚡ | ⭐⭐⭐⭐⭐ | 16 GB | Maximum quality |

!!! tip "Choosing a Model"
    - **First time?** Use `llama2:7b`
    - **Production docs?** Use `codellama`
    - **Limited RAM?** Use `llama2:7b`
    - **Best quality?** Use `llama2:13b` or `codellama`

#### API_TIMEOUT

Maximum time (in seconds) to wait for API responses.

**Default:** `300` (5 minutes)

```bash
# Quick timeout for fast models
API_TIMEOUT=180

# Standard timeout
API_TIMEOUT=300

# Extended timeout for large projects
API_TIMEOUT=600

# Maximum timeout for comprehensive docs
API_TIMEOUT=900
```

!!! warning "Timeout Considerations"
    - Larger models need more time
    - More files = longer processing
    - Complex code needs more timeout
    - Network latency affects remote APIs

### Agent Behavior Configuration

#### MAX_RETRIES

Number of retry attempts for failed API calls.

**Default:** `3`

```bash
# Minimal retries (fail fast)
MAX_RETRIES=1

# Standard retries
MAX_RETRIES=3

# Maximum reliability
MAX_RETRIES=5
```

#### RETRY_DELAY

Base delay in seconds between retries (uses exponential backoff).

**Default:** `2`

```bash
# Quick retries
RETRY_DELAY=1

# Standard delay
RETRY_DELAY=2

# Conservative delay (network issues)
RETRY_DELAY=5
```

**Retry Pattern:**

- 1st retry: wait `RETRY_DELAY` seconds
- 2nd retry: wait `RETRY_DELAY * 2` seconds
- 3rd retry: wait `RETRY_DELAY * 4` seconds
- And so on (exponential backoff)

#### ENABLE_CACHING

Enable response caching for faster subsequent runs.

**Default:** `true`  
**Status:** Future feature (not yet implemented)

```bash
ENABLE_CACHING=true
```

#### CRITIQUE_THRESHOLD

Quality threshold (0.0-1.0) for accepting documentation.

**Default:** `0.8`

```bash
# Lenient (faster, lower quality)
CRITIQUE_THRESHOLD=0.6

# Balanced
CRITIQUE_THRESHOLD=0.8

# Strict (slower, higher quality)
CRITIQUE_THRESHOLD=0.9
```

## Configuration Profiles

### Development Profile

Fast iterations, quick feedback:

```bash
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=llama2:7b
API_TIMEOUT=180
MAX_RETRIES=2
RETRY_DELAY=1
CRITIQUE_THRESHOLD=0.7
```

**Use with:**

```bash
ai-doc-agent --max-files 20 --iterations 2
```

### Production Profile

High quality, comprehensive documentation:

```bash
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=codellama
API_TIMEOUT=600
MAX_RETRIES=5
RETRY_DELAY=3
CRITIQUE_THRESHOLD=0.9
```

**Use with:**

```bash
ai-doc-agent --iterations 5 --max-files 100
```

### Cloud Profile

Using remote Ollama service:

```bash
OLLAMA_API_URL=https://ollama.com/api/generate
OLLAMA_API_KEY=your_api_key
MODEL_NAME=gpt-oss:120b-cloud
API_TIMEOUT=600
MAX_RETRIES=5
RETRY_DELAY=3
CRITIQUE_THRESHOLD=0.8
```

### Testing Profile

Fast, minimal resource usage:

```bash
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=llama2:7b
API_TIMEOUT=120
MAX_RETRIES=1
RETRY_DELAY=1
CRITIQUE_THRESHOLD=0.6
```

**Use with:**

```bash
ai-doc-agent --max-files 10 --iterations 1
```

## Command-Line Overrides

Command-line options override `.env` settings:

```bash
# Model override
ai-doc-agent --model mistral

# Format override
ai-doc-agent --format html

# Multiple overrides
ai-doc-agent --model codellama --iterations 5 --max-files 100
```

## Verification

### Check Configuration

```bash
# View current .env
cat .env

# Test configuration
ai-doc-agent --help

# Verify Ollama connection
curl http://localhost:11434/api/tags
```

### Validate Settings

```bash
# List available models
ollama list

# Check if specific model is available
ollama list | grep llama2:7b

# Pull missing model
ollama pull llama2:7b
```

## Advanced Configuration

### Multiple Environments

Create different configuration files:

```bash
# Development
cp .env .env.dev

# Production
cp .env .env.prod

# Testing
cp .env .env.test
```

**Use with:**

```bash
# Copy desired config before running
cp .env.prod .env
ai-doc-agent
```

### Custom Model Settings

For self-hosted Ollama with custom models:

```bash
# Create custom model
ollama create my-docs-model -f Modelfile

# Use in configuration
MODEL_NAME=my-docs-model
```

### Performance Tuning

#### For Speed

```bash
MODEL_NAME=llama2:7b
API_TIMEOUT=180
MAX_RETRIES=2
CRITIQUE_THRESHOLD=0.7
```

**Command:** `ai-doc-agent --max-files 20 --iterations 2`

#### For Quality

```bash
MODEL_NAME=codellama
API_TIMEOUT=900
MAX_RETRIES=5
CRITIQUE_THRESHOLD=0.9
```

**Command:** `ai-doc-agent --max-files 100 --iterations 5`

#### For Reliability

```bash
MAX_RETRIES=5
RETRY_DELAY=5
API_TIMEOUT=600
```

## Troubleshooting Configuration

### Configuration Not Loading

!!! failure "Settings not applied"

    **Check:**
    1. `.env` file exists in project root
    2. No syntax errors in `.env`
    3. Environment variables properly formatted
    
    ```bash
    # Verify .env location
    ls -la .env
    
    # Check for syntax errors
    cat .env
    ```

### Model Not Found

!!! failure "Model 'xxx' not found"

    **Solution:**
    ```bash
    # List available models
    ollama list
    
    # Pull the model
    ollama pull llama2:7b
    
    # Update .env
    MODEL_NAME=llama2:7b
    ```

### Connection Issues

!!! failure "Cannot connect to Ollama"

    **Solution:**
    ```bash
    # Check if Ollama is running
    ollama list
    
    # Start Ollama if needed
    ollama serve
    
    # Verify URL in .env
    OLLAMA_API_URL=http://localhost:11434/api/generate
    ```

### Timeout Issues

!!! failure "Request timeout"

    **Solutions:**
    1. Increase timeout: `API_TIMEOUT=600`
    2. Reduce files: `--max-files 20`
    3. Use faster model: `MODEL_NAME=llama2:7b`
    4. Reduce iterations: `--iterations 2`

## Configuration Best Practices

### 1. Start Conservative

```bash
# Begin with fast, reliable settings
MODEL_NAME=llama2:7b
API_TIMEOUT=300
MAX_RETRIES=3
```

### 2. Monitor Performance

```bash
# Use verbose mode to see timing
ai-doc-agent --verbose

# Check logs
tail -f langgraph_agent.log
```

### 3. Optimize Based on Results

- Timeout often? → Increase `API_TIMEOUT`
- Poor quality? → Use better model
- Slow? → Reduce files or iterations
- Unreliable? → Increase retries

### 4. Document Your Settings

```bash
# Add comments to your .env
# This configuration is optimized for:
# - Project type: Backend APIs
# - Typical size: 50-100 files
# - Quality level: Production
MODEL_NAME=codellama
# ... rest of config
```

## Next Steps

✅ Configuration complete!

- [Quick Start](quickstart.md) - Generate your first docs
- [Installation](installation.md) - Advanced installation methods
- [User Guide](../guide/overview.md) - Learn all features
- [Complete Guide](../guide.md) - Deep dive into capabilities

## Configuration Reference

### All Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OLLAMA_API_URL` | URL | `https://ollama.com/api/generate` | API endpoint |
| `OLLAMA_API_KEY` | String | Empty | API key (optional) |
| `MODEL_NAME` | String | `gpt-oss:120b-cloud` | LLM model name |
| `API_TIMEOUT` | Integer | `300` | Timeout in seconds |
| `MAX_RETRIES` | Integer | `3` | Retry attempts |
| `RETRY_DELAY` | Integer | `2` | Base retry delay |
| `ENABLE_CACHING` | Boolean | `true` | Enable caching |
| `CRITIQUE_THRESHOLD` | Float | `0.8` | Quality threshold |

### Valid Values

**Model Names:** Any model available in `ollama list`  
**Timeouts:** 60-1800 seconds (1 min - 30 min)  
**Retries:** 0-10 attempts  
**Delays:** 1-10 seconds  
**Threshold:** 0.0-1.0
