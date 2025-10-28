#!/usr/bin/env python3
"""
Base Agent Classes for AI Documentation Generation

This module provides base classes and interfaces for AI agents that generate,
critique, and refine technical documentation.
"""

import logging
from abc import ABC, abstractmethod
import os
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass


class ConfigurationError(AgentError):
    """Raised when there's a configuration error."""
    pass


class AnalysisError(AgentError):
    """Raised when code analysis fails."""
    pass


class GenerationError(AgentError):
    """Raised when documentation generation fails."""
    pass


@dataclass
class AgentConfig:
    """Configuration for AI agents with environment variable loading."""

    max_retries: int = field(default_factory=lambda: int(os.getenv("MAX_RETRIES", "3")))
    retry_delay: int = field(default_factory=lambda: int(os.getenv("RETRY_DELAY", "2")))
    critique_threshold: float = field(default_factory=lambda: float(os.getenv("CRITIQUE_THRESHOLD", "0.8")))
    enable_caching: bool = field(default_factory=lambda: os.getenv("ENABLE_CACHING", "true").lower() == "true")
    cache_dir: str = field(default_factory=lambda: os.getenv("CACHE_DIR", ".cache"))
    cache_max_age_hours: int = field(default_factory=lambda: int(os.getenv("CACHE_MAX_AGE_HOURS", "24")))
    cache_max_entries: int = field(default_factory=lambda: int(os.getenv("CACHE_MAX_ENTRIES", "100")))
    api_timeout: int = field(default_factory=lambda: int(os.getenv("API_TIMEOUT", "300")))

    def __post_init__(self):
        """Validate configuration values."""
        if self.max_retries < 0:
            raise ConfigurationError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ConfigurationError("retry_delay must be non-negative")
        if not (0.0 <= self.critique_threshold <= 1.0):
            raise ConfigurationError("critique_threshold must be between 0.0 and 1.0")
        if self.api_timeout <= 0:
            raise ConfigurationError("api_timeout must be positive")
        if self.cache_max_age_hours < 0:
            raise ConfigurationError("cache_max_age_hours must be non-negative")
        if self.cache_max_entries < 0:
            raise ConfigurationError("cache_max_entries must be non-negative")

    def __repr__(self) -> str:
        return (f"AgentConfig(max_retries={self.max_retries}, "
                f"retry_delay={self.retry_delay}, "
                f"critique_threshold={self.critique_threshold}, "
                f"caching={self.enable_caching})")


class BaseAgent(ABC):
    """
    Abstract base class for documentation generation agents.

    Provides common functionality for analyzing codebases, generating documentation,
    and managing the refinement process.
    """

    def __init__(
        self,
        directory: str,
        max_files: int,
        model: str,
        project_type: Optional[str],
        output_format: str,
        output_file: Optional[str],
        config: AgentConfig,
    ):
        self.directory = Path(directory).resolve()
        self.max_files = max_files
        self.model = model
        self.project_type = project_type
        self.output_format = output_format
        self.output_file = output_file
        self.config = config
        self.file_contents: List[Dict[str, str]] = []
        self.documentation: Optional[str] = None
        self.critique: Optional[str] = None

        logger.info(f"Agent initialized with config: {self.config}")

    def validate_inputs(self) -> None:
        """Validate input parameters."""
        if not self.directory.exists():
            raise AnalysisError(f"Directory does not exist: {self.directory}")
        if not self.directory.is_dir():
            raise AnalysisError(f"Path is not a directory: {self.directory}")
        if self.max_files < 1:
            raise AnalysisError(f"Invalid max_files: {self.max_files}")

    @abstractmethod
    def analyze_codebase(self) -> None:
        """Analyze the codebase to find and read relevant files."""
        pass

    @abstractmethod
    def generate_documentation_draft(self) -> str:
        """Generate the initial documentation draft."""
        pass

    @abstractmethod
    def critique_documentation(self, documentation: str) -> str:
        """Critique the current documentation draft."""
        pass

    @abstractmethod
    def refine_documentation(self, documentation: str, critique: str) -> str:
        """Refine documentation based on critique."""
        pass

    @abstractmethod
    def is_critique_positive(self, critique: str) -> bool:
        """Check if the critique indicates documentation is satisfactory."""
        pass

    @abstractmethod
    def save_documentation(self) -> str:
        """Save the final documentation to file."""
        pass

    @abstractmethod
    def run(self, max_iterations: int = 3) -> int:
        """Main execution loop for the agent."""
        pass


