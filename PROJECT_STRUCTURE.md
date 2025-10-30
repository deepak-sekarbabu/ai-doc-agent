# Project Structure

This document explains the organized structure of the AI Documentation Agent project.

## Directory Layout

```
ai-doc-agent/
│
├── 📁 src/                          # Source Code
│   ├── langgraph_agent.py           # LangGraph-based AI agent (default)
│   ├── ai_agent.py                  # Original AI agent with manual critique loop
│   ├── base_agent.py                # Base agent class
│   ├── doc_generator.py             # Core documentation generator
│   ├── utils/                       # Utility functions
│   │   ├── api_utils.py             # Ollama API integration
│   │   ├── file_utils.py            # File discovery and processing
│   │   ├── text_utils.py            # Text processing utilities
│   │   ├── semantic_code_analyzer.py  # Code relationship analysis
│   │   └── semantic_critique.py     # Documentation critique analysis
│   └── __init__.py                  # Package initialization
│
├── 📁 config/                       # Configuration Files
│   ├── .env.example                 # Environment template
│   └── requirements.txt             # Python dependencies
│
├── 📁 docs/                         # MkDocs Documentation
│   └── (MkDocs site files)
│
├── 📁 build/                        # Build & Deployment
│   ├── Dockerfile                   # Docker image definition
│   └── docker-compose.yml           # Docker orchestration
│
├── 📁 tests/                        # Unit Tests
│   └── (Test files)
│
├── 📁 examples/                     # Example Projects
│   └── (Sample projects for testing)
│
├── 📁 output/                       # Generated Documentation
│   └── (Generated .md, .html, .pdf files)
│
├── 📄 setup.py                      # Package setup configuration
├── 📄 mkdocs.yml                    # Documentation site config
├── 📄 README.md                     # Project overview
├── 📄 .gitignore                    # Git ignore rules
└── 📄 PROJECT_STRUCTURE.md          # This file
```

## File Purposes

### Root Level

- **setup.py** - Python package configuration for pip installation
- **mkdocs.yml** - MkDocs documentation site configuration
- **README.md** - Quick start guide and project overview
- **.gitignore** - Files and directories to exclude from git

### src/ - Source Code

Contains the core application logic:

- **langgraph_agent.py** - LangGraph-based AI agent (default) with semantic analysis integration
- **ai_agent.py** - Original AI agent with manual critique-refinement loop and semantic analysis
- **base_agent.py** - Base agent class with common functionality
- **doc_generator.py** - Documentation generation utilities
- **utils/** - Utility functions including semantic analysis:
  - **api_utils.py** - Ollama API integration
  - **file_utils.py** - File discovery and processing
  - **text_utils.py** - Text processing utilities
  - **semantic_code_analyzer.py** - Code relationship and architecture analysis
  - **semantic_critique.py** - Documentation critique analysis
- **__init__.py** - Package exports and version info

### config/ - Configuration

All configuration files in one place:

- **.env.example** - Template for environment variables
- **requirements.txt** - Python package dependencies

### docs/ - Documentation

MkDocs documentation site files and configuration.

### build/ - Build Scripts

Everything needed to build and deploy:

- **build.bat** / **build.sh** - Automated build scripts
- **ai_agent.spec** - PyInstaller executable configuration
- **Dockerfile** - Container image definition
- **docker-compose.yml** - Docker orchestration

### tests/ - Testing

Unit and integration tests (to be implemented):

- Test files following pytest conventions
- Test data and fixtures

### examples/ - Examples

Sample projects for testing and demonstration:

- **sample_project.py** - Simple Python calculator
- Additional example projects

### output/ - Generated Files

Default location for generated documentation (gitignored)

## Benefits of This Structure

### ✅ Separation of Concerns
- Source code isolated in `src/`
- Configuration centralized in `config/`
- Documentation in `docs/`

### ✅ Easy Navigation
- Logical grouping of related files
- Clear purpose for each directory
- Intuitive file locations

### ✅ Scalability
- Easy to add new modules in `src/`
- Simple to add tests in `tests/`
- Clear place for examples

### ✅ Distribution Ready
- Clean package structure for pip
- Build scripts in dedicated directory
- Proper .gitignore configuration

### ✅ Maintainability
- Easier to find files
- Simpler refactoring
- Better collaboration

## Quick Reference

### Running the Agent

```bash
# Direct execution
python -m src.ai_agent --directory ./my-project

# After pip install
ai-doc-agent --directory ./my-project

# Using LangGraph agent
python -m src.langgraph_agent --directory ./my-project
```

### Building

```bash
# Docker
cd build && docker-compose build

# Package
python -m build
```

### Adding New Features

1. Add code to `src/`
2. Add tests to `tests/`
3. Update docs in `docs/`
4. Add examples in `examples/`

### Configuration

1. Copy `config/.env.example` to `.env`
2. Edit `.env` with your settings
3. Dependencies in `config/requirements.txt`

## Key Features of Version 2.0.0

- **Semantic Code Analysis**: Advanced code relationship and architecture analysis
- **LangGraph Integration**: State-of-the-art agent orchestration with semantic insights
- **Enhanced Documentation**: Semantic analysis results integrated into documentation generation
- **Comprehensive Testing**: Full test coverage with CI/CD integration
- **Docker Support**: Complete containerization for isolated runs
- **Multi-Format Output**: Markdown, HTML, and PDF generation
- **Extensible Architecture**: Plugin system for new languages and output formats

## Project Evolution

The project has evolved from a simple AI agent to a comprehensive documentation generation system with:

1. **Version 1.0**: Basic AI agent with iterative refinement
2. **Version 2.0**: Added semantic code analysis, LangGraph integration, and enhanced architecture

The current structure supports both the original AIAgent implementation and the LangGraph-based agent, providing flexibility for different use cases while maintaining backward compatibility.

```
OLD LOCATION              →  NEW LOCATION
─────────────────────────────────────────────
ai_agent.py               →  src/ai_agent.py
doc_generator.py          →  src/doc_generator.py
README.md                 →  docs/README.md
README_DOC_GENERATOR.md   →  docs/README_DOC_GENERATOR.md
BUNDLING_GUIDE.md         →  docs/BUNDLING_GUIDE.md
.env.example              →  config/.env.example
requirements.txt          →  config/requirements.txt
MANIFEST.in               →  config/MANIFEST.in
build.bat                 →  build/build.bat
build.sh                  →  build/build.sh
ai_agent.spec             →  build/ai_agent.spec
Dockerfile                →  build/Dockerfile
docker-compose.yml        →  build/docker-compose.yml
```


