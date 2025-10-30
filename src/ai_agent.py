#!/usr/bin/env python3
"""
AI Agent for Code Documentation Generation

This script defines an AI agent that autonomously generates, critiques, and refines
documentation for code projects using iterative improvement cycles.

Best Practices Implemented:
- Structured logging with appropriate levels
- Configuration management via environment variables
- Retry logic with exponential backoff
- Result caching to avoid redundant API calls
- Comprehensive error handling
- Progress tracking and reporting
- Modular, testable design
- Semantic critique analysis with cross-validation
"""

import os
import sys
import argparse
import logging
import time
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional, Union
try:
    from .utils.semantic_critique import ValidationIssue
except ImportError:
    from utils.semantic_critique import ValidationIssue
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

try:
    from .doc_generator import (
        DocGeneratorError,
        save_documentation,
        generate_documentation
    )
    from .utils.file_utils import find_code_files, read_file_safe, detect_project_type
    from .utils.api_utils import call_ollama_api, get_ollama_headers, OLLAMA_API_URL, MODEL_NAME, API_TIMEOUT
    from .utils.semantic_critique import (
        SemanticCritiqueAnalyzer,
        DocumentationValidator,
        create_semantic_critique_score,
        ValidationResult
    )
    from .base_agent import BaseAgent, AgentConfig, DocumentationTemplates
    from .utils.api_utils import ResponseCache
