# API Reference

Complete API reference for the AI Documentation Agent v2.0.0 modules, classes, and functions with semantic analysis.

## Module Overview

The AI Documentation Agent consists of several key modules:

| Module | Purpose | Entry Point |
|--------|---------|-------------|
| `ai_agent` | Original iterative refinement agent with semantic analysis | `src/ai_agent.py` |
| `langgraph_agent` | LangGraph-based agent with semantic analysis | `src/langgraph_agent.py` |
| `doc_generator` | Core documentation utilities | `src/doc_generator.py` |
| `semantic_code_analyzer` | Code relationship and architecture analysis | `src/utils/semantic_code_analyzer.py` |
| `semantic_critique` | Documentation critique and validation | `src/utils/semantic_critique.py` |

## ai_agent Module

### AgentConfig

Configuration class for the AI Agent.

```python
from src.ai_agent import AgentConfig

config = AgentConfig()
```

#### Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_retries` | int | 3 | Maximum API retry attempts |
| `retry_delay` | int | 2 | Base delay between retries (seconds) |
| `critique_threshold` | float | 0.8 | Quality threshold (0.0-1.0) |
| `enable_caching` | bool | True | Enable response caching |

#### Example

```python
config = AgentConfig()
config.max_retries = 5
config.retry_delay = 3
config.critique_threshold = 0.9

print(config)
# Output: AgentConfig(max_retries=5, retry_delay=3, critique_threshold=0.9)
```

---

### AIAgent

Main AI agent class with iterative refinement capability.

```python
from src.ai_agent import AIAgent, AgentConfig

agent = AIAgent(
    directory="/path/to/project",
    max_files=30,
    model="llama2:7b",
    project_type="backend",
    output_format="markdown",
    output_file="docs",
    config=AgentConfig()
)

exit_code = agent.run(max_iterations=3)
```

#### Constructor Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `directory` | str | Yes | - | Project directory path |
| `max_files` | int | No | 30 | Maximum files to analyze |
| `model` | str | No | From env | Ollama model name |
| `project_type` | str | No | Auto | 'frontend', 'backend', 'mixed' |
| `output_format` | str | No | 'markdown' | Output format |
| `output_file` | str | No | Auto | Output filename (no ext) |
| `config` | AgentConfig | No | AgentConfig() | Agent configuration |

#### Methods

##### run(max_iterations: int = 3) → int

Run the agent with iterative refinement.

```python
exit_code = agent.run(max_iterations=5)
# Returns: 0 on success, non-zero on error
```

**Parameters:**
- `max_iterations` (int): Maximum refinement iterations (default: 3)

**Returns:**
- `int`: Exit code (0 = success, 1 = error)

**Process:**
1. Discovers and analyzes code files
2. Generates initial documentation
3. Critiques the documentation
4. Refines based on critique
5. Repeats until quality threshold or max iterations
6. Saves final documentation

##### Example Usage

```python
from src.ai_agent import AIAgent

# Basic usage
agent = AIAgent(
    directory="./my-project",
    max_files=50,
    model="codellama"
)
agent.run(max_iterations=5)

# Advanced usage
from src.ai_agent import AgentConfig

config = AgentConfig()
config.max_retries = 5
config.critique_threshold = 0.9

agent = AIAgent(
    directory="/home/user/important-project",
    max_files=100,
    model="codellama",
    project_type="backend",
    output_format="pdf",
    output_file="comprehensive_docs",
    config=config
)

result = agent.run(max_iterations=7)
if result == 0:
print("Documentation generated successfully!")
```

---

## semantic_code_analyzer Module

Advanced analyzer for understanding code relationships and dependencies.

### SemanticCodeAnalyzer

```python
from src.utils.semantic_code_analyzer import SemanticCodeAnalyzer

analyzer = SemanticCodeAnalyzer(file_contents)
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_coupling_analysis()` | `Dict[str, float]` | Returns coupling metrics for files |
| `get_central_elements(top_n)` | `List[Tuple[str, float]]` | Returns most central code elements |
| `detect_architecture_patterns()` | `List[ArchitecturePattern]` | Detects architectural patterns |

