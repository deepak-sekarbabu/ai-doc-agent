"""File utilities for the AI Documentation Agent."""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# File type constants
SUPPORTED_EXTENSIONS: Set[str] = frozenset([
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cs", ".go", ".php", 
    ".rb", ".rs", ".c", ".cpp", ".h", ".hpp", ".html", ".css", ".scss", 
    ".sql", ".sh", ".kt", ".swift", ".vue", ".svelte", ".xml", ".gradle"
])

IGNORED_DIRECTORIES: Set[str] = frozenset([
    "node_modules", ".git", ".vscode", ".idea", "__pycache__", "dist", 
    "build", "target", "out", "bin", "obj", "vendor", "tmp", "temp", 
    ".next", "docs", "coverage", ".pytest_cache"
])

FRONTEND_EXTENSIONS: Set[str] = frozenset([
    ".js", ".ts", ".tsx", ".jsx", ".vue", ".svelte", ".html", ".css", ".scss"
])

BACKEND_EXTENSIONS: Set[str] = frozenset([
    ".py", ".java", ".cs", ".go", ".php", ".rb", ".rs", ".c", ".cpp", ".h", ".hpp", ".kt", ".swift", ".sql"
])

PRIORITY_FILES: Dict[str, Set[str]] = {
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

MAX_CONTENT_PREVIEW: int = 2000


def _get_allowed_extensions(project_type: str) -> Set[str]:
    """
    Get the appropriate extensions based on project type.
    
    Args:
        project_type: The type of project ('frontend', 'backend', or 'mixed')
        
    Returns:
        Set of file extensions appropriate for the project type
    """
    if project_type == "frontend":
        return FRONTEND_EXTENSIONS
    elif project_type == "backend":
        return BACKEND_EXTENSIONS
    else:
        return SUPPORTED_EXTENSIONS


def _get_priority_files(project_type: str) -> Set[str]:
    """
    Get the appropriate priority files based on project type.
    
    Args:
        project_type: The type of project ('frontend', 'backend', or 'mixed')
        
    Returns:
        Set of priority file names for the project type
    """
    return PRIORITY_FILES.get(project_type, PRIORITY_FILES["frontend"] | PRIORITY_FILES["backend"])


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
    
    priority_files_list = _get_priority_files(project_type)
    allowed_extensions = _get_allowed_extensions(project_type)
    
    priority_files: List[str] = []
    code_files: List[str] = []
    
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
        logger.warning(f"Could not read {file_path}: {e}")
        return None
    except UnicodeDecodeError as e:
        logger.warning(f"Could not decode {file_path}: {e}")
        return None
    except Exception as e:
        logger.warning(f"Unexpected error reading {file_path}: {e}")
        return None