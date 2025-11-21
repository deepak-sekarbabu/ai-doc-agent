# Project Structure Reference

The AI Documentation Agent follows a standard Python project structure:

```
Docgenerator/
├── src/                    # Source code
│   ├── langgraph_agent.py # Main AI agent using LangGraph (default)
│   ├── agent_core.py      # Core agent logic
│   ├── doc_generator.py   # Core documentation utilities
│   └── __init__.py        # Package initialization
├── config/                 # Configuration files
│   ├── .env.example       # Environment template
│   ├── requirements.txt   # Python dependencies
│   └── MANIFEST.in        # Package manifest
├── docs/                   # Documentation
│   ├── guide.md           # Complete user guide
│   ├── index.md           # Documentation home page
│   ├── getting-started/   # Quick start guides
│   ├── guide/             # User guides
│   ├── features/          # Feature documentation
│   ├── deployment/        # Deployment guides
│   ├── reference/         # Reference materials
│   ├── development/       # Development guides
│   ├── examples/          # Example documentation
│   └── stylesheets/       # Custom CSS
├── build/                  # Build & deployment scripts
│   ├── build.bat/.sh      # Build executables
│   └── Dockerfile         # Container definition
├── examples/              # Sample projects for testing
├── tests/                 # Unit tests
├── output/                # Generated documentation
├── run.py                 # Quick launcher
└── setup.py               # Package configuration
```

## Key Directories

### src/

Contains all the source code for the AI Documentation Agent.

- **langgraph_agent.py**: Main AI agent implementation using LangGraph (default).
- **agent_core.py**: Core agent logic and base classes.
- **doc_generator.py**: Utilities for file discovery, processing, and documentation generation.

### config/

Configuration files for the project.

- **.env.example**: Template for environment variables
- **requirements.txt**: Python dependencies
- **MANIFEST.in**: Package manifest for distribution

### docs/

Complete documentation for the project, organized by purpose.

### build/

Build scripts and configuration files for creating distributable packages.

## File Organization Principles

The project follows standard Python project conventions with a clear separation of concerns:

1. **Source code** is isolated in `src/`
2. **Configuration** is in `config/`
3. **Documentation** is in `docs/` with subdirectories for different types
4. **Build artifacts** are in `build/` and `dist/`
5. **Tests** are in `tests/`
6. **Examples** are in `examples/`
7. **Generated output** goes to `output/`

This organization makes the project easy to navigate, maintain, and extend.
