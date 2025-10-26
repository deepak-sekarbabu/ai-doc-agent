# Testing

Comprehensive guide to testing the AI Documentation Agent.

## Overview

Testing ensures the AI Documentation Agent works correctly and reliably. This guide covers unit testing, integration testing, and manual testing approaches.

## Test Framework

The project uses **pytest** as the testing framework.

### Why pytest?

- ✅ Simple and intuitive syntax
- ✅ Powerful fixtures
- ✅ Excellent test discovery
- ✅ Rich plugin ecosystem
- ✅ Detailed failure reports

## Setup

### Install Testing Dependencies

```bash
# Install pytest and related tools
pip install pytest pytest-cov pytest-mock

# Or install from requirements
pip install -r config/requirements.txt
```

### Verify Installation

```bash
# Check pytest version
pytest --version

# Run help
pytest --help
```

## Test Structure

### Directory Organization

```
tests/
├── __init__.py
├── test_doc_generator.py      # Core functionality tests
├── test_ai_agent.py            # AI agent tests
├── test_integration.py         # Integration tests
├── test_cli.py                 # Command-line tests
├── fixtures/                   # Test fixtures
│   ├── sample_project/         # Sample project structure
│   ├── expected_outputs/       # Expected results
│   └── test_files/             # Test file samples
└── conftest.py                 # Shared fixtures
```

## Writing Tests

### Basic Test Structure

```python
# tests/test_doc_generator.py
import pytest
from src.doc_generator import detect_project_type, find_code_files

def test_detect_frontend_project(tmp_path):
    """Test detection of frontend projects."""
    # Arrange
    (tmp_path / "package.json").touch()
    
    # Act
    result = detect_project_type(str(tmp_path))
    
    # Assert
    assert result == "frontend"

def test_detect_backend_project(tmp_path):
    """Test detection of backend projects."""
    # Arrange
    (tmp_path / "requirements.txt").touch()
    
    # Act
    result = detect_project_type(str(tmp_path))
    
    # Assert
    assert result == "backend"
```

### Using Fixtures

```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_frontend_project(tmp_path):
    """Create a sample frontend project structure."""
    project_dir = tmp_path / "frontend-app"
    project_dir.mkdir()
    
    # Create files
    (project_dir / "package.json").write_text('{"name": "test"}')
    (project_dir / "index.html").write_text("<html></html>")
    
    src_dir = project_dir / "src"
    src_dir.mkdir()
    (src_dir / "App.tsx").write_text("export const App = () => {}")
    
    return project_dir

@pytest.fixture
def sample_backend_project(tmp_path):
    """Create a sample backend project structure."""
    project_dir = tmp_path / "backend-app"
    project_dir.mkdir()
    
    (project_dir / "requirements.txt").write_text("flask==2.0.0")
    (project_dir / "app.py").write_text("from flask import Flask")
    
    return project_dir

# Use in tests
def test_with_frontend_fixture(sample_frontend_project):
    """Test using frontend fixture."""
    result = detect_project_type(str(sample_frontend_project))
    assert result == "frontend"
```

### Parametrized Tests

```python
@pytest.mark.parametrize("marker_file,expected_type", [
    ("package.json", "frontend"),
    ("yarn.lock", "frontend"),
    ("requirements.txt", "backend"),
    ("pom.xml", "backend"),
    ("go.mod", "backend"),
])
def test_project_detection_markers(tmp_path, marker_file, expected_type):
    """Test project detection with various marker files."""
    (tmp_path / marker_file).touch()
    result = detect_project_type(str(tmp_path))
    assert result == expected_type
```

### Testing Exceptions

```python
def test_invalid_directory():
    """Test handling of invalid directory."""
    with pytest.raises(ValueError, match="Invalid directory"):
        find_code_files("/nonexistent/path")

def test_api_connection_error(mocker):
    """Test handling of API connection errors."""
    # Mock requests to raise exception
    mocker.patch('requests.post', side_effect=ConnectionError())
    
    with pytest.raises(OllamaConnectionError):
        generate_documentation(file_contents)
```

### Mocking

