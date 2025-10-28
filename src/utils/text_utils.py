"""Text processing utilities for the AI Documentation Agent."""

import re
from typing import Dict


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


def clean_markdown_response(response: str) -> str:
    """
    Clean markdown response by removing code block markers.
    
    This function removes markdown code block delimiters and other formatting
    markers that may be included in LLM responses but are not desired in the
    final documentation.
    
    Args:
        response: Raw response from the LLM
        
    Returns:
        Cleaned response with formatting markers removed
    """
    # Remove markdown code block markers
    cleaned = re.sub(r"```.*?```", "", response, flags=re.DOTALL)
    # Remove any special formatting markers if present
    return cleaned.strip()