#!/usr/bin/env python3
"""
Documentation Generator for Code Projects

Automatically generates comprehensive documentation for code projects using Ollama AI.
Supports multiple output formats (Markdown, HTML, PDF) and intelligent file prioritization.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import re

import requests
from dotenv import load_dotenv
import markdown
import pdfkit

from .base_agent import DocumentationTemplates

load_dotenv()

# Configure Ollama API URL based on mode
OLLAMA_MODE = os.getenv("OLLAMA_MODE", "cloud").lower()
if OLLAMA_MODE == "local":
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
else:
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "https://ollama.com/api/generate")

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss:120b-cloud")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "300"))

SUPPORTED_EXTENSIONS = frozenset([
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".go", ".php", 
    ".rb", ".rs", ".c", ".cpp", ".h", ".hpp", ".html", ".css", ".scss", 
    ".sql", ".sh", ".kt", ".swift", ".vue", ".svelte", ".xml", ".gradle"
])

IGNORED_DIRECTORIES = frozenset([
    "node_modules", ".git", ".vscode", ".idea", "__pycache__", "dist", 
    "build", "target", "out", "bin", "obj", "vendor", "tmp", "temp", 
    ".next", "docs", "coverage", ".pytest_cache"
])

FRONTEND_EXTENSIONS = frozenset([
    ".js", ".ts", ".tsx", ".jsx", ".vue", ".svelte", ".html", ".css", ".scss"
])

BACKEND_EXTENSIONS = frozenset([
    ".py", ".java", ".cs", ".go", ".php", ".rb", ".rs", ".c", ".cpp", ".h", ".hpp", ".kt", ".swift", ".sql"
])

PRIORITY_FILES = {
    "frontend": frozenset([
        "package.json", "README.md", "index.html", "App.tsx", "App.jsx",
        "main.tsx", "main.jsx", "vite.config.ts", "tailwind.config.ts",
        "tsconfig.json", "webpack.config.js", "next.config.js", "nuxt.config.js"
    ]),
    "backend": frozenset([
        "pom.xml", "build.gradle", "settings.gradle", "application.properties", 
        "application.yml", "setup.py", "requirements.txt", "go.mod", "Cargo.toml",
        "composer.json", "Program.cs", "Startup.cs", "README.md", "Gemfile"
    ])
}

MAX_CONTENT_PREVIEW = 2000


class DocGeneratorError(Exception):
    """Base exception for documentation generator errors."""
    pass


class OllamaConnectionError(DocGeneratorError):
    """Raised when unable to connect to Ollama API."""
    pass


def detect_project_type(start_path: str) -> str:
    """
    Auto-detect project type based on configuration files.
    
    Args:
        start_path: Root directory to analyze
        
    Returns:
        Project type: 'frontend', 'backend', or 'mixed'
    """
    indicators = {
        "frontend": ["package.json", "yarn.lock", "pnpm-lock.yaml"],
        "backend": ["pom.xml", "build.gradle", "go.mod", "Cargo.toml", "requirements.txt", "Gemfile"]
    }
    
    found_types = set()
    
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRECTORIES]
        
        for file in files:
            if file in indicators["frontend"]:
                found_types.add("frontend")
            if file in indicators["backend"]:
                found_types.add("backend")
        
        if len(found_types) == 2:
            return "mixed"
    
    if "frontend" in found_types:
        return "frontend"
    elif "backend" in found_types:
        return "backend"
    
    return "mixed"


def find_code_files(start_path: str, max_files: int = 50, project_type: Optional[str] = None) -> List[str]:
    """
    Find supported code files in a directory with intelligent prioritization.
    
    Args:
        start_path: Root directory to search
        max_files: Maximum number of files to return
        project_type: Project type ('frontend', 'backend', 'mixed', or None for auto-detect)
        
    Returns:
        List of file paths, with priority files first
    """
    if not os.path.isdir(start_path):
        raise ValueError(f"Invalid directory: {start_path}")
    
    if project_type is None:
        project_type = detect_project_type(start_path)
    
    priority_files_list = PRIORITY_FILES.get(project_type, PRIORITY_FILES["frontend"] | PRIORITY_FILES["backend"])
    
    allowed_extensions = SUPPORTED_EXTENSIONS
    if project_type == "frontend":
        allowed_extensions = FRONTEND_EXTENSIONS
    elif project_type == "backend":
        allowed_extensions = BACKEND_EXTENSIONS
    
    priority_files = []
    code_files = []
    
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRECTORIES]
        
        for file in files:
            if not any(file.endswith(ext) for ext in allowed_extensions):
                continue
                
            file_path = os.path.join(root, file)
            if os.path.basename(file) in priority_files_list:
                priority_files.append(file_path)
            else:
                code_files.append(file_path)
    
    all_files = priority_files + code_files
    return all_files[:max_files]


def read_file_safe(file_path: str) -> Optional[str]:
    """
    Safely read file content with error handling.
    
    Args:
        file_path: Path to file to read
        
    Returns:
        File content or None if reading fails
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except (IOError, OSError) as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
        return None


