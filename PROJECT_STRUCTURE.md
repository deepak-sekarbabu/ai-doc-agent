# Project Structure

This document explains the organized structure of the AI Documentation Agent project.

## Directory Layout

```
Docgenerator/
│
├── 📁 src/                          # Source Code
│   ├── ai_agent.py                  # Main AI agent with iterative refinement
│   ├── doc_generator.py             # Core documentation generator
│   └── __init__.py                  # Package initialization
│
├── 📁 config/                       # Configuration Files
│   ├── .env.example                 # Environment template
│   ├── requirements.txt             # Python dependencies
│   └── MANIFEST.in                  # Package manifest
│
├── 📁 docs/                         # Documentation
│   ├── README.md                    # Complete user guide
│   ├── README_DOC_GENERATOR.md      # Simple generator docs
│   └── BUNDLING_GUIDE.md            # Distribution guide
│
├── 📁 build/                        # Build & Deployment
│   ├── build.bat                    # Windows build script
│   ├── build.sh                     # Linux/Mac build script
│   ├── ai_agent.spec                # PyInstaller configuration
│   ├── Dockerfile                   # Docker image definition
│   └── docker-compose.yml           # Docker compose config
│
├── 📁 tests/                        # Unit Tests (future)
│   └── README.md                    # Testing documentation
│
├── 📁 examples/                     # Example Projects
│   ├── sample_project.py            # Sample Python project
│   └── README.md                    # Examples documentation
│
├── 📁 output/                       # Generated Documentation
│   └── (Generated .md, .html, .pdf files)
│
├── 📄 setup.py                      # Package setup configuration
├── 📄 run.py                        # Quick launcher script
├── 📄 README.md                     # Project overview
├── 📄 .gitignore                    # Git ignore rules
└── 📄 PROJECT_STRUCTURE.md          # This file
```

## File Purposes

### Root Level

- **setup.py** - Python package configuration for pip installation
- **run.py** - Convenience script to run agent from project root
- **README.md** - Quick start guide and project overview
- **.gitignore** - Files and directories to exclude from git

### src/ - Source Code

Contains the core application logic:

- **ai_agent.py** - Main AI agent with critique/refine loop
- **doc_generator.py** - Documentation generation utilities
- **__init__.py** - Package exports and version info

### config/ - Configuration

All configuration files in one place:

- **.env.example** - Template for environment variables
- **requirements.txt** - Python package dependencies
- **MANIFEST.in** - Files to include in package distribution

### docs/ - Documentation

User-facing documentation:

- **README.md** - Complete feature and usage documentation
- **README_DOC_GENERATOR.md** - Simple generator documentation
- **BUNDLING_GUIDE.md** - How to create executables and packages

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
# From project root
python run.py --directory ./my-project

# Direct execution
python src/ai_agent.py --directory ./my-project

# After pip install
ai-doc-agent --directory ./my-project
```

### Building

```bash
# Executable
cd build && build.bat  # Windows
cd build && ./build.sh  # Linux/Mac

# Package
python -m build

# Docker
cd build && docker-compose build
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

## Migration from Old Structure

Files were moved as follows:

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

All scripts and configurations updated to reflect new paths.
