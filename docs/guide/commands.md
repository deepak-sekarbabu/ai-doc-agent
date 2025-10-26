# Command Reference

Complete reference for all commands, options, and usage patterns.

## Command Overview

The AI Documentation Agent provides three main entry points:

| Command | Purpose | Mode |
|---------|---------|------|
| `python run.py` | Quick launcher | AI Agent (iterative) |
| `python src/ai_agent.py` | Full AI agent | AI Agent (iterative) |
| `python src/doc_generator.py` | Simple generator | Single-pass |

## run.py - Quick Launcher

The simplest way to run the AI Agent.

### Syntax

```bash
python run.py [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--directory DIR` | path | Current dir | Directory to analyze |
| `--model MODEL` | string | From .env | Ollama model name |
| `--format FORMAT` | choice | `markdown` | Output format |
| `--output FILE` | string | Auto | Output filename (no ext) |
| `--max-files N` | integer | 30 | Max files to analyze |
| `--project-type TYPE` | choice | Auto | Project type |
| `--iterations N` | integer | 3 | Max refinement iterations |
| `--verbose` | flag | False | Enable verbose logging |

### Examples

#### Basic Usage

```bash
# Analyze current directory
python run.py

# Analyze specific directory
python run.py --directory ~/my-project

# Analyze with relative path
python run.py --directory ./my-app
```

#### Format Options

```bash
# Markdown (default)
python run.py

# HTML output
python run.py --format html

# PDF output (requires wkhtmltopdf)
python run.py --format pdf
```

#### Quality Control

```bash
# Quick docs (2 iterations)
python run.py --iterations 2 --max-files 20

# Standard quality (default)
python run.py --iterations 3 --max-files 30

# High quality (5 iterations)
python run.py --iterations 5 --max-files 100
```

#### Model Selection

```bash
# Use default model
python run.py

# Fast model
python run.py --model llama2:7b

# Code-optimized model
python run.py --model codellama

# High-quality model
python run.py --model llama2:13b
```

#### Project Type

```bash
# Auto-detect (default)
python run.py

# Frontend project
python run.py --project-type frontend

# Backend project
python run.py --project-type backend

# Mixed project
python run.py --project-type mixed
```

#### Custom Output

```bash
# Auto-generated filename
python run.py

# Custom filename
python run.py --output my_project_docs

# Custom filename with format
python run.py --output api_documentation --format html
```

#### Debugging

```bash
# Verbose mode
python run.py --verbose

# Verbose with all options
python run.py \
  --directory ./my-app \
  --verbose \
  --iterations 3 \
  --max-files 50
```

## ai_agent.py - Full AI Agent

Direct access to the AI Agent with all features.

### Syntax

```bash
python src/ai_agent.py [OPTIONS]
```

### Options

Same as `run.py` plus additional advanced options.

### Examples

#### Maximum Quality Documentation

```bash
python src/ai_agent.py \
  --directory ~/important-project \
  --iterations 5 \
  --max-files 100 \
  --model codellama \
  --format pdf \
  --output comprehensive_documentation \
  --verbose
```

#### Backend API Documentation

```bash
python src/ai_agent.py \
  --directory ./api-server \
  --project-type backend \
  --model codellama \
  --max-files 50 \
  --iterations 4 \
  --format html \
  --output api_docs
```

#### Frontend Component Documentation

```bash
python src/ai_agent.py \
  --directory ./component-library \
  --project-type frontend \
  --max-files 75 \
  --iterations 4 \
  --format html \
  --output component_docs
```

#### Quick Testing

```bash
python src/ai_agent.py \
  --directory ./test-project \
  --iterations 1 \
  --max-files 10 \
  --model llama2:7b \
  --verbose
```

## doc_generator.py - Simple Generator

Fast, single-pass documentation generation.

### Syntax

```bash
python src/doc_generator.py DIRECTORY [OPTIONS]
```

