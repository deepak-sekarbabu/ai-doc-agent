# AI Documentation Agent - Project Context

## Project Overview

The AI Documentation Agent is an intelligent, self-improving AI system that autonomously generates, critiques, and refines technical documentation for code projects using iterative improvement cycles. It leverages Ollama (or cloud-based) LLMs to analyze codebases and create comprehensive documentation in multiple formats.

### Key Features
- **Iterative Self-Refinement**: AI critiques and improves its own output through multiple refinement cycles
- **Powered by Ollama**: Uses local or cloud LLM for intelligent analysis
- **Multi-Format Output**: Supports Markdown, HTML, and PDF generation
- **Smart File Prioritization**: Automatically identifies and prioritizes important files
- **Auto-Detection**: Detects project type (frontend/backend/mixed)
- **Production Ready**: Includes logging, retries, validation, and error handling
- **Docstring Extraction**: Incorporates existing code documentation
- **Response Caching**: Speeds up repeated runs with intelligent caching

## Architecture & Components

### Directory Structure
```
├── src/                   # Source code
│   ├── langgraph_agent.py # Main AI agent using LangGraph (default)
│   ├── ai_agent.py        # Original AI agent with manual critique loop
│   ├── doc_generator.py   # Core documentation utilities
│   ├── base_agent.py      # Base agent classes and interfaces
│   ├── core/              # Core modules
│   └── utils/             # Utility functions
├── config/                # Configuration files
│   ├── .env.example       # Environment template
│   ├── requirements.txt   # Python dependencies
│   └── MANIFEST.in        # Package manifest
├── docs/                  # Complete MkDocs documentation
├── build/                 # Build & deployment scripts
├── examples/              # Sample projects for testing
├── tests/                 # Unit tests
├── output/                # Generated documentation (gitignored)
├── run.py                 # Quick launcher
├── setup.py               # Package configuration
└── mkdocs.yml             # Documentation site config
```

### Core Components

#### 1. `langgraph_agent.py` (Default Implementation)
- Implements the AI agent using LangGraph for stateful graph-based processing
- Uses a state machine pattern with nodes for analysis, generation, critique, and refinement
- Handles iterative improvement cycles until quality threshold is met or max iterations reached

#### 2. `ai_agent.py` (Original Implementation)
- Original AI agent implementation with manual critique-refinement loop
- Includes caching, retry logic, and comprehensive error handling
- Implements scoring system for determining when documentation is satisfactory

> See [Agent Implementations Comparison](docs/features/agent-implementations.md) for a detailed comparison of both approaches.

#### 3. `base_agent.py`
- Abstract base class for documentation generation agents
- Defines common interfaces and configuration management
- Includes documentation templates and critique/refinement prompts

#### 4. `doc_generator.py`
- Core documentation generation utilities
- File discovery and analysis functions
- Format conversion (Markdown, HTML, PDF)
- Project type detection and code parsing

## Building and Running

### Prerequisites
- Python 3.8+
- Ollama (running locally or accessible API)
- wkhtmltopdf (optional, for PDF generation)

### Installation Methods

#### Method 1: Development Setup
```bash
pip install -r config/requirements.txt
python run.py --help
```

#### Method 2: Package Installation
```bash
pip install .
ai-doc-agent --help
```

#### Method 3: Standalone Executable
```bash
cd build
build.bat  # Windows
./build.sh  # Linux/Mac
```

#### Method 4: Docker Container
```bash
cd build
docker-compose build
docker-compose run --rm ai-doc-agent --directory /workspace
```

### Configuration
Create a `.env` file from the template:
```bash
cp config/.env.example .env
```

Key configuration options:
- `OLLAMA_MODE`: Set to `local` for localhost Ollama, `cloud` for ollama.com
- `MODEL_NAME`: LLM model to use (e.g., `llama2:7b`, `gpt-oss:120b-cloud`)
- `ENABLE_CACHING`: Enable response caching to speed up repeated runs
- `MAX_RETRIES`: Maximum retry attempts for API calls
- `CRITIQUE_THRESHOLD`: Quality threshold for determining when documentation is satisfactory

### Usage Examples

#### Basic Usage
```bash
# Analyze current directory
python run.py

# Analyze specific project
python run.py --directory ./my-project

# Generate HTML documentation
python run.py --directory ./project --format html --output docs
```

#### Advanced Usage
```bash
# Maximum quality with more refinement iterations
python src/ai_agent.py \
  --directory ~/my-app \
  --iterations 5 \
  --max-files 100 \
  --verbose

# Specify project type and model
python src/ai_agent.py \
  --directory ./backend-api \
  --project-type backend \
  --model codellama \
  --format pdf
```

### Command-Line Options
- `--directory DIR`: Directory to analyze (default: current directory)
- `--model MODEL`: Ollama model to use (default: from .env or `gpt-oss:120b-cloud`)
- `--format FORMAT`: Output format: `markdown`, `html`, `pdf` (default: `markdown`)
- `--output FILE`: Output filename (without extension)
- `--max-files N`: Maximum files to analyze (default: 30)
- `--project-type TYPE`: `frontend`, `backend`, `mixed` (default: auto-detected)
- `--iterations N`: Max refinement iterations (default: 3)
- `--verbose`: Enable verbose logging

## Development Conventions

### Code Structure
- All source code is in `src/` directory
- Follows object-oriented design with base classes and concrete implementations
- Uses type hints throughout for better code quality
- Implements abstract base classes for common interfaces

### Testing
- Unit tests in `tests/` directory
- Uses pytest framework
- Includes both unit and integration tests
- Test coverage >80% required for CI/CD

### Documentation
- Comprehensive documentation available at https://deepak-sekarbabu.github.io/ai-doc-agent/
- MkDocs-based documentation site
- API reference and user guides included
- Examples and troubleshooting sections

### Quality Standards
- Code formatting with Black
- Linting with Flake8
- Type checking with MyPy
- All contributions must pass CI/CD pipeline

### Iterative Improvement Process
The agent follows this workflow:
1. **Analyze Codebase** - Discovers files, detects project type
2. **Generate Draft** - Creates initial documentation using LLM
3. **Critique** - AI analyzes its own output for quality
4. **Refine** - Improves documentation based on critique
5. **Iterate** - Repeats until quality threshold or max iterations
6. **Save** - Outputs final documentation in requested format

### Supported Languages
Python, JavaScript, TypeScript, JSX/TSX, Java, C#, Go, PHP, Ruby, Rust, C/C++, HTML, CSS/SCSS, SQL, Shell, Kotlin, Swift, Vue, Svelte, XML, Gradle

## Testing and Quality Assurance

### Running Tests
```bash
# Install test dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific tests
pytest tests/test_doc_generator.py -v
```

### Test Structure
- `test_ai_agent.py`: Tests for the AI agent functionality
- `test_doc_generator.py`: Tests for documentation generation utilities
- Uses unittest framework with mock objects for API calls
- Comprehensive coverage of positive and negative cases

### CI/CD Pipeline
- Automated testing across multiple Python versions (3.8-3.12)
- Code quality checks (Black formatting, Flake8 linting, MyPy type checking)
- Test coverage reporting with Codecov
- Package building and validation