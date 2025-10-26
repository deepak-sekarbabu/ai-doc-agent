# Tests

Unit tests for AI Documentation Agent.

## Test Coverage

### test_doc_generator.py
- [x] Test project type detection (frontend/backend/mixed)
- [x] Test file discovery and prioritization
- [x] Test reading files safely
- [x] Test docstring extraction (Python)
- [x] Test JSDoc extraction (JavaScript/TypeScript)
- [x] Test prompt building
- [x] Test documentation saving

### test_ai_agent.py
- [x] Test agent configuration
- [x] Test agent initialization
- [x] Test input validation
- [x] Test codebase analysis
- [x] Test documentation generation
- [x] Test critique detection
- [x] Test Ollama API calls with retry logic
- [x] Test prompt building for critique and refinement

## Running Tests

### Install Test Dependencies
```bash
pip install -e .[dev]
```

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_doc_generator.py
pytest tests/test_ai_agent.py
```

### Run with Coverage
```bash
pytest --cov=src --cov-report=html
```

### Run Specific Test
```bash
pytest tests/test_doc_generator.py::TestDocGenerator::test_detect_project_type_frontend -v
```

## Test Structure

- **Unit Tests**: Test individual functions and methods in isolation
- **Mocking**: External dependencies (API calls, file system) are mocked
- **Fixtures**: Test data is set up cleanly for each test
- **Assertions**: Clear and specific assertions for expected behavior

## Adding New Tests

1. Create test methods in existing test classes or new test files
2. Use descriptive test method names: `test_<functionality>_<scenario>`
3. Mock external dependencies appropriately
4. Include docstrings for complex test logic
5. Run tests frequently during development
