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
"""

import os
import sys
import argparse
import logging
import time
import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Union
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from .doc_generator import (
    find_code_files,
    read_file_safe,
    OLLAMA_API_URL,
    MODEL_NAME,
    API_TIMEOUT,
    get_ollama_headers,
    DocGeneratorError,
    save_documentation,
    detect_project_type,
    generate_documentation
)
from .base_agent import BaseAgent, AgentConfig, DocumentationTemplates

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


class ResponseCache:
    """Simple file-based cache for API responses."""

    def __init__(self, cache_dir: str = ".cache", max_age_hours: int = 24, max_entries: int = 100):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.max_age_hours = max_age_hours
        self.max_entries = max_entries

    def _get_cache_key(self, prompt: str, model: str) -> str:
        """Generate cache key from prompt and model."""
        content = f"{model}:{prompt}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get cache file path for a key."""
        return self.cache_dir / f"{cache_key}.json"

    def _clean_expired_entries(self):
        """Remove expired cache entries and enforce max entries limit."""
        try:
            cache_files = list(self.cache_dir.glob("*.json"))
            if len(cache_files) > self.max_entries:
                # Sort by modification time, keep newest
                cache_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
                for old_file in cache_files[self.max_entries:]:
                    old_file.unlink()

            # Remove expired entries
            current_time = time.time()
            max_age_seconds = self.max_age_hours * 3600

            for cache_file in cache_files:
                if current_time - cache_file.stat().st_mtime > max_age_seconds:
                    cache_file.unlink()
        except Exception as e:
            logger.warning(f"Cache cleanup failed: {e}")

    def get(self, prompt: str, model: str) -> Optional[str]:
        """Get cached response for a prompt and model."""
        if not self.cache_dir.exists():
            return None

        cache_key = self._get_cache_key(prompt, model)
        cache_path = self._get_cache_path(cache_key)

        try:
            if cache_path.exists():
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('response')
        except Exception as e:
            logger.warning(f"Cache read failed: {e}")

        return None

    def set(self, prompt: str, model: str, response: str):
        """Cache a response for a prompt and model."""
        try:
            self._clean_expired_entries()

            cache_key = self._get_cache_key(prompt, model)
            cache_path = self._get_cache_path(cache_key)

            data = {
                'prompt': prompt[:200],  # Store truncated prompt for debugging
                'model': model,
                'response': response,
                'timestamp': time.time()
            }

            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.warning(f"Cache write failed: {e}")

    def clear(self):
        """Clear all cached entries."""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
        except Exception as e:
            logger.warning(f"Cache clear failed: {e}")




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
        Use the LLM to critique the documentation.

        Args:
            documentation: Documentation to critique

        Returns:
            Critique text
        """
        prompt = DocumentationTemplates.CRITIQUE_PROMPT.format(documentation=documentation)
        return self._call_ollama_with_retry(prompt, operation="critique")

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
        Check if the critique indicates documentation is satisfactory.

        Uses a scoring system to analyze critique content:
        - Positive indicators increase score
        - Negative indicators decrease score
        - Length and specificity affect final decision

        Args:
            critique: Critique text

        Returns:
            True if critique is positive (score >= threshold)
        """
        critique_lower = critique.lower().strip()

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

        if any(phrase in critique_lower for phrase in explicit_positive):
            return True

        # Scoring system
        score = 0

        # Positive indicators (add points)
        positive_words = [
            "excellent", "perfect", "outstanding", "comprehensive", "well-written",
            "clear", "concise", "accurate", "complete", "thorough", "professional",
            "satisfactory", "good", "great", "fantastic"
        ]

        # Negative indicators (subtract points)
        negative_words = [
            "needs improvement", "requires changes", "missing", "incomplete", "unclear",
            "confusing", "inaccurate", "poor", "lacks", "insufficient", "inadequate",
            "problematic", "issues", "errors", "deficient"
        ]

        # Count positive and negative words
        positive_count = sum(1 for word in positive_words if word in critique_lower)
        negative_count = sum(1 for word in negative_words if word in critique_lower)

        score += positive_count * 2
        score -= negative_count * 3

        # Length analysis - very short critiques are often positive
        if len(critique.strip()) < 50:
            score += 2

        # Check for specific improvement requests
        improvement_phrases = [
            "should add", "consider adding", "recommend adding",
            "needs to include", "missing section", "add section",
            "improve", "enhance", "fix", "correct"
        ]

        improvement_requests = sum(1 for phrase in improvement_phrases if phrase in critique_lower)
        score -= improvement_requests * 2

        # Threshold for positive critique
        threshold = self.config.critique_threshold * 10  # Convert to score scale

        return score >= threshold

    def save_documentation(self) -> str:
        """Save the final documentation to file."""
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
        # Check cache first if enabled
        if self.cache and self.config.enable_caching:
            cached_response = self.cache.get(prompt, self.model)
            if cached_response:
                logger.info(f"Using cached response for {operation}")
                return cached_response

        import requests

        for attempt in range(self.config.max_retries):
            try:
                logger.info(f"Sending {operation} request to Ollama (attempt {attempt + 1})")
                
                response = requests.post(
                    OLLAMA_API_URL,
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                    },
                    headers=get_ollama_headers(),
                    timeout=self.config.api_timeout
                )
                response.raise_for_status()
                
                resp_data = response.json()
                content = resp_data.get("response") or resp_data.get("text", "")
                
                if not content:
                    raise DocGeneratorError("Invalid API response format from Ollama")

                content = content.strip()

                # Cache the response if caching is enabled
                if self.cache and self.config.enable_caching:
                    self.cache.set(prompt, self.model, content)

                logger.info(f"{operation.capitalize()} completed successfully")
                return content
                
            except requests.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (2 ** attempt))
                else:
                    raise DocGeneratorError(f"API timeout after {self.config.max_retries} attempts")
                    
            except requests.RequestException as e:
                logger.error(f"Request failed on attempt {attempt + 1}: {e}")
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (2 ** attempt))
                else:
                    raise DocGeneratorError(f"API request failed after {self.config.max_retries} attempts: {e}")

    def _log_completion_metrics(self, output_path: str, total_time: float):
        """Log completion statistics."""
        logger.info("="*60)
        logger.info("Documentation Generation Complete!")
        logger.info(f"Output file: {output_path}")
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


def main():
    """Main entry point for the AI agent."""
    # Detect if running as executable or script
    import os
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

    sys.exit(agent.run(max_iterations=args.iterations))


if __name__ == "__main__":
    main()
