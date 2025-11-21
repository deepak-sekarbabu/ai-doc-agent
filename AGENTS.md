# AGENTS.md - AI Documentation Agent Development Guide

## Build/Test/Lint Commands

```bash
# Install in editable mode with dev dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run single test
pytest tests/test_ai_agent.py::TestAIAgent::test_agent_config_defaults

# Run by marker
pytest -m unit

# Lint with black, flake8, mypy
black src/ tests/
flake8 src/ tests/
mypy src/

# Test coverage (minimum 85%)
pytest --cov=src --cov-fail-under=85

# Generate documentation locally
mkdocs serve
```

## Architecture & Codebase Structure

**Python 3.8+** package organized as:
- `src/` - Main package with agents: `langgraph_agent.py` (LangGraph-based, default), `ai_agent.py` (manual critique loop), `base_agent.py` (base classes)
- `src/utils/` - Core modules: `api_utils.py` (Ollama API + ResponseCache), `file_utils.py` (file discovery), `semantic_code_analyzer.py` (dependency graph), `semantic_critique.py` (critique analysis)
- `tests/` - Unit tests following `test_*.py` pattern
- `config/` - Requirements and env templates
- `docs/` - MkDocs site

**Dependencies**: LangChain, LangGraph, requests, python-dotenv, markdown, pdfkit (wkhtmltopdf binary required), MkDocs

## Code Style & Conventions

**Imports**: Try-except for relative vs absolute imports (handle both); dependencies at top of file
**Types**: Use `typing` annotations (Dict, List, Optional, Union); `dataclass` for config
**Exceptions**: Custom class hierarchy (AgentError → ConfigurationError, AnalysisError, GenerationError, DocGeneratorError)
**Error Handling**: Validate input in `__post_init__`, wrap API calls in retries with exponential backoff, log before raising
**Naming**: Lowercase snake_case for functions/variables, PascalCase for classes, ALL_CAPS for constants
**Docstrings**: Module-level docstrings; class/method docstrings (Sphinx format with Args/Returns)
**Logging**: Use `logger = logging.getLogger(__name__)` per module; log at INFO/ERROR/WARNING levels
**Testing**: Mock external calls (requests.post), use fixtures for tempdir, name test functions `test_*`
**Config**: Load from env via `AgentConfig` dataclass with validation; defaults in `os.getenv()`