def extract_docstrings(content: str) -> Dict[str, str]:
    """Extract Python docstrings from code."""
    docstrings = {}
    pattern = r'(def|class)\s+([^\s\(]+).*?:\s*\n\s*"""(.*?)"""'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        entity_type, entity_name, docstring = match.groups()
        docstrings[f"{entity_type} {entity_name}"] = docstring.strip()
    
    return docstrings


def extract_jsdoc(content: str) -> Dict[str, str]:
    """Extract JSDoc comments from JavaScript/TypeScript code."""
    jsdocs = {}
    pattern = r'/\*\*(.*?)\*/\s*(?:export\s+)?(?:function|class|const|let|var)\s+([^\s\(=]+)'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        doc_comment, entity_name = match.groups()
        doc_lines = [line.strip().lstrip('*').strip() for line in doc_comment.split('\n')]
        cleaned_doc = '\n'.join(line for line in doc_lines if line)
        jsdocs[entity_name] = cleaned_doc
    
    return jsdocs


def get_ollama_headers() -> Dict[str, str]:
    """Build request headers with optional API key authentication."""
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("OLLAMA_API_KEY")
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    return headers


def check_ollama_connection() -> bool:
    """Verify Ollama API is accessible."""
    try:
        # For cloud mode, check the base domain; for local, check the API endpoint
        if OLLAMA_MODE == "local":
            # Check if local Ollama is running by trying to access the API endpoint
            response = requests.get(
                "http://localhost:11434/api/tags",
                headers=get_ollama_headers(),
                timeout=5
            )
        else:
            # For cloud mode, check the base domain
            response = requests.get(
                "https://ollama.com/",
                headers=get_ollama_headers(),
                timeout=5
            )
        return response.status_code == 200
    except requests.RequestException:
        return False


def build_prompt(file_summaries: str, docstring_info: str, output_format: str, project_type: str = "mixed") -> str:
    """Build the documentation generation prompt."""
    return DocumentationTemplates.build_generation_prompt(
        file_summaries, docstring_info, output_format, project_type
    )


def generate_documentation(
    file_contents: List[Dict[str, str]], 
    output_format: str = "markdown",
    model: str = MODEL_NAME,
    project_type: str = "mixed"
) -> str:
    """
    Generate documentation using Ollama API.
    
    Args:
        file_contents: List of dicts with 'path' and 'content' keys
        output_format: Output format (markdown, html, pdf)
        model: Ollama model name
        project_type: Project type (frontend, backend, mixed)
        
    Returns:
        Generated documentation string
        
    Raises:
        DocGeneratorError: If documentation generation fails
    """
    if not file_contents:
        raise DocGeneratorError("No code files to document")
    
    file_summaries = []
    docstring_info = []
    
    for file_info in file_contents:
        path = file_info['path']
        content = file_info['content']
        
        content_preview = content[:MAX_CONTENT_PREVIEW]
        if len(content) > MAX_CONTENT_PREVIEW:
            content_preview += "..."
        
        file_summaries.append(f"--- File: {path} ---\n{content_preview}")
        
        if path.endswith('.py'):
            docstrings = extract_docstrings(content)
            if docstrings:
                docstring_info.append(f"--- Docstrings from {path} ---")
                docstring_info.extend(f"{k}: {v}" for k, v in docstrings.items())
        
        elif path.endswith(('.js', '.ts', '.tsx', '.jsx')):
            jsdocs = extract_jsdoc(content)
            if jsdocs:
                docstring_info.append(f"--- JSDoc from {path} ---")
                docstring_info.extend(f"{k}: {v}" for k, v in jsdocs.items())
    
    prompt = build_prompt(
        "\n".join(file_summaries),
        "\n".join(docstring_info),
        output_format,
        project_type
    )
    
    print(f"Sending request to Ollama API (model: {model})...")
    print(f"Prompt: {len(prompt)} chars (~{len(prompt) // 4} tokens)")
    
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            headers=get_ollama_headers(),
            timeout=API_TIMEOUT
        )
        response.raise_for_status()
        
        resp_data = response.json()
        doc = resp_data.get("response") or resp_data.get("text")
        
        if not doc:
            raise DocGeneratorError("Invalid API response format")
        
        doc = re.sub(r"```.*?```", "", doc, flags=re.DOTALL)
        doc = re.sub(r"<think>.*?</think>", "", doc, flags=re.DOTALL)
        
        print("Documentation generated successfully")
        return doc
        
    except requests.Timeout:
        raise DocGeneratorError(f"API request timeout after {API_TIMEOUT}s")
    except requests.HTTPError as e:
        raise DocGeneratorError(f"API request failed: {e}")
    except requests.RequestException as e:
        raise DocGeneratorError(f"Network error: {e}")


