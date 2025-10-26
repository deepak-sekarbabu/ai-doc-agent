# Changelog

All notable changes to the AI Documentation Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Response caching for faster subsequent runs
- Support for more programming languages
- Plugin system for custom extensions
- Web UI for easier usage
- API server mode
- Integration with popular IDEs

---

## [2.0.0] - 2025-01-26

### Added
- **Iterative Refinement**: AI agent now critiques and refines its own output
- **Self-Critique System**: Automatic quality assessment and improvement
- **Smart File Prioritization**: Intelligent file ordering based on importance
- **Project Type Detection**: Auto-detect frontend, backend, or mixed projects
- **Multi-Format Output**: Support for Markdown, HTML, and PDF
- **Comprehensive Logging**: Detailed logging with file and console output
- **Retry Logic**: Exponential backoff for API failures
- **Configuration System**: Environment-based configuration via .env
- **Quality Thresholds**: Configurable acceptance criteria
- **Docker Support**: Containerized deployment option
- **PyInstaller Support**: Standalone executable builds
- **Organized Structure**: Clean project organization with src/, config/, docs/
- **Complete Documentation**: Comprehensive guides and API reference

### Changed
- **Breaking**: Restructured project layout (moved to src/ directory)
- **Breaking**: Updated configuration to use .env file
- Improved error handling and user feedback
- Enhanced documentation generation quality
- Better handling of large codebases
- Optimized file discovery algorithm

### Fixed
- Timeout issues with large projects
- Memory leaks in long-running sessions
- Unicode handling in documentation
- PDF generation on Windows
- API connection error messages

### Removed
- Direct hardcoded configuration (moved to .env)
- Deprecated single-pass generator as primary mode

---

## [1.5.0] - 2024-12-15

### Added
- HTML output format support
- PDF generation capability
- Basic project type detection
- Priority file identification
- Configurable file limits

### Changed
- Improved prompt engineering
- Better code extraction
- Enhanced error messages

### Fixed
- File encoding issues
- Empty documentation output
- API timeout handling

---

## [1.0.0] - 2024-11-01

### Added
- Initial release
- Basic documentation generation
- Ollama API integration
- Markdown output support
- Simple file discovery
- Command-line interface
- Basic configuration options

### Features
- Generate documentation from Python, JavaScript, TypeScript files
- Support for common web frameworks
- Automatic file discovery
- Simple command-line usage
- Configurable output location

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version: Incompatible API changes
- **MINOR** version: New features (backward compatible)
- **PATCH** version: Bug fixes (backward compatible)

### Example
- `2.0.0` → Major release with breaking changes
- `2.1.0` → New features added
- `2.1.1` → Bug fixes only

---

## Release Process

### 1. Pre-Release

- [ ] Update version in `setup.py`
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Test manual workflows
- [ ] Update documentation

### 2. Release

```bash
# Tag version
git tag -a v2.0.0 -m "Release version 2.0.0"

# Push tag
git push origin v2.0.0

# Create GitHub release
# - Go to GitHub Releases
# - Create new release from tag
# - Add release notes from CHANGELOG
```

### 3. Post-Release

- [ ] Announce on project channels
- [ ] Update documentation site
- [ ] Monitor for issues
- [ ] Plan next version

---

## Detailed Changes by Version

### [2.0.0] - Detailed Changes

#### New Files
- `src/ai_agent.py` - AI agent with iterative refinement
- `config/.env.example` - Configuration template
- `build/Dockerfile` - Docker containerization
- `build/docker-compose.yml` - Docker Compose setup
- `build/ai_agent.spec` - PyInstaller specification
- `docs/` - Complete documentation structure

#### Modified Files
- `src/doc_generator.py` - Enhanced with prioritization
- `run.py` - Updated launcher
- `setup.py` - New package configuration
- `README.md` - Comprehensive updates

