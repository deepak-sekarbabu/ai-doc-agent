# Configuration Reference

Complete reference for all configuration options, environment variables, and settings.

## Overview

The AI Documentation Agent is configured through environment variables stored in a `.env` file in the project root.

## Configuration File

### Location

```
project-root/
├── .env                    # Your configuration
├── config/
│   └── .env.example       # Template
└── ...
```

### Creating Configuration

```bash
# Copy template
cp config/.env.example .env

# Edit with your settings
nano .env  # or vim, code, etc.
```

## Environment Variables

### Ollama API Configuration

#### OLLAMA_API_URL

**Description:** URL endpoint for the Ollama API

**Type:** String (URL)  
**Required:** No  
**Default:** `https://ollama.com/api/generate`

**Valid Values:**
```bash
# Local Ollama instance
OLLAMA_API_URL=http://localhost:11434/api/generate

# Remote server
OLLAMA_API_URL=https://your-server.com/api/generate

# Cloud service
OLLAMA_API_URL=https://ollama.com/api/generate
```

**Usage:**
- Local development → `http://localhost:11434/api/generate`
- Production with local Ollama → Same as above
- Remote/Cloud Ollama → Custom URL

**Notes:**
- Must be a valid HTTP/HTTPS URL
- Must end with `/api/generate`
- Port 11434 is Ollama's default

---

#### OLLAMA_API_KEY

**Description:** API key for authenticated Ollama instances (optional)

**Type:** String  
**Required:** No  
**Default:** Empty (not required for local Ollama)

**Valid Values:**
```bash
# No key needed (local Ollama)
OLLAMA_API_KEY=

# With authentication (remote/cloud)
OLLAMA_API_KEY=your_api_key_here
OLLAMA_API_KEY=sk-abc123def456...
```

**Usage:**
- Local Ollama → Leave empty
- Authenticated remote → Set to your API key
- Cloud services → Set to provided key

**Security:**
- Never commit API keys to version control
- Use `.gitignore` for `.env` files
- Rotate keys regularly

---

#### MODEL_NAME

**Description:** Ollama model to use for documentation generation

**Type:** String  
**Required:** No  
**Default:** `gpt-oss:120b-cloud`

**Valid Values:**
```bash
# Fast models
MODEL_NAME=llama2:7b
MODEL_NAME=mistral

# Code-optimized
MODEL_NAME=codellama

# High-quality
MODEL_NAME=llama2:13b
MODEL_NAME=gpt-oss:120b-cloud

# Custom models
MODEL_NAME=your-custom-model
```

**Model Comparison:**

| Model | Size | Speed | Quality | RAM | Best For |
|-------|------|-------|---------|-----|----------|
| `llama2:7b` | 7B | ⚡⚡⚡ | ⭐⭐⭐ | 4-8 GB | Testing, quick docs |
| `mistral` | 7B | ⚡⚡ | ⭐⭐⭐⭐ | 8 GB | Balanced use |
| `codellama` | 7B | ⚡⚡ | ⭐⭐⭐⭐⭐ | 8 GB | Code documentation |
| `llama2:13b` | 13B | ⚡ | ⭐⭐⭐⭐⭐ | 16 GB | Best quality |
| `gpt-oss:120b-cloud` | 120B | ⚡ | ⭐⭐⭐⭐⭐ | Cloud | Cloud use |

**Usage:**
```bash
# Check available models
ollama list

# Pull a model
ollama pull llama2:7b

# Use in configuration
MODEL_NAME=llama2:7b
```

---

#### API_TIMEOUT

**Description:** Maximum time to wait for API responses (seconds)

**Type:** Integer  
**Required:** No  
**Default:** `300` (5 minutes)

**Valid Values:**
```bash
# Quick timeout (fast models, small projects)
API_TIMEOUT=120

# Standard timeout (default)
API_TIMEOUT=300

# Extended timeout (large projects)
API_TIMEOUT=600

# Maximum timeout
API_TIMEOUT=900
```

**Range:** 60 - 1800 (1 minute to 30 minutes)

**Considerations:**
- Larger models need more time
- More files = longer processing
- Complex code needs more time
- Network latency (remote APIs)

**Recommendations:**

| Scenario | Timeout |
|----------|---------|
| Small project + fast model | 120-180 |
| Standard usage | 300 |
| Large project | 600 |
| Comprehensive docs | 900 |

---

### Agent Behavior Configuration

#### MAX_RETRIES

**Description:** Number of retry attempts for failed API calls

**Type:** Integer  
**Required:** No  
**Default:** `3`

**Valid Values:**
```bash
# Minimal retries (fail fast)
MAX_RETRIES=1

# Standard retries
MAX_RETRIES=3

# Robust retries
MAX_RETRIES=5

# Maximum retries
MAX_RETRIES=10
```