except ImportError:
    from doc_generator import (
        DocGeneratorError,
        save_documentation,
        generate_documentation
    )
    from utils.file_utils import find_code_files, read_file_safe, detect_project_type
    from utils.api_utils import call_ollama_api, get_ollama_headers, OLLAMA_API_URL, MODEL_NAME, API_TIMEOUT
    from utils.semantic_critique import (
        SemanticCritiqueAnalyzer,
        DocumentationValidator,
        create_semantic_critique_score,
        ValidationResult
    )
    from base_agent import BaseAgent, AgentConfig, DocumentationTemplates
    from utils.api_utils import ResponseCache

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('ai_agent.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class AIAgent(BaseAgent):
    """
    An AI agent that generates and refines documentation for a codebase.

    The agent follows a critique-refine cycle to iteratively improve documentation quality.
    It uses LLM-powered self-critique to identify areas for improvement.

    Inherits common functionality from BaseAgent.
    """

    def __init__(
        self,
        directory: str,
        max_files: int,
        model: str,
        project_type: Optional[str],
        output_format: str,
        output_file: Optional[str],
        config: Optional[AgentConfig] = None
    ):
        # Use default config if none provided (loads from environment variables)
        if config is None:
            config = AgentConfig()

        super().__init__(directory, max_files, model, project_type,
                         output_format, output_file, config)

        self.cache = ResponseCache(
            cache_dir=self.config.cache_dir,
            max_age_hours=self.config.cache_max_age_hours,
            max_entries=self.config.cache_max_entries
        ) if self.config.enable_caching else None
        
        # Initialize semantic critique analyzer and validator
        self.semantic_analyzer = SemanticCritiqueAnalyzer()
        self.documentation_validator = None  # Will be set after code analysis
        
        self.iteration_metrics: List[Dict[str, Union[int, float]]] = []

    def run(self, max_iterations: int = 3) -> int:
        """
        Main execution loop for the agent.

        Args:
            max_iterations: Maximum number of refinement iterations

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        logger.info("AI Agent activated. Starting documentation process...")
        start_time = time.time()

        try:
            self.validate_inputs()
            self.analyze_codebase()

            logger.info("Generating initial documentation draft...")
            self.documentation = self.generate_documentation_draft()

            for i in range(max_iterations):
                logger.info(f"Iteration {i + 1}/{max_iterations}")
                iteration_start = time.time()

                self.critique = self.critique_documentation(self.documentation)
                logger.info(f"Critique: {self.critique[:200]}...")

                if self.is_critique_positive(self.critique):
                    logger.info("Critique is positive. Finalizing documentation.")
                    break

                logger.info("Refining documentation based on critique...")
                self.documentation = self.refine_documentation(
                    self.documentation,
                    self.critique
                )

                iteration_time = time.time() - iteration_start
                self.iteration_metrics.append({
                    "iteration": i + 1,
                    "time": iteration_time,
                    "doc_length": len(self.documentation)
                })
            else:
                logger.warning("Max refinement iterations reached without positive critique.")

            output_path = self.save_documentation()

            total_time = time.time() - start_time
            self._log_completion_metrics(output_path, total_time)

            return 0

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return 1

    def analyze_codebase(self) -> None:
        """Analyze the codebase to find and read relevant files."""
        logger.info(f"Analyzing directory: {self.directory}")

        if self.project_type is None:
            self.project_type = detect_project_type(str(self.directory))
            logger.info(f"Auto-detected project type: {self.project_type}")
        else:
            logger.info(f"Project type: {self.project_type}")

        code_files = find_code_files(
            str(self.directory),
            self.max_files,
            self.project_type
        )

        if not code_files:
            raise DocGeneratorError("No supported code files found.")

        logger.info(f"Found {len(code_files)} files to analyze")

        # Read files in parallel for better performance
        file_contents = []
        with ThreadPoolExecutor(max_workers=min(8, len(code_files))) as executor:
            future_to_file = {
                executor.submit(read_file_safe, file_path): file_path
                for file_path in code_files
            }
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    content = future.result()
                    if content:
                        rel_path = os.path.relpath(file_path, self.directory)
                        logger.debug(f"Read: {rel_path}")
                        file_contents.append({
                            "path": rel_path,
                            "content": content
                        })
                except Exception as e:
                    logger.warning(f"Failed to read {file_path}: {e}")

        self.file_contents = file_contents

        if not self.file_contents:
            raise DocGeneratorError("No files could be read successfully.")

        # Initialize documentation validator with analyzed files
        self.documentation_validator = DocumentationValidator(self.file_contents)

        logger.info(f"Successfully read {len(self.file_contents)} files")

    def generate_documentation_draft(self) -> str:
        """
        Generate the initial documentation draft.

        Returns:
            Generated documentation string
        """
        return generate_documentation(
            self.file_contents,
            self.output_format,
            self.model,
            self.project_type
        )

    def critique_documentation(self, documentation: str) -> str:
        """
        Use the LLM to critique the documentation with semantic understanding.

        This method generates a critique using the LLM and then performs
        semantic analysis and cross-validation to provide comprehensive feedback.

        Args:
            documentation: Documentation to critique

        Returns:
            Enhanced critique text with semantic analysis and validation results
        """
        # Generate initial critique from LLM
        prompt = DocumentationTemplates.CRITIQUE_PROMPT.format(documentation=documentation)
        initial_critique = self._call_ollama_with_retry(prompt, operation="critique")
        
        # Perform semantic analysis of the critique
        semantic_score = self.semantic_analyzer.analyze_critique_semantically(initial_critique)
        
        # Cross-validate documentation against code
        validation_issues = []
        if self.documentation_validator:
            validation_issues = self.documentation_validator.validate_documentation(documentation)
        
        # Generate enhanced critique with validation results
        enhanced_critique = self._enhance_critique_with_validation(
            initial_critique,
            semantic_score,
            validation_issues
        )
        
        return enhanced_critique

    def _enhance_critique_with_validation(self, initial_critique: str,
                                        semantic_score,
                                        validation_issues: List) -> str:
        """
        Enhance the initial critique with semantic analysis and validation results.
        
        Args:
            initial_critique: Original critique from LLM
            semantic_score: Semantic analysis results
            validation_issues: Validation issues found
            
        Returns:
            Enhanced critique with validation insights
        """
        critique_lines = [initial_critique.strip()]
        
        # Add semantic analysis insights
        critique_lines.append(f"\n## Semantic Analysis")
        critique_lines.append(f"- Overall Quality Score: {semantic_score.overall_score:.2f}/1.00")
        critique_lines.append(f"- Technical Accuracy: {semantic_score.technical_accuracy:.2f}")
        critique_lines.append(f"- Completeness: {semantic_score.completeness:.2f}")
        critique_lines.append(f"- Clarity: {semantic_score.clarity:.2f}")
        critique_lines.append(f"- Structure: {semantic_score.structure:.2f}")
        critique_lines.append(f"- Usefulness: {semantic_score.usefulness:.2f}")
        critique_lines.append(f"- Confidence: {semantic_score.confidence:.2f}")
        
        # Add validation results
        if validation_issues:
            critique_lines.append(f"\n## Cross-Validation Results")
            
            errors = [issue for issue in validation_issues if issue.severity == ValidationResult.ERROR]
            warnings = [issue for issue in validation_issues if issue.severity == ValidationResult.WARNING]
            
            if errors:
                critique_lines.append(f"\n### Critical Issues ({len(errors)}):")
                for issue in errors[:5]:  # Show up to 5 critical issues
                    critique_lines.append(f"- **{issue.issue_type}**: {issue.description}")
                    critique_lines.append(f"  → {issue.suggested_fix}")
                    if issue.location:
                        critique_lines.append(f"  → Location: {issue.location}")
            
            if warnings:
                critique_lines.append(f"\n### Warnings ({len(warnings)}):")
                for issue in warnings[:5]:  # Show up to 5 warnings
                    critique_lines.append(f"- **{issue.issue_type}**: {issue.description}")
                    critique_lines.append(f"  → {issue.suggested_fix}")
                    if issue.location:
                        critique_lines.append(f"  → Location: {issue.location}")
        else:
            critique_lines.append(f"\n## Cross-Validation Results")
            critique_lines.append("✅ No validation issues found - documentation aligns well with code structure")
        
        return "\n".join(critique_lines)

    def refine_documentation(self, documentation: str, critique: str) -> str:
        """
        Refine the documentation based on critique.

        Args:
            documentation: Current documentation
            critique: Critique to address

        Returns:
            Refined documentation
        """
        file_summaries = "\n".join([
            f"--- File: {f['path']} ---\n{f['content'][:2000]}..."
            for f in self.file_contents
        ])
        prompt = DocumentationTemplates.REFINEMENT_PROMPT.format(
            documentation=documentation,
            critique=critique,
            file_summaries=file_summaries
        )
        return self._call_ollama_with_retry(prompt, operation="refinement")



    def is_critique_positive(self, critique: str) -> bool:
        """
        Check if the critique indicates documentation is satisfactory using semantic analysis.

        Uses semantic understanding and cross-validation to assess critique quality:
        - Analyzes critique content semantically rather than using keyword matching
        - Cross-validates documentation against actual code functionality
        - Combines semantic score with validation issues for final determination

        Args:
            critique: Critique text

        Returns:
            True if critique is positive based on semantic analysis and validation
        """
        # Early exit for explicit positive statements
        explicit_positive = [
            "excellent and requires no changes",
            "perfect and requires no changes",
            "documentation is excellent",
            "documentation is perfect",
            "no changes needed",
            "no improvements necessary",
            "satisfactory as is"
        ]

        critique_lower = critique.lower().strip()
        if any(phrase in critique_lower for phrase in explicit_positive):
            return True

        # Use semantic analysis instead of keyword matching
        semantic_score = self.semantic_analyzer.analyze_critique_semantically(critique)
        
        # Cross-validate documentation if we have it
        validation_issues = []
        if self.documentation and self.documentation_validator:
            validation_issues = self.documentation_validator.validate_documentation(self.documentation)
        
        # Combine semantic analysis with validation results
        final_score = create_semantic_critique_score(semantic_score, validation_issues)
        
        # Log analysis details for debugging
        logger.debug(f"Semantic score breakdown: {semantic_score}")
        logger.debug(f"Validation issues found: {len(validation_issues)}")
        logger.debug(f"Final score: {final_score:.3f} (threshold: {self.config.critique_threshold})")
        
        # Consider critique positive if score meets threshold and no critical errors
        critical_errors = [issue for issue in validation_issues
                          if issue.severity == ValidationResult.ERROR]
        
        return final_score >= self.config.critique_threshold and len(critical_errors) == 0

    def save_documentation(self) -> str:
        """Save the final documentation to file."""
        if self.documentation is None:
            raise DocGeneratorError("No documentation to save")
        
        return save_documentation(
            self.documentation,
            self.output_format,
            self.output_file,
            output_dir=self.directory / "output"
        )

    def _call_ollama_with_retry(self, prompt: str, operation: str = "generation") -> str:
        """
        Call Ollama API with exponential backoff retry logic and caching.

        Args:
            prompt: Prompt to send
            operation: Description of the operation (for logging)

        Returns:
            API response text

        Raises:
            DocGeneratorError: If all retries fail
        """
        # Use utility function for API calls with caching
        return call_ollama_api(
            prompt=prompt,
            model=self.model,
            max_retries=self.config.max_retries,
            retry_delay=self.config.retry_delay,
            api_timeout=self.config.api_timeout,
            use_cache=self.config.enable_caching,
            cache=self.cache if self.cache else None
        )

    def _log_completion_metrics(self, output_path: str, total_time: float):
        """Log completion statistics."""
        logger.info("="*60)
        logger.info("Documentation Generation Complete!")
        logger.info(f"Output file: {output_path}")
        
        if self.documentation:
            logger.info(f"Documentation size: {len(self.documentation):,} characters")
        
        logger.info(f"Total time: {total_time:.2f}s")
        logger.info(f"Files analyzed: {len(self.file_contents)}")
        logger.info(f"Iterations: {len(self.iteration_metrics)}")
        logger.info(f"Caching: {'enabled' if self.config.enable_caching else 'disabled'}")

        for metric in self.iteration_metrics:
            logger.info(
                f"  Iteration {metric['iteration']}: "
                f"{metric['time']:.2f}s, "
                f"{metric['doc_length']:,} chars"
            )
        logger.info("="*60)

    def clear_cache(self):
        """Clear the response cache."""
        if self.cache:
            self.cache.clear()
            logger.info("Cache cleared successfully")
        else:
            logger.info("Caching is disabled")


def main() -> int:
    """Main entry point for the AI agent."""
    # Detect if running as executable or script
    script_name = os.path.basename(sys.argv[0])
    if script_name.endswith('.exe'):
        cmd = 'ai-doc-agent.exe'
    else:
        cmd = 'python ai_agent.py'
    
    parser = argparse.ArgumentParser(
        description="AI agent to generate and refine documentation for code projects.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  {cmd}
  {cmd} --directory ./my-project --format html
  {cmd} --max-files 50 --iterations 5
  {cmd} --model llama2:7b --output my_docs
        """
    )
    
    parser.add_argument(
        "--model", 
        default=MODEL_NAME, 
        help=f"Ollama model (default: {MODEL_NAME})"
    )
    parser.add_argument(
        "--format", 
        default="markdown", 
        choices=["markdown", "html", "pdf"], 
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--output", 
        help="Output filename (without extension)"
    )
    parser.add_argument(
        "--max-files", 
        type=int, 
        default=30, 
        help="Maximum files to analyze (default: 30)"
    )
    parser.add_argument(
        "--directory", 
        help="Directory to analyze (default: current directory)"
    )
    parser.add_argument(
        "--project-type", 
        choices=["frontend", "backend", "mixed"], 
        help="Project type (default: auto-detect)"
    )
    parser.add_argument(
        "--iterations", 
        type=int, 
        default=3, 
        help="Max refinement iterations (default: 3)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    directory = args.directory or str(Path.cwd())

    # Config is created automatically in AIAgent if not provided
    agent = AIAgent(
        directory=directory,
        max_files=args.max_files,
        model=args.model,
        project_type=args.project_type,
        output_format=args.format,
        output_file=args.output
    )

    return agent.run(max_iterations=args.iterations)


if __name__ == "__main__":
    sys.exit(main())