#### Architecture Changes
```
Old Structure:          New Structure:
├── ai_agent.py        ├── src/
├── doc_generator.py   │   ├── ai_agent.py
├── requirements.txt   │   └── doc_generator.py
└── README.md          ├── config/
                       │   ├── requirements.txt
                       │   └── .env.example
                       ├── build/
                       ├── docs/
                       ├── tests/
                       └── run.py
```

#### API Changes
```python
# Old (v1.x)
generate_documentation(directory, output_format)

# New (v2.x)
agent = AIAgent(
    directory=directory,
    model=model,
    output_format=output_format,
    config=config
)
agent.run(max_iterations=3)
```

#### Configuration Changes
```bash
# Old (v1.x)
# Hardcoded in script

# New (v2.x)
# .env file
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=llama2:7b
API_TIMEOUT=300
```

---

## Migration Guide

### Upgrading from 1.x to 2.0

#### 1. Update Project Structure

```bash
# Backup old version
cp -r old-version old-version-backup

# Clone new version
git clone https://github.com/your-repo/ai-doc-agent.git
cd ai-doc-agent
```

#### 2. Update Configuration

```bash
# Create .env file
cp config/.env.example .env

# Transfer your old settings
# Old: MODEL = "llama2:7b"
# New: MODEL_NAME=llama2:7b in .env
```

#### 3. Update Scripts

```bash
# Old usage
python ai_agent.py /path/to/project

# New usage
python run.py --directory /path/to/project
```

#### 4. Update Imports (if using as library)

```python
# Old
from ai_agent import generate_documentation

# New
from src.ai_agent import AIAgent
from src.doc_generator import generate_documentation
```

---

## Breaking Changes Log

### v2.0.0

**Configuration:**
- Environment variables now required in `.env` file
- `MODEL` renamed to `MODEL_NAME`
- `OLLAMA_URL` renamed to `OLLAMA_API_URL`

**Project Structure:**
- Source files moved to `src/` directory
- Configuration moved to `config/` directory
- Import paths changed

**CLI:**
- New command-line argument names
- `--model` flag added for model override
- `--iterations` flag added for refinement control

**API:**
- `AIAgent` class signature changed
- Configuration now uses `AgentConfig` class
- Return values updated (exit codes)

---

## Deprecation Notices

### Deprecated in v2.0

- Direct script execution (use `run.py` instead)
- Hardcoded configuration (use `.env`)
- Single-pass mode as primary (use AI Agent)

### Removed in v2.0

- Old directory structure
- Direct configuration in scripts
- Legacy command-line arguments

---

## Security Updates

### v2.0.0
- Added `.env` to `.gitignore` to prevent secret leaks
- Improved input validation
- Sanitized file path handling
- Updated dependencies to latest versions

---

## Known Issues

### Current Issues

**v2.0.0:**
- PDF generation may fail on some Windows systems without wkhtmltopdf
- Very large projects (500+ files) may timeout
- Response caching not yet implemented
- Some antivirus software flags PyInstaller executables

**Workarounds:**
- Install wkhtmltopdf separately for PDF support
- Use `--max-files` to limit file count
- Disable caching (already disabled by default)
- Add executable to antivirus exceptions

---

## Contributing to Changelog

When contributing, please update CHANGELOG.md:

1. Add changes to **[Unreleased]** section
2. Use these categories:
   - **Added** - New features
   - **Changed** - Changes to existing features
   - **Deprecated** - Soon-to-be removed features
   - **Removed** - Removed features
   - **Fixed** - Bug fixes
   - **Security** - Security updates

3. Format:
   ```markdown
   ### Added
   - Feature description with context
   - Another feature
   ```

---

## Next Steps

- [Contributing Guide](contributing.md) - How to contribute
- [Testing Guide](testing.md) - Testing instructions
- [API Reference](../reference/api.md) - API documentation
- [User Guide](../guide/overview.md) - Usage guide

---

**Note:** This changelog is maintained manually. For detailed commit history, see [GitHub commits](https://github.com/deepak-sekarbabu/ai-doc-agent/commits/main).