### Positional Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `DIRECTORY` | Yes | Path to project directory |

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--format FORMAT` | choice | `markdown` | Output format |
| `--output FILE` | string | Auto | Output filename |

### Examples

#### Basic Usage

```bash
# Simple documentation
python src/doc_generator.py ./my-project

# With specific format
python src/doc_generator.py ./my-project --format html

# Custom output name
python src/doc_generator.py ./my-project --output quick_docs
```

#### Quick Testing

```bash
# Test on example project
python src/doc_generator.py ./examples

# Quick HTML docs
python src/doc_generator.py ./examples --format html
```

## Option Details

### --directory

Specifies the project directory to analyze.

**Type:** Path (string)  
**Default:** Current directory  
**Required:** No

```bash
# Current directory (default)
python run.py

# Relative path
python run.py --directory ./my-app
python run.py --directory ../other-project

# Absolute path
python run.py --directory /home/user/projects/my-app
python run.py --directory C:\Projects\MyApp  # Windows
```

**Tips:**
- Use absolute paths to avoid ambiguity
- Ensure the path exists and is readable
- Directory should contain source code files

### --model

Specifies the Ollama model to use.

**Type:** String  
**Default:** From `.env` (MODEL_NAME)  
**Required:** No

```bash
# Default model from .env
python run.py

# Override with specific model
python run.py --model llama2:7b
python run.py --model mistral
python run.py --model codellama
python run.py --model llama2:13b
```

**Available Models:**
```bash
# List installed models
ollama list

# Pull a new model
ollama pull codellama
```

**Model Recommendations:**
- `llama2:7b` - Fast, good for testing (4-8 GB RAM)
- `mistral` - Balanced quality/speed (8 GB RAM)
- `codellama` - Best for code docs (8 GB RAM)
- `llama2:13b` - Highest quality (16 GB RAM)

### --format

Output format for documentation.

**Type:** Choice  
**Options:** `markdown`, `html`, `pdf`  
**Default:** `markdown`  
**Required:** No

```bash
# Markdown (default, GitHub-ready)
python run.py --format markdown

# HTML (styled, browser-ready)
python run.py --format html

# PDF (printable, requires wkhtmltopdf)
python run.py --format pdf
```

**Format Details:**

**Markdown:**
- Clean, readable text format
- GitHub/GitLab compatible
- Easy to version control
- No dependencies

**HTML:**
- Professional styling
- Browser-ready
- Includes CSS
- Good for sharing

**PDF:**
- Professional appearance
- Printable
- Requires `wkhtmltopdf` installed
- Platform-specific installation

### --output

Custom output filename (without extension).

**Type:** String  
**Default:** Auto-generated (e.g., `my-project_documentation`)  
**Required:** No

```bash
# Auto-generated name
python run.py

# Custom name
python run.py --output my_docs

# With format
python run.py --output api_reference --format html
# Creates: api_reference.html
```

**Output Location:**
- Files saved to `output/` directory
- Directory created if doesn't exist
- Extension added automatically

### --max-files

Maximum number of files to analyze.

**Type:** Integer  
**Default:** 30  
**Range:** 1-1000  
**Required:** No

```bash
# Default (30 files)
python run.py

# Quick docs (fewer files)
python run.py --max-files 15

# Standard project
python run.py --max-files 50

# Large project
python run.py --max-files 100

# Very large project (may timeout)
python run.py --max-files 200
```

**Considerations:**
- More files = better context = higher quality
- More files = longer processing time
- More files = higher API costs
- Timeout may occur with too many files

**Recommendations:**
- Small project (< 20 files): `--max-files 15`
- Medium project (20-50 files): `--max-files 30`
- Large project (50-100 files): `--max-files 75`
- Very large project: `--max-files 100`

### --project-type

Explicitly specify project type.

**Type:** Choice  
**Options:** `frontend`, `backend`, `mixed`  
**Default:** Auto-detect  
**Required:** No

```bash
# Auto-detect (default)
python run.py