**Range:** 0 - 10

**Retry Behavior:**
- Uses exponential backoff
- Delay increases with each retry
- Total time = sum of all delays

**Usage:**
- Development → 1-2 (fail fast)
- Production → 3-5 (reliable)
- Critical systems → 5-10 (maximum reliability)

---

#### RETRY_DELAY

**Description:** Base delay between retries (exponential backoff)

**Type:** Integer (seconds)  
**Required:** No  
**Default:** `2`

**Valid Values:**
```bash
# Quick retries
RETRY_DELAY=1

# Standard delay
RETRY_DELAY=2

# Conservative delay
RETRY_DELAY=5
```

**Range:** 1 - 10 seconds

**Exponential Backoff:**
```
Retry 1: wait RETRY_DELAY seconds (2s)
Retry 2: wait RETRY_DELAY * 2 seconds (4s)
Retry 3: wait RETRY_DELAY * 4 seconds (8s)
Retry 4: wait RETRY_DELAY * 8 seconds (16s)
...
```

**Total Wait Time Examples:**

| Retries | Delay | Total Wait |
|---------|-------|------------|
| 3 | 2s | 2 + 4 + 8 = 14s |
| 5 | 2s | 2 + 4 + 8 + 16 + 32 = 62s |
| 3 | 5s | 5 + 10 + 20 = 35s |

**Usage:**
- Fast network → 1-2 seconds
- Normal network → 2-3 seconds
- Slow/unreliable network → 5-10 seconds

---

#### ENABLE_CACHING

**Description:** Enable response caching for faster subsequent runs

**Type:** Boolean  
**Required:** No  
**Default:** `true`

**Valid Values:**
```bash
# Enable caching
ENABLE_CACHING=true

# Disable caching
ENABLE_CACHING=false
```

**Status:** Future feature (not fully implemented)

**Benefits:**
- Faster repeated runs
- Reduced API calls
- Lower costs
- Consistent results

---

#### CRITIQUE_THRESHOLD

**Description:** Quality threshold for accepting documentation (0.0-1.0)

**Type:** Float  
**Required:** No  
**Default:** `0.8` (80% quality)

**Valid Values:**
```bash
# Lenient (faster, lower quality)
CRITIQUE_THRESHOLD=0.6

# Balanced (default)
CRITIQUE_THRESHOLD=0.8

# Strict (slower, higher quality)
CRITIQUE_THRESHOLD=0.9

# Very strict
CRITIQUE_THRESHOLD=0.95
```

**Range:** 0.0 - 1.0 (0% to 100%)

**Impact:**

| Threshold | Iterations Needed | Time | Quality |
|-----------|-------------------|------|---------|
| 0.6 | 1-2 | Fast | Basic |
| 0.8 | 2-3 | Medium | Good |
| 0.9 | 3-5 | Slow | Excellent |
| 0.95 | 5-7+ | Very slow | Outstanding |

**Usage:**
- Quick docs → 0.6-0.7
- Standard docs → 0.8
- Production docs → 0.9
- Critical docs → 0.95

---

## Configuration Profiles

### Development Profile

**Goal:** Fast iteration, quick feedback

```bash
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=llama2:7b
API_TIMEOUT=180
MAX_RETRIES=2
RETRY_DELAY=1
CRITIQUE_THRESHOLD=0.7
ENABLE_CACHING=true
```

**Use with:**
```bash
python run.py --max-files 20 --iterations 2
```

---

### Production Profile

**Goal:** High quality, comprehensive documentation

```bash
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=codellama
API_TIMEOUT=600
MAX_RETRIES=5
RETRY_DELAY=3
CRITIQUE_THRESHOLD=0.9
ENABLE_CACHING=true
```

**Use with:**
```bash
python run.py --iterations 5 --max-files 100
```

---

### Cloud Profile

**Goal:** Using remote Ollama service

```bash
OLLAMA_API_URL=https://ollama.com/api/generate
OLLAMA_API_KEY=your_api_key_here
MODEL_NAME=gpt-oss:120b-cloud
API_TIMEOUT=600
MAX_RETRIES=5
RETRY_DELAY=3
CRITIQUE_THRESHOLD=0.8
ENABLE_CACHING=true
```

**Use with:**
```bash
python run.py --iterations 3
```

---

### Testing Profile

**Goal:** Fast, minimal resource usage

```bash
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=llama2:7b
API_TIMEOUT=120
MAX_RETRIES=1
RETRY_DELAY=1
CRITIQUE_THRESHOLD=0.6
ENABLE_CACHING=false
```

**Use with:**
```bash
python run.py --max-files 10 --iterations 1
```

