# Contributing

Thank you for your interest in contributing to the AI Documentation Agent! This guide will help you get started.

## Ways to Contribute

There are many ways to contribute to this project:

- 🐛 **Report bugs** - Help us identify and fix issues
- 💡 **Suggest features** - Share your ideas for improvements
- 📝 **Improve documentation** - Help make docs clearer and more comprehensive
- 🔧 **Submit pull requests** - Contribute code improvements
- ⭐ **Star the project** - Show your support on GitHub
- 🗣️ **Share feedback** - Let us know how you use the tool

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.8 or higher
- Git installed
- Ollama installed and running
- Basic understanding of Python
- Familiarity with the project (read the documentation)

### Development Setup

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork

git clone https://github.com/YOUR-USERNAME/ai-doc-agent.git
cd ai-doc-agent
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
# Install all dependencies including dev tools
pip install -r config/requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

#### 4. Configure Environment

```bash
# Copy environment template
cp config/.env.example .env

# Edit .env with your settings
# Set OLLAMA_API_URL and MODEL_NAME
```

#### 5. Verify Setup

```bash
# Test the agent
python run.py --help

# Run with example project
python run.py --directory ./examples --max-files 5
```

## Development Workflow

### Branch Strategy

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description

# Or for documentation
git checkout -b docs/doc-improvement
```

**Branch Naming:**
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation changes
- `refactor/*` - Code refactoring
- `test/*` - Test additions/changes

### Making Changes

#### 1. Write Code

Follow the project's coding standards:

```python
# Good example
def generate_documentation(
    file_contents: List[Dict[str, str]],
    output_format: str = "markdown"
) -> str:
    """
    Generate documentation from file contents.
    
    Args:
        file_contents: List of file dictionaries
        output_format: Output format (markdown/html/pdf)
    
    Returns:
        Generated documentation string
    
    Raises:
        DocGeneratorError: If generation fails
    """
    # Implementation
    pass
```

#### 2. Format Code

```bash
# Format with black
black src/

# Check style with flake8
flake8 src/

# Type check with mypy
mypy src/
```

#### 3. Write Tests

```bash
# Create test file in tests/ directory
# tests/test_your_feature.py

import pytest
from src.doc_generator import your_function

def test_your_function():
    """Test your function works correctly."""
    result = your_function(input_data)
    assert result == expected_output

def test_error_handling():
    """Test error handling."""
    with pytest.raises(ValueError):
        your_function(invalid_data)
```

#### 4. Run Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_doc_generator.py

# Run with coverage
pytest --cov=src tests/
```

#### 5. Update Documentation

```bash
# Update relevant documentation files
# - README.md (if feature is user-facing)
# - docs/guide.md (user guide updates)
# - API documentation (for new functions)
# - CHANGELOG.md (describe your changes)
```

### Commit Guidelines

Write clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "Add support for TypeScript files"
git commit -m "Fix timeout issue with large projects"
git commit -m "Update documentation for Docker deployment"

# Format
<type>: <short description>

[optional longer description]

[optional footer]
```

**Commit Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Build/config changes

**Examples:**

```bash
# Feature
git commit -m "feat: add support for Go projects"

# Bug fix
git commit -m "fix: handle missing .env file gracefully"

# Documentation
git commit -m "docs: add Docker deployment guide"

# With description
git commit -m "feat: implement caching for API responses

Add LRU cache to reduce API calls for repeated runs.
Configurable via ENABLE_CACHING environment variable.

Closes #42"
```

### Pull Request Process

#### 1. Update Your Fork

```bash
# Add upstream remote (one time)
git remote add upstream https://github.com/deepak-sekarbabu/ai-doc-agent.git

# Fetch latest changes
git fetch upstream

# Merge into your branch
git merge upstream/main
```

#### 2. Push Your Branch

```bash
# Push to your fork
git push origin feature/your-feature-name
```

#### 3. Create Pull Request

1. Go to GitHub repository
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Changes Made
- Added X feature
- Fixed Y issue
- Updated Z documentation

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] Updated documentation

## Screenshots (if applicable)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests pass
```

#### 4. Code Review

- Respond to feedback promptly
- Make requested changes
- Push updates to same branch
- Be open to suggestions

#### 5. Merge

Once approved, maintainers will merge your PR.

## Coding Standards

### Python Style Guide

Follow PEP 8 with these specifics:

**Line Length:**
```python
# Maximum 100 characters per line
# Break long lines logically
result = function_with_many_parameters(
    parameter1=value1,
    parameter2=value2,
    parameter3=value3
)
```

**Imports:**
```python
# Group imports
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third-party
import requests
from dotenv import load_dotenv

# 3. Local
from doc_generator import generate_documentation
```

**Type Hints:**
```python
# Use type hints
def process_files(
    files: List[str],
    max_count: int = 30
) -> Dict[str, Any]:
    """Process files and return results."""
    pass
```

**Docstrings:**
```python
def my_function(param1: str, param2: int) -> bool:
    """
    Short description of function.
    
    Longer description if needed, explaining what the
    function does and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When input is invalid
        RuntimeError: When operation fails
    
    Example:
        >>> result = my_function("test", 42)
        >>> print(result)
        True
    """
    pass
```

**Error Handling:**
```python
# Use specific exceptions
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise RuntimeError("Operation failed") from e
```

### Code Organization

**File Structure:**
```python
#!/usr/bin/env python3
"""
Module description.

Detailed explanation of what this module does.
"""

# Imports
import os
import sys

# Constants
MAX_FILES = 30
TIMEOUT = 300

# Classes
class MyClass:
    """Class docstring."""
    pass

# Functions
def my_function():
    """Function docstring."""
    pass

# Main execution
if __name__ == "__main__":
    main()
```

## Testing Guidelines

### Writing Tests

```python
# tests/test_feature.py
import pytest
from src.doc_generator import detect_project_type

class TestProjectDetection:
    """Tests for project type detection."""
    
    def test_frontend_detection(self, tmp_path):
        """Test detection of frontend projects."""
        # Setup
        (tmp_path / "package.json").touch()
        
        # Execute
        result = detect_project_type(str(tmp_path))
        
        # Assert
        assert result == "frontend"
    
    def test_backend_detection(self, tmp_path):
        """Test detection of backend projects."""
        (tmp_path / "requirements.txt").touch()
        result = detect_project_type(str(tmp_path))
        assert result == "backend"
    
    @pytest.mark.parametrize("file,expected", [
        ("package.json", "frontend"),
        ("requirements.txt", "backend"),
    ])
    def test_various_markers(self, tmp_path, file, expected):
        """Test detection with various marker files."""
        (tmp_path / file).touch()
        result = detect_project_type(str(tmp_path))
        assert result == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_doc_generator.py::test_detect_project_type

# Run with coverage
pytest --cov=src --cov-report=html tests/

# Run only fast tests
pytest -m "not slow"
```

## Documentation Guidelines

### Writing Documentation

**Be Clear and Concise:**
```markdown
# Good
Generate HTML documentation for your project.

# Avoid
This feature allows you to generate documentation in 
the HTML format which is really useful when you want 
to share it with others...
```

**Include Examples:**
```markdown
# Good
Generate docs with custom model:
\`\`\`bash
python run.py --model codellama
\`\`\`

# Avoid
You can use different models.
```

**Use Consistent Formatting:**
- Code blocks with language tags
- Commands in code blocks
- Variables in backticks: `VARIABLE_NAME`
- Emphasis with **bold** or *italic*

### Documentation Structure

```markdown
# Feature Title

Brief introduction (1-2 sentences).

## Overview

Detailed explanation of the feature.

## Usage

### Basic Usage
[Basic example]

### Advanced Usage
[Advanced example]

## Options

| Option | Description | Default |
|--------|-------------|---------|
| ... | ... | ... |

## Examples

### Example 1: [Description]
[Code and explanation]

### Example 2: [Description]
[Code and explanation]

## Troubleshooting

### Issue: [Problem]
**Solution:** [Fix]

## Next Steps

- [Related docs]
```

## Issue Reporting

### Bug Reports

Use this template:

```markdown
**Describe the bug**
Clear description of the bug.

**To Reproduce**
1. Run command '...'
2. See error '...'

**Expected behavior**
What should happen.

**Actual behavior**
What actually happens.

**Environment**
- OS: [e.g., Windows 10]
- Python: [e.g., 3.11]
- Ollama: [e.g., 0.1.14]
- Model: [e.g., llama2:7b]

**Error logs**
\`\`\`
[Paste error messages]
\`\`\`

**Additional context**
Any other relevant information.
```

### Feature Requests

```markdown
**Is your feature request related to a problem?**
Description of the problem.

**Describe the solution you'd like**
Clear description of desired feature.

**Describe alternatives considered**
Other approaches you've thought about.

**Additional context**
Mockups, examples, or other details.
```

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project
- Show empathy towards others

### Communication

- **GitHub Issues** - Bug reports and feature requests
- **Pull Requests** - Code contributions
- **Discussions** - Questions and general discussion

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Project documentation

## Getting Help

Need help contributing?

- 📖 Read the [documentation](../guide.md)
- 🐛 Check [existing issues](https://github.com/deepak-sekarbabu/ai-doc-agent/issues)
- 💬 Start a [discussion](https://github.com/deepak-sekarbabu/ai-doc-agent/discussions)
- 📧 Contact maintainers

## Next Steps

- [Testing Guide](testing.md) - Learn about testing
- [Project Structure](../reference/structure.md) - Understand the codebase
- [API Reference](../reference/api.md) - API documentation
- [Changelog](changelog.md) - Version history

---

**Thank you for contributing!** 🎉