class DocumentationTemplates:
    """Templates for documentation generation prompts."""

    CRITIQUE_PROMPT = """You are a senior quality assurance engineer and technical documentation expert.

Your task is to critique the following technical documentation with a focus on:

1. **Clarity**: Is the documentation clear, concise, and easy to understand?
2. **Completeness**: Are there missing sections, important details, or undocumented features?
3. **Accuracy**: Is the information technically correct based on code context?
4. **Structure**: Is the organization logical and well-formatted?
5. **Usefulness**: Will this help developers understand and use the codebase?

Provide a numbered list of specific, actionable feedback items.

If the documentation is excellent and requires no changes, respond ONLY with:
"The documentation is excellent and requires no changes."

Documentation to critique:
---
{documentation}
---

Provide your critique below:
"""

    REFINEMENT_PROMPT = """You are a senior technical writer. Your task is to refine the documentation based on the critique.

Original Documentation:
---
{documentation}
---

Critique to Address:
---
{critique}
---

Code Files Summary (for reference):
---
{file_summaries}
---

Instructions:
- Address ALL points in the critique
- Maintain the overall structure and formatting
- Ensure technical accuracy
- Make the documentation more clear and useful
- Provide a COMPLETE, refined version of the documentation

Refined Documentation:
"""

    @staticmethod
    def get_project_description(project_type: str) -> str:
        """Get project-specific description for documentation generation."""
        descriptions = {
            "frontend": """
You are a senior technical documentation writer. Analyze the following frontend codebase
and generate comprehensive technical documentation.

Project Overview:
This is a frontend application. Analyze the frameworks, libraries, UI components, state management,
routing, and styling approaches used. Focus on component architecture, user interface patterns,
and client-side functionality.""",
            "backend": """
You are a senior technical documentation writer. Analyze the following backend codebase
and generate comprehensive technical documentation.

Project Overview:
This is a backend application. Analyze the API endpoints, data models, database interactions,
authentication/authorization, middleware, services, and business logic. Focus on server-side
architecture, API design patterns, and data flow.""",
            "mixed": """
You are a senior technical documentation writer. Analyze the following codebase
and generate comprehensive technical documentation.

Project Overview:
This is a full-stack application with both frontend and backend components. Analyze both
client-side and server-side architecture, their integration, and communication patterns."""
        }
        return descriptions.get(project_type, descriptions["mixed"])

    @staticmethod
    def get_format_instructions(output_format: str) -> str:
        """Get format-specific instructions."""
        instructions = {
            "html": "Generate documentation in HTML format with proper HTML5 structure.",
            "pdf": "Generate documentation in Markdown format that will be converted to PDF.",
            "markdown": "Generate documentation in well-structured Markdown format."
        }
        return instructions.get(output_format.lower(), instructions["markdown"])

    @staticmethod
    def build_generation_prompt(
        file_summaries: str,
        docstring_info: str,
        output_format: str,
        project_type: str
    ) -> str:
        """Build the main documentation generation prompt."""
        project_intro = DocumentationTemplates.get_project_description(project_type)
        format_instructions = DocumentationTemplates.get_format_instructions(output_format)

        return f"""
{project_intro}

{format_instructions}

Structure your documentation with these exact sections:

# Project Documentation

## 1. Project Overview
- High-level description of the project's purpose and functionality
- Primary technologies and frameworks used
- Target audience and use cases

## 2. Architecture and Design
- Overall architecture and component structure
- Key design patterns and principles
- Folder organization and code structure
- State management approach
- Performance optimization strategies

## 3. Key Components and Modules
For each major component/module:
- Purpose and functionality
- Key features and capabilities
- Dependencies and relationships
- Implementation details

## 4. Development Setup
- Prerequisites and system requirements
- Installation instructions
- Environment configuration
- Available scripts and commands

## 5. Deployment
- Build process
- Deployment options
- Hosting considerations

## 6. File Documentation
For each significant file (prioritize important files):
- File path and purpose
- Key functions/classes/methods with parameters and return values
- Usage examples where applicable

## 7. Best Practices and Guidelines
- Coding standards
- Performance considerations
- Accessibility features
- Security considerations

Here are the code files to analyze:

{file_summaries}

Here are extracted documentation comments:

{docstring_info}

IMPORTANT:
- Provide specific, actionable information
- Use proper formatting with headers, lists, and code blocks
- Focus on the most important files first (package.json, README.md, App.tsx, etc.)
- Be concise but comprehensive
- Do not include any backticks or code block markers in your response
- Do not use phrases like "This is a placeholder" or "This is a sample"
""".strip()