---

### CI/CD Profile

**Goal:** Automated documentation in pipeline

```bash
OLLAMA_API_URL=http://ollama-service:11434/api/generate
MODEL_NAME=llama2:7b
API_TIMEOUT=300
MAX_RETRIES=3
RETRY_DELAY=2
CRITIQUE_THRESHOLD=0.8
ENABLE_CACHING=true
```

**Use with:**
```bash
python run.py --format markdown --output docs/API
```

---

## Command-Line Overrides

Command-line options override `.env` settings:

```bash
# Model override
python run.py --model mistral
# Overrides MODEL_NAME in .env

# Format override
python run.py --format html
# Does not affect .env

# Multiple overrides
python run.py \
  --model codellama \
  --iterations 5 \
  --max-files 100
```

**Precedence Order:**
1. Command-line arguments (highest)
2. Environment variables (`.env`)
3. Default values (lowest)

---

## Validation

### Check Current Configuration

```bash
# View .env contents
cat .env

# On Windows
type .env
```

### Validate Settings

```python
# Python script to validate
import os
from dotenv import load_dotenv

load_dotenv()

print(f"API URL: {os.getenv('OLLAMA_API_URL')}")
print(f"Model: {os.getenv('MODEL_NAME')}")
print(f"Timeout: {os.getenv('API_TIMEOUT')}")
print(f"Max Retries: {os.getenv('MAX_RETRIES')}")
```

### Test Configuration

```bash
# Test with help command
python run.py --help

# Test with small project
python run.py --directory ./examples --max-files 5
```

---

## Security Best Practices

### 1. Protect API Keys

```bash
# Add .env to .gitignore
echo ".env" >> .gitignore

# Never commit .env
git status  # Should not show .env
```

### 2. Use Environment-Specific Files

```bash
# Development
.env.dev

# Production
.env.prod

# Testing
.env.test

# Copy when needed
cp .env.prod .env
```

### 3. Rotate Keys Regularly

```bash
# Update API key
OLLAMA_API_KEY=new_key_here

# Test new key
python run.py --help
```

### 4. Restrict File Permissions

```bash
# Linux/macOS - make .env readable only by owner
chmod 600 .env

# Verify permissions
ls -la .env
# Should show: -rw------- (600)
```

---

## Troubleshooting

### Configuration Not Loading

**Symptom:** Settings ignored

**Solution:**
```bash
# Check .env exists in project root
ls -la .env

# Check syntax (no spaces around =)
# Correct: KEY=value
# Wrong: KEY = value

# Verify location
pwd  # Should be in project root
```

### Invalid Values

**Symptom:** Errors about invalid configuration

**Solution:**
```bash
# Check data types
API_TIMEOUT=300     # Integer, not "300"
CRITIQUE_THRESHOLD=0.8  # Float, not "0.8"
ENABLE_CACHING=true    # Boolean, not "True"

# Check ranges
API_TIMEOUT=300    # Not negative or 0
CRITIQUE_THRESHOLD=0.8  # Between 0.0 and 1.0
```

### API Connection Issues

**Symptom:** Cannot connect to Ollama

**Solution:**
```bash
# Check URL format
OLLAMA_API_URL=http://localhost:11434/api/generate
# Not: http://localhost:11434 (missing /api/generate)

# Test URL
curl http://localhost:11434/api/tags

# Verify Ollama is running
ollama list
```

---

## Configuration Examples

### Example 1: Local Development

```bash
# .env
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_API_KEY=
MODEL_NAME=llama2:7b
API_TIMEOUT=180
MAX_RETRIES=2
RETRY_DELAY=1
ENABLE_CACHING=true
CRITIQUE_THRESHOLD=0.7
```

### Example 2: Remote Ollama

```bash
# .env
OLLAMA_API_URL=https://ollama.example.com/api/generate
OLLAMA_API_KEY=sk-abc123def456
MODEL_NAME=codellama
API_TIMEOUT=600
MAX_RETRIES=5
RETRY_DELAY=3
ENABLE_CACHING=true
CRITIQUE_THRESHOLD=0.8
```

### Example 3: Docker Container

```bash
# .env
OLLAMA_API_URL=http://host.docker.internal:11434/api/generate
OLLAMA_API_KEY=
MODEL_NAME=mistral
API_TIMEOUT=300
MAX_RETRIES=3
RETRY_DELAY=2
ENABLE_CACHING=true
CRITIQUE_THRESHOLD=0.8
```

---

## Next Steps

- [API Reference](api.md) - Module and function documentation
- [Project Structure](structure.md) - Code organization
- [Configuration Guide](../getting-started/configuration.md) - Detailed setup
- [Quick Start](../getting-started/quickstart.md) - Get started
