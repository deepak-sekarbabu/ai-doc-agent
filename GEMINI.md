# AI Doc Agent Project (`ai-doc-agent`) - Version 2.0.0

This document provides a comprehensive overview of the `ai-doc-agent` project, designed to be used as a context for AI-driven development.

## Project Overview

The `ai-doc-agent` v2.0.0 is a sophisticated Python-based tool that automates the generation of technical documentation for code projects with advanced semantic code analysis. It leverages Large Language Models (LLMs) through Ollama to analyze a codebase, perform semantic relationship analysis, generate initial documentation, and then iteratively critique and refine its own output to improve quality. This iterative process is implemented as a stateful graph using LangGraph with semantic analysis capabilities.

**Key Technologies:**

*   **Backend:** Python 3.8+
*   **AI/LLM:** Ollama (local or cloud), LangChain, LangGraph
*   **Semantic Analysis:** Advanced code relationship and architecture analysis
*   **Dependencies:** `requests` (for API calls), `markdown`, `pdfkit` (for output formats), `ast` (for code parsing)
*   **Documentation:** `MkDocs` with the `Material` theme
*   **Testing:** `pytest` with coverage reporting
*   **Packaging:** `setuptools`, `PyInstaller` (for executables), `Docker`
*   **Code Quality:** `black`, `flake8`, `mypy`

## Building and Running

### 1. Installation

The project is a Python application. Install using the package installation method:

```bash
git clone https://github.com/deepak-sekarbabu/ai-doc-agent.git
cd ai-doc-agent

# Install with development dependencies (recommended)
pip install -e .[dev]
```

This installs the package in editable mode and registers the `ai-doc-agent` console script.

### 2. Configuration

Configuration is managed through a `.env` file. Copy the example and edit it as needed:

```bash
cp .env.example .env
```

The `.env` file contains settings for Ollama (mode, model name), API timeouts, agent behavior (caching, retries), and semantic analysis parameters.

### 3. Running the Agent

The primary entry point is the `ai-doc-agent` console script, which executes the main AI agent from `src/langgraph_agent.py` (the LangGraph-based implementation with semantic analysis). The project also provides an original implementation in `src/ai_agent.py`.

**To run the agent:**

```bash
# Analyze the current directory
ai-doc-agent

# Analyze a specific directory
ai-doc-agent --directory /path/to/your/project

# Generate documentation with semantic analysis
ai-doc-agent --directory ./my-project --format html
```

## Development Conventions

### Testing

The project uses `pytest` for comprehensive unit testing. Tests are located in the `tests/` directory and include semantic analysis testing.

**To run the test suite:**

```bash
pytest
```

**To run tests with coverage:**

```bash
pytest --cov=src --cov-report=html
```

**To run semantic analysis tests:**

```bash
pytest -k "semantic"
```

### Code Style and Quality

The project enforces a high standard of code quality through its CI pipeline (`.github/workflows/ci.yml`). All contributions must pass:

*   **Formatting:** `black`
*   **Linting:** `flake8`
*   **Type Checking:** `mypy`

### Continuous Integration (CI)

The CI pipeline on GitHub Actions automates testing across multiple Python versions, code quality checks, and build verification.

## Documentation

The project's comprehensive documentation is built using `MkDocs` with the Material theme and is located in the `docs/` directory. The documentation includes semantic analysis guides, API references, and deployment instructions.

**To serve the documentation locally:**

1.  Install MkDocs dependencies:
    ```bash
    pip install mkdocs mkdocs-material
    ```
2.  Start the local development server:
    ```bash
    mkdocs serve
    ```
3.  Open your browser to `http://localhost:8000`.

**Online Documentation:** https://deepak-sekarbabu.github.io/ai-doc-agent/

The documentation site configuration is in `mkdocs.yml`.
