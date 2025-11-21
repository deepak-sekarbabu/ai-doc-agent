# AI Documentation Agent v2.0.0 - Complete Guide

Comprehensive documentation for the AI Documentation Agent with semantic analysis - an intelligent system that generates, critiques, and refines technical documentation autonomously.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [Output Structure](#output-structure)
- [Advanced Topics](#advanced-topics)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Overview

### What is AI Documentation Agent?

An autonomous AI agent that:

1. Analyzes your codebase with semantic code analysis
2. Performs deep relationship and architecture analysis
3. Generates comprehensive documentation enhanced with semantic insights
4. Critiques its own output with semantic understanding
5. Iteratively refines until quality standards are met
6. Produces professional documentation in multiple formats

### Key Benefits

- **Save Time** - Automated documentation generation
- **High Quality** - Iterative refinement ensures comprehensive coverage
- **Semantic Analysis** - Deep code relationship and architecture understanding
- **Consistent** - Follows structured documentation patterns
- **Flexible** - Multiple output formats and customization options
- **Intelligent** - Auto-detects project type and prioritizes important files

### Use Cases

- 📚 Generate README files for open-source projects
- 📖 Create internal documentation for team projects
- 🎓 Document learning projects and portfolios
- 🏢 Produce technical specifications for clients
- 🔄 Maintain up-to-date documentation during development

## Architecture

### System Components

```
┌─────────────────────────────────────────┐
│     AI Documentation Agent v2.0.0       │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────────────────────┐   │
│  │   Codebase Analyzer              │   │
│  │   - File Discovery               │   │
│  │   - Project Type Detection       │   │
│  │   - Priority Sorting             │   │
│  └──────────────────────────────────┘   │
│                                         │
│                 ▼                       │
│  ┌──────────────────────────────────┐   │
│  │   Semantic Code Analyzer         │   │
│  │   - Relationship Analysis        │   │
│  │   - Architecture Detection       │   │
│  │   - Dependency Mapping           │   │
│  └──────────────────────────────────┘   │
│                 ▼                       │
│  ┌──────────────────────────────────┐   │
│  │   Documentation Generator        │   │
│  │   - Template Building            │   │
│  │   - LLM Integration              │   │
│  │   - Semantic Enhancement         │   │
│  └──────────────────────────────────┘   │
│                 ▼                       │
│  ┌──────────────────────────────────┐   │
│  │   Quality Assurance Loop         │   │
│  │   - Self-Critique                │   │
│  │   - Semantic Validation          │   │
│  │   - Refinement                   │   │
│  └──────────────────────────────────┘   │
│                 ▼                       │
│  ┌──────────────────────────────────┐   │
│  │   Output Manager                 │   │
│  │   - Format Export                │   │
│  │   - Metrics Reporting            │   │
│  │   - File Saving                  │   │
│  └──────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

### Data Flow

1. **Input** → Codebase directory
2. **Analysis** → File discovery and prioritization
3. **Generation** → Initial documentation draft
4. **Critique** → AI-powered quality assessment
5. **Refinement** → Improvement based on critique
6. **Iteration** → Repeat steps 4-5 until quality threshold
7. **Output** → Formatted documentation file

## Installation

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Ollama (for LLM)
ollama --version

# wkhtmltopdf (optional, for PDF)
wkhtmltopdf --version
```

### Step-by-Step Setup

#### 1. Install Ollama

```bash
# Visit https://ollama.ai/download
# Or use package manager:

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 2. Pull an LLM Model

```bash
# Start Ollama server
ollama serve

# Pull a model (choose one)
ollama pull llama2:7b        # Fast, good quality
ollama pull mistral          # Better quality
ollama pull codellama        # Best for code
ollama pull llama2:13b       # Highest quality
```

#### 3. Install Python Dependencies

```bash
# From project root
pip install -r config/requirements.txt

# Or install as package
pip install .
```

#### 4. Configure Environment

```bash
# Copy template
cp config/.env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

#### 5. Verify Installation

```bash
# Test the agent
ai-doc-agent --help

# Generate docs for sample project
ai-doc-agent --directory ./examples --output test
```

## Configuration

### Environment Variables

Located in `.env` file:

#### API Configuration

```bash
# Ollama API endpoint
OLLAMA_API_URL=http://localhost:11434/api/generate

# API timeout in seconds
API_TIMEOUT=300

# Optional API key (if using hosted Ollama)
OLLAMA_API_KEY=your_key_here
```

#### Model Selection

```bash
# Model name (must be pulled with ollama pull)
MODEL_NAME=llama2:7b

# Alternative models:
# MODEL_NAME=mistral
# MODEL_NAME=codellama
# MODEL_NAME=llama2:13b
```

#### Agent Behavior

```bash
# Maximum retry attempts for API calls
MAX_RETRIES=3

# Base delay between retries (exponential backoff)
RETRY_DELAY=2

# Enable response caching (future feature)
ENABLE_CACHING=true

# Quality threshold for accepting documentation
CRITIQUE_THRESHOLD=0.8
```

### Configuration Tips

- **Fast Iterations**: Use `llama2:7b` with `API_TIMEOUT=180`
- **High Quality**: Use `codellama` or `mistral` with `API_TIMEOUT=600`
- **Reliability**: Set `MAX_RETRIES=5` and `RETRY_DELAY=3`
- **Production**: Use larger models and increase timeout

## Usage

### Basic Commands

```bash
# Quick start - analyze current directory
ai-doc-agent

# Analyze specific directory
ai-doc-agent --directory /path/to/project

# Generate HTML output
ai-doc-agent --format html

# Specify output filename
ai-doc-agent --output my_project_docs

# Verbose logging
ai-doc-agent --verbose
```

- **Graceful Degradation** - Falls back to simpler formats
- **Detailed Errors** - Clear error messages with solutions
- **Recovery** - Continues after non-critical errors

## Output Structure

Generated documentation includes these sections:

### 1. Project Overview

- High-level description
- Primary technologies
- Target audience
- Use cases

### 2. Architecture and Design

- Overall architecture
- Component structure
- Design patterns
- Folder organization
- State management
- Performance strategies

### 3. Key Components and Modules

For each component:

- Purpose and functionality
- Key features
- Dependencies
- Implementation details

### 4. Development Setup

- Prerequisites
- Installation steps
- Environment configuration
- Available scripts

### 5. Deployment

- Build process
- Deployment options
- Hosting considerations

### 6. File Documentation

For each file:

- File path and purpose
- Functions/classes/methods
- Parameters and return values
- Usage examples

### 7. Best Practices

- Coding standards
- Performance considerations
- Accessibility features
- Security considerations

## Advanced Topics

### Custom Prompts

Edit `src/langgraph_agent.py` to customize prompts:

```python
def _build_critique_prompt(self, documentation: str) -> str:
    return f"""Your custom critique prompt here...
    
    Focus on:
    1. Your specific criteria
    2. Your quality standards
    3. Your documentation style
    
    {documentation}
    """
```

> **Note**: The project provides two agent implementations. See [Agent Implementations Comparison](features/agent-implementations.md) for details on both approaches.

### Adding New File Types

Edit `src/doc_generator.py`:

```python
SUPPORTED_EXTENSIONS = frozenset([
    ".py", ".js", ".ts",  # existing
    ".dart",  # Add Dart
    ".scala",  # Add Scala
    ".r",  # Add R
])
```

### Custom Output Formats

Extend the save function in `src/doc_generator.py`:

```python
elif output_format.lower() == "asciidoc":
    # Add your custom format handler
    content = convert_to_asciidoc(content)
    filename = f"{base_name}.adoc"
```

### Integration with CI/CD

```yaml
# .github/workflows/docs.yml
name: Generate Documentation
on: [push]
jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Docs
        run: |
          pip install -r config/requirements.txt
          ai-doc-agent --output docs/API
```

## API Reference

### AIAgent Class

```python
from src.agent_core import AIAgent, AgentConfig

# Create configuration
config = AgentConfig()
config.max_retries = 5
config.retry_delay = 3

# Initialize agent
agent = AIAgent(
    directory="./my-project",
    max_files=50,
    model="codellama",
    project_type="backend",
    output_format="markdown",
    output_file="api_docs",
    config=config
)

# Run documentation generation
exit_code = agent.run(max_iterations=5)
```

> **Note**: This documents the [AIAgent](file:///c:/Projects/ai-doc-agent/src/agent_core.py) implementation. The project also provides a [LangGraph-based implementation](features/agent-implementations.md).

### Standalone Functions

```python
from src.doc_generator import (
    generate_documentation,
    find_code_files,
    detect_project_type
)

# Detect project type
project_type = detect_project_type("./my-app")

# Find code files
files = find_code_files("./my-app", max_files=30, project_type="frontend")

# Generate documentation
file_contents = [{"path": "main.py", "content": "..."}]
docs = generate_documentation(file_contents, output_format="markdown")
```

## Troubleshooting

### Common Issues

#### Issue: "Cannot connect to Ollama"

**Solution:**

```bash
# 1. Start Ollama
ollama serve

# 2. Verify it's running
curl http://localhost:11434/api/tags

# 3. Check .env configuration
cat .env | grep OLLAMA_API_URL
```

#### Issue: "API Timeout"

**Solutions:**

```bash
# Increase timeout in .env
API_TIMEOUT=600

# Or reduce files
ai-doc-agent --max-files 20

# Or use faster model
MODEL_NAME=llama2:7b
```

#### Issue: "No files found"

**Solutions:**

```bash
# Check directory path
ai-doc-agent --directory /absolute/path/to/project

# Use verbose mode
ai-doc-agent --verbose

# Check if files are in ignored directories
# Edit IGNORED_DIRECTORIES in src/doc_generator.py
```

#### Issue: "Poor documentation quality"

**Solutions:**

```bash
# Increase iterations
ai-doc-agent --max-iterations 5

# Use better model
ai-doc-agent --model codellama

# Analyze more files
ai-doc-agent --max-files 100

# Manually specify project type
ai-doc-agent --project-type backend
```

#### Issue: "PDF generation failed"

**Solution:**

```bash
# Install wkhtmltopdf
# Windows: choco install wkhtmltopdf
# Mac: brew install wkhtmltopdf
# Linux: sudo apt-get install wkhtmltopdf

# Or use markdown/html instead
ai-doc-agent --format markdown
```

## Best Practices

### For Best Quality

1. **Use Appropriate Models**
   - Small projects: `llama2:7b`
   - Medium projects: `mistral`
   - Large/complex: `codellama` or `llama2:13b`

2. **Set Sufficient Iterations**
   - Quick docs: 2 iterations
   - Standard: 3 iterations
   - High quality: 5 iterations

3. **Provide Context**
   - Include README files in analysis
   - Analyze configuration files
   - Don't set max-files too low

4. **Specify Project Type**
   - Manual specification is more accurate
   - Helps with file prioritization
   - Improves documentation relevance

### For Best Performance

1. **Start Small**

   ```bash
   ai-doc-agent --max-files 20 --max-iterations 2
   ```

2. **Use Fast Models**

   ```bash
   MODEL_NAME=llama2:7b
   ```

3. **Increase Timeout**

   ```bash
   API_TIMEOUT=600
   ```

4. **Monitor Resources**

   ```bash
   # Check Ollama memory usage
   ollama ps
   ```

### For Production Use

1. **Version Control**

   ```bash
   # Track generated docs
   git add docs/
   git commit -m "Update documentation"
   ```

2. **Automation**

   ```bash
   # Add to pre-commit hook
   ai-doc-agent --output docs/API
   ```

3. **Quality Checks**

   ```bash
   # Always use verbose mode first
   ai-doc-agent --verbose
   
   # Review langgraph_agent.log
   tail -f langgraph_agent.log
   ```

4. **Backup**

   ```bash
   # Keep previous versions
   cp output/docs.md output/docs_backup_$(date +%Y%m%d).md
   ```

---

**For More Information:**

- [Bundling Guide](deployment/bundling.md)
- [Project Structure](reference/structure.md)
- [Examples](examples/samples.md)

**Support:**

- Check logs: `langgraph_agent.log`
- Run with: `--verbose`
- Review: Troubleshooting section above