def convert_markdown_to_html(markdown: str) -> str:
    """
    Simple markdown to HTML conversion.
    
    Note: For production use, consider using a library like markdown2 or python-markdown.
    """
    html = markdown
    
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>\n)+', r'<ul>\n\g<0></ul>', html, flags=re.DOTALL)
    html = re.sub(r'(?<!\n)\n(?!\n)(?!<[uo]l|<li|<h[1-6])', r'<br>', html)
    html = re.sub(r'(?<!\n)\n\n(?!<[uo]l|<li|<h[1-6])', r'</p>\n\n<p>', html)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Documentation</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; 
                color: #333; }}
        h1, h2, h3 {{ color: #2c3e50; margin-top: 1.5em; }}
        h1 {{ border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
        code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; 
                font-family: 'Courier New', monospace; }}
        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; 
               overflow-x: auto; border-left: 4px solid #3498db; }}
        ul {{ padding-left: 30px; }}
        li {{ margin: 8px 0; }}
    </style>
</head>
<body>
    <p>{html}</p>
</body>
</html>
"""


def convert_to_pdf(markdown_content: str, output_path: str) -> None:
    """Convert markdown content to PDF using pdfkit."""
    html_content = markdown.markdown(
        markdown_content,
        extensions=['extra', 'codehilite', 'toc']
    )
    
    styled_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Documentation</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 40px; 
                color: #333; }}
        h1, h2, h3 {{ color: #2c3e50; margin-top: 1.5em; }}
        h1 {{ border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
        code {{ background-color: #f4f4f4; padding: 2px 6px; border-radius: 3px; 
                font-family: 'Courier New', monospace; font-size: 0.9em; }}
        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; 
               overflow-x: auto; border-left: 4px solid #3498db; }}
        ul, ol {{ padding-left: 30px; }}
        li {{ margin: 8px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    pdfkit.from_string(styled_html, output_path, options={
        'encoding': 'UTF-8',
        'enable-local-file-access': None
    })


def save_documentation(content: str, output_format: str, output_file: Optional[str] = None, output_dir: Optional[Path] = None) -> str:
    """
    Save documentation to file.

    Args:
        content: Documentation content
        output_format: Output format (markdown, html, pdf)
        output_file: Optional output filename (without extension)
        output_dir: Optional output directory path

    Returns:
        Path to saved file
    """
    # Create output directory if it doesn't exist
    if output_dir is None:
        output_dir = Path("output")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = output_file.rsplit('.', 1)[0] if output_file else f"documentation_{timestamp}"
    
    if output_format.lower() == "html":
        filename = output_dir / f"{base_name}.html"
        final_content = convert_markdown_to_html(content)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(final_content)
    elif output_format.lower() == "pdf":
        filename = output_dir / f"{base_name}.pdf"
        try:
            convert_to_pdf(content, str(filename))
            print("PDF generated successfully")
        except Exception as e:
            print(f"PDF generation failed: {e}")
            print("Falling back to Markdown format...")
            filename = output_dir / f"{base_name}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print("\nNote: Install wkhtmltopdf for PDF support:")
            print("Windows: choco install wkhtmltopdf or download from https://wkhtmltopdf.org/downloads.html")
    else:
        filename = output_dir / f"{base_name}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
    
    return str(filename)