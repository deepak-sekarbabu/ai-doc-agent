# Quick Start

Get up and running with AI Documentation Agent v2.0.0 in under 5 minutes!

## Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.8 or higher
- ✅ Ollama installed and running
- ✅ Git (for cloning the repository)
- ✅ wkhtmltopdf (optional, for PDF generation)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/deepak-sekarbabu/ai-doc-agent.git
cd ai-doc-agent
```

### 2. Install Package

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -e .[dev]          # Installs console scripts
```

This installs the package in editable mode with development dependencies and registers the `ai-doc-agent` console script.

### 3. Configure Environment

```bash
cp .env.example .env
```

The default configuration works for most users. Edit `.env` if you need custom settings (see [Configuration](configuration.md) for details).

### 4. Start Ollama

=== "Windows/macOS/Linux"

    ```bash
    ollama serve
    ```

### 5. Pull an LLM Model

```bash
# Recommended models (choose based on your needs):
ollama pull llama2:7b          # Fast, good quality (2GB)
ollama pull mistral:7b         # Better quality (4GB)
ollama pull codellama:7b       # Best for code (4GB)
ollama pull gpt-oss:120b-cloud # Cloud model (requires API key)
```

## Your First Documentation

### Generate docs for the sample project:

```bash
ai-doc-agent --directory ./examples --output my_first_docs
```

This will:

1. ✅ Analyze the example project with semantic code analysis
2. ✅ Generate comprehensive documentation with AI refinement
3. ✅ Save to `my_first_docs.md` in the current directory

### Check the output:

```bash
# View the generated documentation
cat output/my_first_docs.md

# Or open in your editor
code output/my_first_docs.md
```

## Generate Docs for Your Project

Now try it on your own project:

```bash
ai-doc-agent --directory /path/to/your/project
```

### Quick Examples

=== "Basic"

```bash
# Analyze current directory
ai-doc-agent
```

=== "HTML Output"

```bash
# Generate HTML documentation
ai-doc-agent --directory ./my-app --format html
```

=== "High Quality"

```bash
# Maximum quality with more iterations
ai-doc-agent --directory ./my-app --iterations 5 --max-files 100
```

=== "Specific Type"

```bash
# Specify project type for better results
ai-doc-agent --directory ./api --project-type backend
```

## Common Commands

```bash
# Quick documentation (fast)
ai-doc-agent --max-files 15 --iterations 2

# Standard documentation
ai-doc-agent --directory ~/my-project

# High-quality documentation
ai-doc-agent --directory ~/my-project --iterations 5 --model codellama

# Generate HTML or PDF
ai-doc-agent --format html
ai-doc-agent --format pdf

# Verbose output for debugging
ai-doc-agent --verbose
```

## Understanding the Output

The generated documentation includes:

1. **Project Overview** - High-level description and purpose
2. **Architecture & Design** - System design with semantic relationships
3. **Semantic Code Analysis** - Code dependencies and architectural patterns
4. **Key Components** - Detailed module documentation with relationships
5. **Development Setup** - Installation and configuration
6. **Deployment Guide** - Build and hosting instructions
7. **File Documentation** - Functions, classes, and methods with examples
8. **Best Practices** - Standards, security, and recommendations

## Quick Troubleshooting

!!! failure "Cannot connect to Ollama"
    
    **Solution:** Make sure Ollama is running:
    ```bash
    ollama serve
    ```

!!! failure "No files found"

**Solution:** Check the directory path:
```bash
ai-doc-agent --directory /absolute/path/to/project --verbose
```

!!! failure "API Timeout"

**Solution:** Reduce the number of files or increase timeout:
```bash
ai-doc-agent --max-files 20
# Or edit .env: API_TIMEOUT=600
```

## Next Steps

✅ You're all set! Now learn more:

- [Configuration](configuration.md) - Customize the agent for your needs
- [Installation Methods](installation.md) - Docker, standalone executables, etc.
- [Complete Guide](../guide.md) - Learn all features and advanced usage
- [User Guide](../guide/overview.md) - Deep dive into capabilities

## Tips for Best Results

!!! tip "Choose the Right Model"
    - **Small projects** → `llama2:7b` (fast)
    - **Medium projects** → `mistral` (balanced)
    - **Large/complex** → `codellama` (best quality)

!!! tip "Adjust File Count"
    - Start with `--max-files 20` for testing
    - Increase to 50-100 for comprehensive docs
    - Too many files may cause timeouts

!!! tip "Iterative Refinement"
    - 2 iterations → Quick documentation
    - 3 iterations → Standard quality (default)
    - 5 iterations → Maximum quality

## Command Reference

| Option | Description | Example |
|--------|-------------|---------|
| `--directory DIR` | Project to analyze | `--directory ~/my-app` |
| `--format FORMAT` | Output format | `--format html` |
| `--output FILE` | Output filename | `--output my_docs` |
| `--max-files N` | Max files to analyze | `--max-files 50` |
| `--iterations N` | Refinement cycles | `--iterations 5` |
| `--model MODEL` | LLM model | `--model codellama` |
| `--project-type TYPE` | Project type | `--project-type backend` |
| `--verbose` | Verbose logging | `--verbose` |

## Support

Need help?

- 📖 Check the [Complete Guide](../guide.md)
- 🔧 Review [Configuration Options](configuration.md)
- 🐛 Enable verbose mode: `--verbose`
- 📝 Check logs: `ai_agent.log`
