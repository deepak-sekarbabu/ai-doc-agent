# Quick Start

Get up and running with AI Documentation Agent in under 5 minutes!

## Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.8 or higher
- ✅ Ollama installed and running
- ✅ Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/deepak-sekarbabu/ai-doc-agent.git
cd ai-doc-agent
```

### 2. Install Dependencies

```bash
pip install -r config/requirements.txt
```

### 3. Configure Environment

```bash
cp config/.env.example .env
```

The default configuration works for most users. Edit `.env` if you need custom settings.

### 4. Start Ollama

=== "Windows/macOS/Linux"

    ```bash
    ollama serve
    ```

### 5. Pull an LLM Model

```bash
# Recommended for getting started (fast, good quality)
ollama pull llama2:7b

# Or choose an alternative:
# ollama pull mistral        # Better quality
# ollama pull codellama      # Best for code
```

## Your First Documentation

### Generate docs for the sample project:

```bash
python run.py --directory ./examples --output my_first_docs
```

This will:

1. ✅ Analyze the example project
2. ✅ Generate comprehensive documentation
3. ✅ Save to `output/my_first_docs.md`

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
python run.py --directory /path/to/your/project
```

### Quick Examples

=== "Basic"

    ```bash
    # Analyze current directory
    python run.py
    ```

=== "HTML Output"

    ```bash
    # Generate HTML documentation
    python run.py --directory ./my-app --format html
    ```

=== "High Quality"

    ```bash
    # Maximum quality with more iterations
    python run.py --directory ./my-app --iterations 5 --max-files 100
    ```

=== "Specific Type"

    ```bash
    # Specify project type for better results
    python run.py --directory ./api --project-type backend
    ```

## Common Commands

```bash
# Quick documentation (fast)
python run.py --max-files 15 --iterations 2

# Standard documentation
python run.py --directory ~/my-project

# High-quality documentation
python run.py --directory ~/my-project --iterations 5 --model codellama

# Generate HTML or PDF
python run.py --format html
python run.py --format pdf

# Verbose output for debugging
python run.py --verbose
```

## Understanding the Output

The generated documentation includes:

1. **Project Overview** - High-level description and purpose
2. **Architecture** - System design and component structure
3. **Key Components** - Detailed module documentation
4. **Development Setup** - Installation and configuration
5. **Deployment Guide** - Build and hosting instructions
6. **File Documentation** - Functions, classes, and methods
7. **Best Practices** - Standards and recommendations

## Quick Troubleshooting

!!! failure "Cannot connect to Ollama"
    
    **Solution:** Make sure Ollama is running:
    ```bash
    ollama serve
    ```

!!! failure "No files found"
    
    **Solution:** Check the directory path:
    ```bash
    python run.py --directory /absolute/path/to/project --verbose
    ```

!!! failure "API Timeout"
    
    **Solution:** Reduce the number of files or increase timeout:
    ```bash
    python run.py --max-files 20
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
