# Simple Generator Guide

Quick, single-pass documentation generation without iterative refinement.

## Overview

The Simple Generator (`src/doc_generator.py`) provides fast, straightforward documentation generation. Unlike the AI Agent, it generates documentation in a single pass without critique or refinement.

## When to Use

### Use Simple Generator For:

- ✅ **Quick documentation needs** - Fast turnaround
- ✅ **Simple projects** - Small codebases
- ✅ **Initial drafts** - Starting point for manual editing
- ✅ **Testing** - Validate setup and configuration
- ✅ **Time-constrained** - Immediate documentation needed

### Use AI Agent Instead For:

- ⚠️ **Production documentation** - Needs high quality
- ⚠️ **Complex projects** - Requires deep analysis
- ⚠️ **Comprehensive docs** - Detailed coverage needed
- ⚠️ **Quality-critical** - Documentation accuracy matters

## Key Differences

| Feature | Simple Generator | AI Agent |
|---------|-----------------|----------|
| **Speed** | ⚡⚡⚡ Very Fast | ⚡ Slower |
| **Quality** | ⭐⭐ Basic | ⭐⭐⭐⭐⭐ Excellent |
| **Iterations** | 1 (single pass) | 1-5 (configurable) |
| **Refinement** | ❌ None | ✅ Iterative |
| **Self-Critique** | ❌ None | ✅ Yes |
| **API Calls** | 1-2 | 3-15 |
| **Best For** | Quick docs | Production docs |

## Usage

### Direct Script Usage

```bash
# Basic usage
python src/doc_generator.py ./my-project

# Specify output format
python src/doc_generator.py ./my-project --format html

# Custom output filename
python src/doc_generator.py ./my-project --output quick_docs
```

### As Python Module

```python
from src.doc_generator import generate_documentation, find_code_files

# Find files
files = find_code_files("./my-project", max_files=30)

# Generate documentation
docs = generate_documentation(files, output_format="markdown")

# Save
with open("output.md", "w") as f:
    f.write(docs)
```

### Quick Launcher

```bash
# The run.py launcher uses AI Agent by default
# For simple generation, call doc_generator.py directly
python src/doc_generator.py ./my-project
```

## Command-Line Options

### Basic Options

```bash
# Directory to analyze
python src/doc_generator.py /path/to/project

# Output format
python src/doc_generator.py ./project --format markdown
python src/doc_generator.py ./project --format html
python src/doc_generator.py ./project --format pdf

# Output filename
python src/doc_generator.py ./project --output my_docs
```

### Available Formats

**Markdown** (default)
```bash
python src/doc_generator.py ./project
# Output: project_documentation.md
```

**HTML**
```bash
python src/doc_generator.py ./project --format html
# Output: project_documentation.html
```

**PDF** (requires wkhtmltopdf)
```bash
python src/doc_generator.py ./project --format pdf
# Output: project_documentation.pdf
```

## Core Functions

### find_code_files()

Discovers code files in a directory.

```python
from src.doc_generator import find_code_files

files = find_code_files(
    directory="./my-project",
    max_files=30,
    project_type="backend"  # or "frontend", "mixed"
)

# Returns: List of tuples (file_path, file_content)
```

**Parameters:**
- `directory` - Path to analyze
- `max_files` - Maximum files to include (default: 30)
- `project_type` - Optional project type hint

**Returns:**
- List of tuples: `[(path, content), ...]`

### detect_project_type()

Auto-detects project type from files.

```python
from src.doc_generator import detect_project_type

project_type = detect_project_type("./my-project")
# Returns: "frontend", "backend", or "mixed"
```

**Detection Logic:**

**Frontend Indicators:**
- `package.json`, `yarn.lock`, `pnpm-lock.yaml`
- `.jsx`, `.tsx`, `.vue`, `.svelte` files
- `webpack.config.js`, `vite.config.ts`

**Backend Indicators:**
- `requirements.txt`, `Pipfile`
- `pom.xml`, `build.gradle`
- `go.mod`, `Cargo.toml`
- `Gemfile`, `composer.json`

**Mixed:**
- Contains both frontend and backend indicators

### generate_documentation()

Generates documentation from file contents.

```python
from src.doc_generator import generate_documentation

file_contents = [
    {"path": "main.py", "content": "# Main entry point..."},
    {"path": "utils.py", "content": "# Utility functions..."}
]

docs = generate_documentation(
    file_contents=file_contents,
    output_format="markdown",
    project_type="backend"
)
```

**Parameters:**
- `file_contents` - List of file dictionaries
- `output_format` - `"markdown"`, `"html"`, or `"pdf"`
- `project_type` - Optional type hint

**Returns:**
- String containing formatted documentation

### save_documentation()

Saves documentation to file.

```python
from src.doc_generator import save_documentation

save_documentation(
    content="# My Project Documentation...",
    output_format="markdown",
    output_file="my_docs"  # No extension
)
# Creates: my_docs.md
```

**Parameters:**
- `content` - Documentation content
- `output_format` - `"markdown"`, `"html"`, or `"pdf"`
- `output_file` - Filename without extension

**Output:**
- Returns full path to saved file

## Programmatic Usage

### Example 1: Simple Documentation

```python
from src.doc_generator import find_code_files, generate_documentation, save_documentation

# Find files
files = find_code_files("./my-app", max_files=30)

# Generate
docs = generate_documentation(files, output_format="markdown")

# Save
save_documentation(docs, "markdown", "my_app_docs")
```

### Example 2: Custom File Selection

