# AI Documentation Agent v2.0.0 - Project Context

## Project Overview

The AI Documentation Agent v2.0.0 is an intelligent, self-improving AI system that autonomously generates, critiques, and refines technical documentation for code projects using iterative improvement cycles with advanced semantic code analysis. It leverages Ollama (or cloud-based) LLMs to analyze codebases, perform semantic relationship analysis, and create comprehensive documentation in multiple formats.

### Key Features
- **Semantic Code Analysis**: Advanced code relationship and architecture analysis
- **Iterative Self-Refinement**: AI critiques and improves its own output through multiple refinement cycles
- **Powered by Ollama**: Uses local or cloud LLM for intelligent analysis
- **Multi-Format Output**: Supports Markdown, HTML, and PDF generation
- **Smart File Prioritization**: Automatically identifies and prioritizes important files
- **Auto-Detection**: Detects project type (frontend/backend/mixed)
- **Production Ready**: Includes logging, retries, validation, and error handling
- **Docstring Extraction**: Incorporates existing code documentation
- **Response Caching**: Speeds up repeated runs with intelligent caching
- **Architecture Recognition**: Identifies design patterns and structural elements

## Architecture & Components

### Directory Structure
```
├── src/                          # Source code
│   ├── langgraph_agent.py        # LangGraph-based AI agent (default)
│   ├── ai_agent.py               # Original AI agent with semantic analysis
│   ├── base_agent.py             # Base agent classes and interfaces
│   ├── doc_generator.py          # Core documentation utilities
│   ├── utils/                    # Utility functions
│   │   ├── api_utils.py          # Ollama API integration
│   │   ├── file_utils.py         # File discovery and processing
│   │   ├── text_utils.py         # Text processing utilities
│   │   ├── semantic_code_analyzer.py    # Code relationship analysis
│   │   └── semantic_critique.py         # Documentation critique analysis
│   └── __init__.py               # Package initialization
├── config/                       # Configuration files
│   ├── .env.example              # Environment template
│   └── requirements.txt          # Python dependencies
├── docs/                         # MkDocs documentation
├── build/                        # Build & deployment scripts
├── examples/                     # Sample projects for testing
├── tests/                        # Unit tests
├── output/                       # Generated documentation (gitignored)
├── setup.py                      # Package configuration
├── mkdocs.yml                    # Documentation site config
└── README.md                     # Project overview
```

### Core Components

#### 1. `langgraph_agent.py` (Default Implementation)
- Implements the AI agent using LangGraph for stateful graph-based processing with semantic analysis
- Uses a state machine pattern with nodes for analysis, semantic analysis, generation, critique, and refinement
- Handles iterative improvement cycles until quality threshold is met or max iterations reached
- Performs advanced code relationship and architecture analysis

#### 2. `ai_agent.py` (Original Implementation)
- Original AI agent implementation with semantic analysis and manual critique-refinement loop
- Includes caching, retry logic, and comprehensive error handling
- Implements scoring system for determining when documentation is satisfactory
- Performs semantic code analysis and validation

#### 3. Semantic Analysis Modules
- `semantic_code_analyzer.py`: Advanced code relationship and architecture analysis
- `semantic_critique.py`: AI-powered documentation critique and validation
- Performs dependency mapping, architecture pattern recognition, and cross-validation

> See [Agent Implementations Comparison](docs/features/agent-implementations.md) for a detailed comparison of both approaches.

#### 4. `base_agent.py`
- Abstract base class for documentation generation agents
- Defines common interfaces and configuration management
- Includes documentation templates and critique/refinement prompts

#### 5. `doc_generator.py`
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

#### Method 1: Package Installation (Recommended)
```bash
git clone https://github.com/deepak-sekarbabu/ai-doc-agent.git
cd ai-doc-agent
pip install -e .[dev]
ai-doc-agent --help
```

#### Method 2: Docker Container
```bash
cd build
docker build -t ai-doc-agent:latest .
docker run --rm -v "$(pwd)/project:/src" ai-doc-agent:latest --directory /src
```

#### Method 3: PyInstaller Bundle
```bash
pip install pyinstaller
pyinstaller --onefile src/ai_agent.py --name ai-doc-agent
./dist/ai-doc-agent --help
```

### Configuration
Create a `.env` file from the template:
```bash
cp .env.example .env
```

Key configuration options:
- `OLLAMA_MODE`: Set to `local` for localhost Ollama, `cloud` for ollama.com
- `MODEL_NAME`: LLM model to use (e.g., `llama2:7b`, `gpt-oss:120b-cloud`)
- `ENABLE_CACHING`: Enable response caching to speed up repeated runs
- `MAX_RETRIES`: Maximum retry attempts for API calls
- `CRITIQUE_THRESHOLD`: Quality threshold for determining when documentation is satisfactory
- `MAX_FILES`: Maximum number of files to analyze (default: 100)
- `MAX_ITERATIONS`: Maximum refinement iterations (default: 3)

### Usage Examples

#### Basic Usage
```bash
# Analyze current directory
ai-doc-agent

# Analyze specific project
ai-doc-agent --directory ./my-project

# Generate HTML documentation
ai-doc-agent --directory ./project --format html --output docs
```

#### Advanced Usage
```bash
# Maximum quality with more refinement iterations
ai-doc-agent \
--directory ~/my-app \
--max-iterations 5 \
--max-files 100 \
--verbose

# Specify project type and model
ai-doc-agent \
--directory ./backend-api \
--project-type backend \
--model codellama \
--format pdf
```

### Command-Line Options
- `--directory DIR`: Directory to analyze (default: current directory)
- `--format FORMAT`: Output format: `markdown`, `html`, `pdf` (default: `markdown`)
- `--output FILE`: Output filename (without extension)
- `--max-files N`: Maximum files to analyze (default: 100)
- `--max-iterations N`: Max refinement iterations (default: 3)
- `--model MODEL`: Ollama model to use (default: from .env or `gpt-oss:120b-cloud`)
- `--project-type TYPE`: `frontend`, `backend`, `mixed` (default: auto-detected)
- `--verbose`: Enable verbose logging
- `--no-cache`: Disable response caching

## Development Conventions

### Code Structure
- All source code is in `src/` directory
- Follows object-oriented design with base classes and concrete implementations
- Uses type hints throughout for better code quality
- Implements abstract base classes for common interfaces

### Testing
- Unit tests in `tests/` directory
- Uses pytest framework with coverage reporting
- Includes semantic analysis and integration tests
- Test coverage >85% required for CI/CD

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
# Install test dependencies (already included in pip install -e .[dev])
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run semantic analysis tests
pytest -k "semantic"

# Run specific tests
pytest tests/test_doc_generator.py -v
```

### Test Structure
- `test_ai_agent.py`: Tests for the AI agent functionality with semantic analysis
- `test_doc_generator.py`: Tests for documentation generation utilities
- `test_semantic_analyzer.py`: Tests for semantic code analysis features
- Uses pytest framework with mock objects for API calls
- Comprehensive coverage of positive and negative cases

### CI/CD Pipeline
- Automated testing across multiple Python versions (3.8-3.12)
- Code quality checks (Black formatting, Flake8 linting, MyPy type checking)
- Test coverage reporting with Codecov (>85% required)
- Package building and validation
- Semantic analysis integration testing