#### Example

```python
from src.utils.semantic_code_analyzer import SemanticCodeAnalyzer

# Analyze codebase
analyzer = SemanticCodeAnalyzer(file_contents)

# Get coupling analysis
coupling = analyzer.get_coupling_analysis()
print(f"Coupling analysis: {coupling}")

# Get central elements
central = analyzer.get_central_elements(top_n=5)
for element, score in central:
    print(f"{element}: {score}")

# Detect patterns
patterns = analyzer.detect_architecture_patterns()
for pattern in patterns:
    print(f"Pattern: {pattern.pattern_type} - {pattern.description}")
```

---

## semantic_critique Module

AI-powered documentation critique and validation.

### SemanticCritiqueAnalyzer

```python
from src.utils.semantic_critique import SemanticCritiqueAnalyzer

analyzer = SemanticCritiqueAnalyzer()
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `analyze_critique_semantically(text)` | `SemanticScore` | Analyzes critique quality |

### DocumentationValidator

```python
from src.utils.semantic_critique import DocumentationValidator

validator = DocumentationValidator(file_contents)
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `validate_documentation(docs)` | `List[ValidationIssue]` | Validates documentation against code |

---

## langgraph_agent Module

LangGraph-based agent implementation with semantic analysis workflow.

### AgentState

Typed dictionary defining the state passed between LangGraph nodes.

```python
from src.langgraph_agent import AgentState

state: AgentState = {
    "directory": Path("./project"),
    "max_files": 100,
    "model": "codellama",
    "file_contents": [...],
    "documentation": None,
    "semantic_analyzer": None,
    "semantic_analysis": None,
    # ... other fields
}
```

### Workflow Nodes

| Node Function | Purpose |
|---------------|---------|
| `analyze_codebase` | Discovers and reads code files |
| `perform_semantic_analysis` | Analyzes code relationships and architecture |
| `generate_draft` | Creates initial documentation with semantic insights |
| `critique_document` | AI-powered critique of documentation |
| `refine_document` | Improves documentation based on critique |

### Example Usage

```python
from src.langgraph_agent import build_graph

# Create and run the graph
app = build_graph()
result = app.invoke(initial_state)
print(f"Documentation: {result['documentation']}")
```

---

## doc_generator Module

Core utilities for file discovery, processing, and documentation generation.

### Constants

#### File Extensions

```python
from src.doc_generator import SUPPORTED_EXTENSIONS

# Frozenset of supported file extensions
SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".go", 
    ".php", ".rb", ".rs", ".c", ".cpp", ".h", ".hpp", ".html", 
    ".css", ".scss", ".sql", ".sh", ".kt", ".swift", ".vue", 
    ".svelte", ".xml", ".gradle"
}
```

#### Ignored Directories

```python
from src.doc_generator import IGNORED_DIRECTORIES

# Frozenset of directories to skip
IGNORED_DIRECTORIES = {
    "node_modules", ".git", ".vscode", ".idea", "__pycache__",
    "dist", "build", "target", "out", "bin", "obj", "vendor",
    "tmp", "temp", ".next", "docs", "coverage", ".pytest_cache"
}
```

#### Priority Files

```python
from src.doc_generator import PRIORITY_FILES

# Dictionary of priority files by project type
PRIORITY_FILES = {
    "frontend": {
        "package.json", "index.html", "App.tsx", "App.jsx",
        "main.tsx", "vite.config.ts", "tailwind.config.ts"
    },
    "backend": {
        "pom.xml", "build.gradle", "requirements.txt", "go.mod",
        "Cargo.toml", "Program.cs", "setup.py"
    }
}
```

---

### Functions

#### detect_project_type()

Auto-detect project type based on configuration files.

```python
from src.doc_generator import detect_project_type

project_type = detect_project_type("/path/to/project")
# Returns: "frontend", "backend", or "mixed"
```