# Frontend project
python run.py --project-type frontend

# Backend project
python run.py --project-type backend

# Mixed (full-stack)
python run.py --project-type mixed
```

**Why Specify?**
- More accurate file prioritization
- Better-targeted documentation
- Faster than auto-detection
- Override incorrect auto-detection

**Detection Indicators:**

**Frontend:**
- `package.json`, `yarn.lock`
- `.jsx`, `.tsx`, `.vue`, `.svelte`
- `webpack.config.js`, `vite.config.ts`

**Backend:**
- `requirements.txt`, `pom.xml`, `go.mod`
- `.java`, `.py`, `.go` (without frontend files)
- `application.properties`, `build.gradle`

**Mixed:**
- Both frontend and backend indicators

### --iterations

Maximum refinement iterations.

**Type:** Integer  
**Default:** 3  
**Range:** 1-10  
**Required:** No

```bash
# Quick docs (minimal refinement)
python run.py --iterations 1

# Fast docs (some refinement)
python run.py --iterations 2

# Standard quality (default)
python run.py --iterations 3

# High quality
python run.py --iterations 5

# Maximum quality (slow)
python run.py --iterations 10
```

**Iteration Process:**
1. Generate documentation
2. Critique quality
3. Refine based on critique
4. Repeat until quality threshold OR max iterations

**Trade-offs:**
- More iterations = better quality
- More iterations = longer time
- More iterations = more API calls
- Diminishing returns after 5 iterations

**Recommendations:**
- Testing: `--iterations 1`
- Quick docs: `--iterations 2`
- Standard: `--iterations 3` (default)
- Production: `--iterations 5`
- Critical: `--iterations 7-10`

### --verbose

Enable verbose logging output.

**Type:** Flag (no value)  
**Default:** False  
**Required:** No

```bash
# Normal output (INFO level)
python run.py

# Verbose output (DEBUG level)
python run.py --verbose
```

**Verbose Output Includes:**
- File discovery process
- API request details
- Generation progress
- Critique feedback
- Timing information
- Debug messages

**Use When:**
- Troubleshooting issues
- Understanding agent behavior
- Monitoring progress
- Debugging configuration
- Learning how it works

## Common Command Patterns

### Quick Documentation

```bash
python run.py \
  --max-files 15 \
  --iterations 2 \
  --model llama2:7b
```

**Result:** Fast, basic documentation

### Standard Documentation

```bash
python run.py \
  --directory ~/my-project \
  --max-files 30 \
  --iterations 3
```

**Result:** Good quality, reasonable time

### Production Documentation

```bash
python run.py \
  --directory ~/my-project \
  --iterations 5 \
  --max-files 100 \
  --model codellama \
  --format pdf \
  --output production_docs \
  --verbose
```

**Result:** Highest quality, comprehensive

### Testing/Development

```bash
python run.py \
  --directory ./test-project \
  --max-files 10 \
  --iterations 1 \
  --verbose
```

**Result:** Quick feedback for testing

### API Documentation

```bash
python run.py \
  --directory ./api \
  --project-type backend \
  --model codellama \
  --format html \
  --iterations 4
```

**Result:** API-focused documentation

### Component Library

```bash
python run.py \
  --directory ./components \
  --project-type frontend \
  --format html \
  --iterations 4
```

**Result:** Component documentation with examples

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Configuration error |
| 3 | File/directory not found |
| 4 | API error |
| 5 | Output error |

## Environment Variables

Commands respect `.env` configuration:

```bash
# Affects all commands
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=codellama
API_TIMEOUT=300
MAX_RETRIES=3
```

See [Configuration Guide](../getting-started/configuration.md) for details.

## Next Steps

- [AI Agent Guide](ai-agent.md) - Understand iterative mode
- [Simple Generator Guide](doc-generator.md) - Single-pass mode
- [Configuration](../getting-started/configuration.md) - Customize behavior
- [Quick Start](../getting-started/quickstart.md) - Get started quickly