```python
from src.doc_generator import generate_documentation, read_file_safe

# Manually select specific files
files = [
    {"path": "app/main.py", "content": read_file_safe("app/main.py")},
    {"path": "app/config.py", "content": read_file_safe("app/config.py")},
    {"path": "app/routes.py", "content": read_file_safe("app/routes.py")}
]

# Generate focused documentation
docs = generate_documentation(files, output_format="html")

# Save
with open("api_docs.html", "w", encoding="utf-8") as f:
    f.write(docs)
```

### Example 3: Batch Processing

```python
from src.doc_generator import find_code_files, generate_documentation, save_documentation
import os

projects = ["./project1", "./project2", "./project3"]

for project in projects:
    # Find files
    files = find_code_files(project, max_files=20)
    
    # Generate docs
    docs = generate_documentation(files, output_format="markdown")
    
    # Save with project name
    project_name = os.path.basename(project)
    save_documentation(docs, "markdown", f"{project_name}_docs")
    
    print(f"✓ Generated docs for {project_name}")
```

## Supported File Types

The generator supports these file extensions:

### Programming Languages
- **Python** - `.py`
- **JavaScript/TypeScript** - `.js`, `.ts`, `.jsx`, `.tsx`
- **Java** - `.java`
- **C#** - `.cs`
- **Go** - `.go`
- **Rust** - `.rs`
- **PHP** - `.php`
- **Ruby** - `.rb`
- **C/C++** - `.c`, `.cpp`, `.h`, `.hpp`
- **Kotlin** - `.kt`
- **Swift** - `.swift`
- **Scala** - `.scala`

### Web Technologies
- **HTML** - `.html`, `.htm`
- **CSS** - `.css`, `.scss`, `.sass`, `.less`
- **Vue** - `.vue`
- **Svelte** - `.svelte`

### Configuration & Data
- **JSON** - `.json`
- **YAML** - `.yaml`, `.yml`
- **XML** - `.xml`
- **SQL** - `.sql`

### Build & Config
- **Gradle** - `.gradle`
- **Shell** - `.sh`, `.bash`

## Ignored Directories

The generator automatically skips:

```python
IGNORED_DIRECTORIES = {
    'node_modules', '__pycache__', '.git', '.idea',
    'dist', 'build', '.next', '.nuxt', 'venv',
    'target', 'bin', 'obj', 'out', 'vendor',
    '.vscode', '.DS_Store', 'coverage'
}
```

## Configuration

The Simple Generator uses the same `.env` configuration:

```bash
# Model for generation
MODEL_NAME=llama2:7b

# API endpoint
OLLAMA_API_URL=http://localhost:11434/api/generate

# Timeout
API_TIMEOUT=300
```

See [Configuration Guide](../getting-started/configuration.md) for details.

## Output Structure

Generated documentation includes:

### 1. Project Overview
- Project description
- Technologies detected
- File structure

### 2. Key Files
For each analyzed file:
- File path and purpose
- Key functions/classes
- Basic documentation

### 3. Setup Instructions
- Basic installation steps
- Configuration hints
- Running the project

## Comparison Examples

### Simple Generator Output

**Time:** ~1 minute  
**Quality:** ⭐⭐

```markdown
# Project Documentation

## Overview
This is a web application built with React.

## Files
- src/App.tsx - Main application component
- src/index.tsx - Entry point
- package.json - Dependencies

## Setup
1. Install dependencies: npm install
2. Run: npm start
```

### AI Agent Output (3 iterations)

**Time:** ~5 minutes  
**Quality:** ⭐⭐⭐⭐⭐

```markdown
# Comprehensive Project Documentation

## Executive Overview
A modern React application featuring...
[Detailed description]

## Architecture
### Component Structure
[Detailed architecture diagram and explanation]

## Key Components
### App.tsx
[Detailed component documentation with props, state, examples]

## Development Setup
[Comprehensive installation guide]

## Deployment
[Production build and hosting instructions]

## Best Practices
[Coding standards, patterns used, recommendations]
```

## Troubleshooting

### No Files Found

```bash
# Check directory exists
ls ./my-project

# Try absolute path
python src/doc_generator.py /absolute/path/to/project

# Check file extensions are supported
# See "Supported File Types" section above
```

### Poor Output Quality

```bash
# Use AI Agent instead for better quality
python run.py --directory ./my-project

# Or increase context with more files
# (Edit max_files in script or use as module)
```

### API Errors

```bash
# Ensure Ollama is running
ollama serve

# Check configuration
cat .env | grep OLLAMA_API_URL
```

### PDF Generation Fails

```bash
# Install wkhtmltopdf
# Windows: choco install wkhtmltopdf
# Mac: brew install wkhtmltopdf
# Linux: sudo apt-get install wkhtmltopdf

# Or use markdown/html instead
python src/doc_generator.py ./project --format html
```

## Performance Tips

### Fast Generation

```bash
# Use fastest model
# In .env: MODEL_NAME=llama2:7b

# Limit files
python src/doc_generator.py ./project --max-files 15
```

### Better Quality (still single-pass)

```bash
# Use better model
# In .env: MODEL_NAME=codellama

# Include more files for context
python src/doc_generator.py ./project --max-files 50
```

## When to Upgrade to AI Agent

Consider using the AI Agent if you need:

- ✅ High-quality, production-ready documentation
- ✅ Comprehensive coverage of complex projects
- ✅ Self-critique and iterative refinement
- ✅ Better accuracy and detail
- ✅ Professional documentation standards

```bash
# Simple upgrade path
# From:
python src/doc_generator.py ./my-project

# To:
python run.py --directory ./my-project
```

## Next Steps

- [AI Agent Guide](ai-agent.md) - Upgrade to iterative refinement
- [Command Reference](commands.md) - Complete command documentation
- [Overview](overview.md) - Understanding both modes
- [Configuration](../getting-started/configuration.md) - Customize settings