**Parameters:**
- `start_path` (str): Root directory to analyze

**Returns:**
- `str`: Project type ("frontend", "backend", or "mixed")

**Example:**

```python
# Frontend project (has package.json)
type1 = detect_project_type("./react-app")
print(type1)  # "frontend"

# Backend project (has requirements.txt)
type2 = detect_project_type("./flask-api")
print(type2)  # "backend"

# Mixed project (has both)
type3 = detect_project_type("./fullstack-app")
print(type3)  # "mixed"
```

---

#### find_code_files()

Find and prioritize code files in a directory.

```python
from src.doc_generator import find_code_files

files = find_code_files(
    start_path="/path/to/project",
    max_files=30,
    project_type="backend"
)
# Returns: List of file paths
```

**Parameters:**
- `start_path` (str): Root directory to search
- `max_files` (int, optional): Maximum files to return (default: 50)
- `project_type` (str, optional): Project type or None for auto-detect

**Returns:**
- `List[str]`: List of file paths, priority files first

**Example:**

```python
# Auto-detect and find files
files = find_code_files("./my-project", max_files=30)

# Explicit project type
files = find_code_files(
    "./my-api",
    max_files=50,
    project_type="backend"
)

# Iterate over files
for file_path in files:
    print(f"Found: {file_path}")
```

---

#### read_file_safe()

Safely read file contents with error handling.

```python
from src.doc_generator import read_file_safe

content = read_file_safe("/path/to/file.py")
# Returns: File content or empty string on error
```

**Parameters:**
- `file_path` (str): Path to file

**Returns:**
- `str`: File content or empty string if error

**Example:**

```python
content = read_file_safe("app/main.py")
if content:
    print(f"Read {len(content)} characters")
else:
    print("Failed to read file")
```

---

#### build_prompt()

Build a prompt for the LLM from file contents.

```python
from src.doc_generator import build_prompt

file_contents = [
    {"path": "main.py", "content": "# Main file..."},
    {"path": "utils.py", "content": "# Utilities..."}
]

prompt = build_prompt(
    file_contents,
    project_type="backend",
    output_format="markdown"
)
```

**Parameters:**
- `file_contents` (List[Dict]): List of file dictionaries
- `project_type` (str, optional): Project type
- `output_format` (str, optional): Output format

**Returns:**
- `str`: Formatted prompt for LLM

---

#### generate_documentation()

Generate documentation using Ollama API.

```python
from src.doc_generator import generate_documentation

file_contents = [
    {"path": "app.py", "content": "# Flask app..."},
    {"path": "models.py", "content": "# Database models..."}
]

docs = generate_documentation(
    file_contents,
    output_format="markdown",
    project_type="backend"
)
```

**Parameters:**
- `file_contents` (List[Dict]): List of file dictionaries
- `output_format` (str, optional): Output format (default: "markdown")
- `project_type` (str, optional): Project type

**Returns:**
- `str`: Generated documentation

**Raises:**
- `OllamaConnectionError`: If cannot connect to Ollama API
- `DocGeneratorError`: For other generation errors

**Example:**

```python
from src.doc_generator import (
    find_code_files,
    read_file_safe,
    generate_documentation
)

# Find files
files = find_code_files("./my-project", max_files=30)

# Read contents
file_contents = []
for file_path in files:
    content = read_file_safe(file_path)
    file_contents.append({
        "path": file_path,
        "content": content
    })

# Generate documentation
try:
    docs = generate_documentation(
        file_contents,
        output_format="html",
        project_type="frontend"
    )
    print("Documentation generated successfully!")
except Exception as e:
    print(f"Error: {e}")
```

---

#### save_documentation()

Save documentation to file in specified format.

```python
from src.doc_generator import save_documentation

output_path = save_documentation(
    content="# My Documentation\n...",
    output_format="markdown",
    output_file="my_docs"
)
# Returns: "output/my_docs.md"
```