```python
def test_ollama_api_call(mocker):
    """Test Ollama API call with mocking."""
    # Mock the API response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '{"response": "Generated docs"}\n'
    
    mocker.patch('requests.post', return_value=mock_response)
    
    # Run function
    result = generate_documentation(file_contents)
    
    # Verify
    assert "Generated docs" in result
    requests.post.assert_called_once()
```

## Test Categories

### Unit Tests

Test individual functions in isolation.

```python
# tests/test_doc_generator.py

def test_read_file_safe_success(tmp_path):
    """Test successful file reading."""
    test_file = tmp_path / "test.py"
    content = "print('hello')"
    test_file.write_text(content)
    
    result = read_file_safe(str(test_file))
    assert result == content

def test_read_file_safe_error():
    """Test file reading error handling."""
    result = read_file_safe("/nonexistent/file.py")
    assert result == ""

def test_find_code_files_max_limit(sample_frontend_project):
    """Test max_files limit is respected."""
    files = find_code_files(
        str(sample_frontend_project),
        max_files=2
    )
    assert len(files) <= 2

def test_priority_files_first(sample_frontend_project):
    """Test that priority files come first."""
    files = find_code_files(str(sample_frontend_project))
    
    # package.json should be first
    assert "package.json" in files[0]
```

### Integration Tests

Test multiple components working together.

```python
# tests/test_integration.py

def test_full_documentation_generation(sample_frontend_project):
    """Test complete documentation generation flow."""
    # Find files
    files = find_code_files(str(sample_frontend_project))
    assert len(files) > 0
    
    # Read contents
    file_contents = []
    for file_path in files:
        content = read_file_safe(file_path)
        file_contents.append({
            "path": file_path,
            "content": content
        })
    
    # Generate documentation (mocked)
    # In real test, would mock API call
    assert len(file_contents) > 0

def test_agent_workflow(sample_backend_project, mocker):
    """Test AI agent complete workflow."""
    # Mock API calls
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = '{"response": "Documentation"}\n'
    mocker.patch('requests.post', return_value=mock_response)
    
    # Create agent
    from src.ai_agent import AIAgent
    agent = AIAgent(
        directory=str(sample_backend_project),
        max_files=10,
        model="test-model",
        project_type="backend",
        output_format="markdown",
        output_file="test_output"
    )
    
    # Run (will be mocked)
    # result = agent.run(max_iterations=1)
    # assert result == 0
```

### CLI Tests

Test command-line interface.

```python
# tests/test_cli.py
import subprocess

def test_help_command():
    """Test --help flag."""
    result = subprocess.run(
        ["python", "run.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()

def test_version_display():
    """Test version information."""
    result = subprocess.run(
        ["python", "run.py", "--help"],
        capture_output=True,
        text=True
    )
    assert "AI Documentation Agent" in result.stdout
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_doc_generator.py

# Run specific test
pytest tests/test_doc_generator.py::test_detect_frontend_project

# Run tests matching pattern
pytest -k "detection"
```

### Test Coverage

```bash
# Run with coverage report
pytest --cov=src tests/

# Generate HTML coverage report
pytest --cov=src --cov-report=html tests/

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Markers

```python
# Mark slow tests
@pytest.mark.slow
def test_large_project():
    """Test with large project (slow)."""
    pass

# Mark tests requiring network
@pytest.mark.network
def test_api_integration():
    """Test real API integration."""
    pass
```

```bash
# Run only fast tests
pytest -m "not slow"

# Run only network tests
pytest -m network

# Skip network tests
pytest -m "not network"
```

### Continuous Testing

```bash
# Watch mode (requires pytest-watch)
pip install pytest-watch
ptw

# Run on file change
pytest --looponfail
```

## Test Best Practices

### 1. Test Naming

```python
# Good names - descriptive
def test_detect_frontend_project_with_package_json():
    pass

def test_raises_error_when_directory_not_found():
    pass

# Avoid - unclear
def test_1():
    pass

def test_stuff():
    pass
```

### 2. Arrange-Act-Assert Pattern

```python
def test_file_prioritization():
    # Arrange - setup
    project_dir = create_test_project()
    
    # Act - execute
    files = find_code_files(project_dir)
    
    # Assert - verify
    assert "package.json" in files[0]
