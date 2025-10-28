"""AI Documentation Agent - Source Package"""

__version__ = "2.0.0"
__author__ = "deepak-sekarbabu"
__description__ = "AI-powered documentation generator with iterative self-improvement"

from .ai_agent import AIAgent
from .base_agent import AgentConfig, AgentError, ConfigurationError, AnalysisError, GenerationError
from .doc_generator import (
    generate_documentation,
    find_code_files,
    detect_project_type,
    DocGeneratorError,
    OllamaConnectionError,
)

__all__ = [
    "AIAgent",
    "AgentConfig",
    "AgentError",
    "ConfigurationError",
    "AnalysisError",
    "GenerationError",
    "generate_documentation",
    "find_code_files",
    "detect_project_type",
    "DocGeneratorError",
    "OllamaConnectionError",
]