**Parameters:**
- `content` (str): Documentation content
- `output_format` (str): Format ("markdown", "html", "pdf")
- `output_file` (str): Output filename without extension

**Returns:**
- `str`: Full path to saved file

**Example:**

```python
# Save as Markdown
path1 = save_documentation(docs, "markdown", "api_docs")
# Creates: output/api_docs.md

# Save as HTML
path2 = save_documentation(docs, "html", "api_docs")
# Creates: output/api_docs.html

# Save as PDF
path3 = save_documentation(docs, "pdf", "api_docs")
# Creates: output/api_docs.pdf
```

---

#### get_ollama_headers()

Get HTTP headers for Ollama API requests.

```python
from src.doc_generator import get_ollama_headers

headers = get_ollama_headers()
# Returns: {"Content-Type": "application/json", ...}
```

**Returns:**
- `Dict[str, str]`: HTTP headers dictionary

---

### Exceptions

#### DocGeneratorError

Base exception for documentation generator errors.

```python
from src.doc_generator import DocGeneratorError

try:
    # Some operation
    pass
except DocGeneratorError as e:
    print(f"Generator error: {e}")
```

#### OllamaConnectionError

Raised when unable to connect to Ollama API.

```python
from src.doc_generator import OllamaConnectionError

try:
    docs = generate_documentation(file_contents)
except OllamaConnectionError as e:
    print(f"Cannot connect to Ollama: {e}")
```

---

## Environment Variables

Both modules respect these environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `OLLAMA_API_URL` | str | `https://ollama.com/api/generate` | Ollama API endpoint |
| `MODEL_NAME` | str | `gpt-oss:120b-cloud` | LLM model name |
| `API_TIMEOUT` | int | `300` | API timeout (seconds) |
| `MAX_RETRIES` | int | `3` | Maximum retry attempts |
| `RETRY_DELAY` | int | `2` | Base retry delay (seconds) |
| `CRITIQUE_THRESHOLD` | float | `0.8` | Quality threshold (0.0-1.0) |
| `ENABLE_CACHING` | bool | `true` | Enable caching |

---

## Complete Example

### End-to-End Documentation Generation

```python
#!/usr/bin/env python3
from src.ai_agent import AIAgent, AgentConfig
from src.doc_generator import (
    detect_project_type,
    find_code_files,
    generate_documentation,
    save_documentation
)

# Method 1: Using AI Agent (Recommended)
def generate_with_agent():
    config = AgentConfig()
    config.max_retries = 5
    config.critique_threshold = 0.9
    
    agent = AIAgent(
        directory="./my-project",
        max_files=50,
        model="codellama",
        project_type="backend",
        output_format="html",
        output_file="comprehensive_docs",
        config=config
    )
    
    return agent.run(max_iterations=5)

# Method 2: Using doc_generator directly
def generate_simple():
    # Detect project type
    project_type = detect_project_type("./my-project")
    print(f"Detected: {project_type}")
    
    # Find files
    files = find_code_files(
        "./my-project",
        max_files=30,
        project_type=project_type
    )
    print(f"Found {len(files)} files")
    
    # Read contents
    from src.doc_generator import read_file_safe
    file_contents = [
        {"path": f, "content": read_file_safe(f)}
        for f in files
    ]
    
    # Generate docs
    docs = generate_documentation(
        file_contents,
        output_format="markdown",
        project_type=project_type
    )
    
    # Save
    output_path = save_documentation(
        docs,
        "markdown",
        "my_docs"
    )
    print(f"Saved to: {output_path}")

# Run
if __name__ == "__main__":
    # Use AI Agent for best quality
    result = generate_with_agent()
    
    # Or use simple generator for speed
    # generate_simple()
```

---

## Next Steps

- [Configuration Reference](config.md) - Environment variables
- [Project Structure](structure.md) - Code organization
- [User Guide](../guide/overview.md) - Usage guide
- [Command Reference](../guide/commands.md) - CLI commands
