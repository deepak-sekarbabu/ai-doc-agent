# AI Doc Agent Project (`ai-doc-agent`)

This document provides a comprehensive overview of the `ai-doc-agent` project, designed to be used as a context for AI-driven development.

## Project Overview

The `ai-doc-agent` is a sophisticated Python-based tool that automates the generation of technical documentation for code projects. It leverages Large Language Models (LLMs) through Ollama to analyze a codebase, generate initial documentation, and then iteratively critique and refine its own output to improve quality. This iterative process is implemented as a stateful graph using LangGraph.

**Key Technologies:**

*   **Backend:** Python
*   **AI/LLM:** Ollama (local or cloud), LangChain, LangGraph
*   **Dependencies:** `requests` (for API calls), `markdown`, `pdfkit` (for output formats).
*   **Documentation:** `MkDocs` with the `Material` theme.
*   **Testing:** `pytest`
*   **Packaging:** `setuptools`, `PyInstaller` (for executables), `Docker`

## Building and Running

### 1. Installation

The project is a Python application. Install dependencies from `config/requirements.txt`:

```bash
pip install -r config/requirements.txt
```

For development, install the dev dependencies:

```bash
pip install -e .[dev]
```

### 2. Configuration

Configuration is managed through a `.env` file. Copy the example and edit it as needed:

```bash
cp config/.env.example .env
```

The `.env` file contains settings for Ollama (mode, model name), API timeouts, and agent behavior (caching, retries).

### 3. Running the Agent

The primary entry point is `run.py`, which executes the main AI agent from `src/langgraph_agent.py` (the LangGraph-based implementation). The project also provides an original implementation in `src/ai_agent.py`.

**To run the agent:**

```bash
# Analyze the current directory
python run.py

# Analyze a specific directory
python run.py --directory /path/to/your/project
```

The script can also be run as an installed package:

```bash
# After installing with 'pip install .'
ai-doc-agent --directory /path/to/your/project
```

## Development Conventions

### Testing

The project uses `pytest` for unit testing. Tests are located in the `tests/` directory.

**To run the test suite:**

```bash
pytest
```

**To run tests with coverage:**

```bash
pytest --cov=src --cov-report=html
```

### Code Style and Quality

The project enforces a high standard of code quality through its CI pipeline (`.github/workflows/ci.yml`). All contributions must pass:

*   **Formatting:** `black`
*   **Linting:** `flake8`
*   **Type Checking:** `mypy`

### Continuous Integration (CI)

The CI pipeline on GitHub Actions automates testing across multiple Python versions, code quality checks, and build verification.

## Documentation

The project's own documentation is built using `MkDocs` and is located in the `docs/` directory.

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

The documentation site configuration is in `mkdocs.yml`.