```

### 3. One Assertion Per Test

```python
# Good - focused test
def test_returns_frontend_type():
    result = detect_project_type(frontend_project)
    assert result == "frontend"

def test_returns_backend_type():
    result = detect_project_type(backend_project)
    assert result == "backend"

# Avoid - too many assertions
def test_project_detection():
    assert detect_project_type(frontend_project) == "frontend"
    assert detect_project_type(backend_project) == "backend"
    assert detect_project_type(mixed_project) == "mixed"
```

### 4. Use Fixtures for Setup

```python
# Good - reusable fixture
@pytest.fixture
def sample_project():
    return create_project_structure()

def test_something(sample_project):
    result = process(sample_project)
    assert result is not None

# Avoid - repeated setup
def test_something():
    project = create_project_structure()
    result = process(project)
    assert result is not None
```

### 5. Mock External Dependencies

```python
# Good - mock API calls
def test_documentation_generation(mocker):
    mocker.patch('requests.post', return_value=mock_response)
    result = generate_documentation(files)
    assert result is not None

# Avoid - real API calls in tests
def test_documentation_generation():
    result = generate_documentation(files)  # Makes real API call
    assert result is not None
```

## Manual Testing

### Test Checklist

Before releasing, manually test:

**Basic Functionality:**
- [ ] `python run.py --help` displays help
- [ ] Generate docs for sample project
- [ ] All output formats work (markdown, html, pdf)
- [ ] Configuration loads from .env

**Different Project Types:**
- [ ] Frontend project (React/Vue)
- [ ] Backend project (Python/Java)
- [ ] Mixed project (Full-stack)

**Edge Cases:**
- [ ] Empty directory
- [ ] Very large project (100+ files)
- [ ] Project with no supported files
- [ ] Invalid .env configuration

**Error Handling:**
- [ ] Ollama not running
- [ ] Invalid directory path
- [ ] Network timeout
- [ ] Insufficient permissions

### Test Commands

```bash
# Test with examples
python run.py --directory ./examples --max-files 10

# Test different formats
python run.py --directory ./examples --format markdown
python run.py --directory ./examples --format html
python run.py --directory ./examples --format pdf

# Test iterations
python run.py --directory ./examples --iterations 2
python run.py --directory ./examples --iterations 5

# Test with different models
python run.py --directory ./examples --model llama2:7b
python run.py --directory ./examples --model codellama

# Test verbose mode
python run.py --directory ./examples --verbose

# Test error conditions
python run.py --directory /nonexistent
python run.py --model nonexistent-model
```

## CI/CD Testing

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -r config/requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest --cov=src tests/
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Performance Testing

### Benchmarking

```python
# tests/test_performance.py
import time

def test_file_discovery_performance(large_project):
    """Test file discovery performance."""
    start = time.time()
    files = find_code_files(large_project, max_files=100)
    duration = time.time() - start
    
    assert len(files) > 0
    assert duration < 5.0  # Should complete in < 5 seconds

@pytest.mark.slow
def test_full_generation_performance(sample_project, mocker):
    """Test full documentation generation performance."""
    # Mock API to avoid network delay
    mocker.patch('requests.post', return_value=mock_response)
    
    start = time.time()
    # Run full generation
    duration = time.time() - start
    
    assert duration < 30.0  # Should complete in < 30 seconds
```

## Troubleshooting Tests

### Tests Failing

**Check test isolation:**
```bash
# Run tests in random order
pytest --random-order
```

**Check for side effects:**
```bash
# Run single test
pytest tests/test_file.py::test_name -v
```

### Slow Tests

```bash
# Find slowest tests
pytest --durations=10

# Profile tests
pytest --profile
```

### Coverage Issues

```bash
# See which lines aren't covered
pytest --cov=src --cov-report=term-missing tests/
```

## Next Steps

- [Contributing Guide](contributing.md) - How to contribute
- [API Reference](../reference/api.md) - API documentation
- [Changelog](changelog.md) - Version history
- [Examples](../examples/samples.md) - Sample projects
