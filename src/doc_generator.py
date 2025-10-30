#!/usr/bin/env python3
"""
Documentation Generator for Code Projects

Automatically generates comprehensive documentation for code projects using Ollama AI.
Supports multiple output formats (Markdown, HTML, PDF) and intelligent file prioritization.
"""

import os
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import markdown
import pdfkit
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

try:
    from .base_agent import DocumentationTemplates  # noqa: E402
    from .utils.file_utils import find_code_files, read_file_safe, detect_project_type, MAX_CONTENT_PREVIEW  # noqa: E402
    from .utils.text_utils import extract_docstrings, extract_jsdoc, clean_markdown_response  # noqa: E402
    from .utils.api_utils import ResponseCache, call_ollama_api, get_ollama_headers, OLLAMA_API_URL, MODEL_NAME, API_TIMEOUT  # noqa: E402
except ImportError:
    from base_agent import DocumentationTemplates  # noqa: E402
    from utils.file_utils import find_code_files, read_file_safe, detect_project_type, MAX_CONTENT_PREVIEW  # noqa: E402
    from utils.text_utils import extract_docstrings, extract_jsdoc, clean_markdown_response  # noqa: E402
    from utils.api_utils import ResponseCache, call_ollama_api, get_ollama_headers, OLLAMA_API_URL, MODEL_NAME, API_TIMEOUT  # noqa: E402

load_dotenv()

class DocGeneratorError(Exception):
    """Base exception for documentation generator errors."""
    pass


class OllamaConnectionError(DocGeneratorError):
    """Raised when unable to connect to Ollama API."""
    pass


def build_prompt(file_summaries: str, docstring_info: str, output_format: str, project_type: str = "mixed") -> str:
    """Build the documentation generation prompt."""
    return DocumentationTemplates.build_generation_prompt(
        file_summaries, docstring_info, output_format, project_type
    )


def _prepare_file_summaries(file_contents: List[Dict[str, str]]) -> Tuple[List[str], List[str]]:
    """Prepare file summaries and docstring info from file contents."""
    file_summaries: List[str] = []
    docstring_info: List[str] = []
    
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
    
    return file_summaries, docstring_info


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
    
    file_summaries, docstring_info = _prepare_file_summaries(file_contents)
    
    prompt = build_prompt(
        "\n".join(file_summaries),
        "\n".join(docstring_info),
        output_format,
        project_type
    )
    
    logger.info(f"Sending request to Ollama API (model: {model})")
    logger.debug(f"Prompt: {len(prompt)} chars (~{len(prompt) // 4} tokens)")
    
    # Use the utility function for API calls with caching
    cache = ResponseCache()  # Use default settings or load from config
    doc = call_ollama_api(
        prompt=prompt,
        model=model,
        max_retries=3,
        retry_delay=2,
        api_timeout=API_TIMEOUT,
        use_cache=True,
        cache=cache
    )
    
    # Clean the response
    doc = clean_markdown_response(doc)
    
    logger.info("Documentation generated successfully")
    return doc


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
    
    try:
        output_dir.mkdir(exist_ok=True, parents=True)
    except OSError as e:
        logger.error(f"Failed to create output directory {output_dir}: {e}")
        raise DocGeneratorError(f"Cannot create output directory: {e}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = output_file.rsplit('.', 1)[0] if output_file else f"documentation_{timestamp}"

    try:
        if output_format.lower() == "html":
            filename = output_dir / f"{base_name}.html"
            final_content = convert_markdown_to_html(content)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_content)
        elif output_format.lower() == "pdf":
            filename = output_dir / f"{base_name}.pdf"
            try:
                convert_to_pdf(content, str(filename))
                logger.info("PDF generated successfully")
            except Exception as e:
                logger.warning(f"PDF generation failed: {e}. Falling back to Markdown format...")
                filename = output_dir / f"{base_name}.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                logger.info("Note: Install wkhtmltopdf for PDF support: https://wkhtmltopdf.org/downloads.html")
        else:
            filename = output_dir / f"{base_name}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
    except OSError as e:
        logger.error(f"Failed to write documentation to {filename}: {e}")
        raise DocGeneratorError(f"Cannot write documentation file: {e}")

    return str(filename)