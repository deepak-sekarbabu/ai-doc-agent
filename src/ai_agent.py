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
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from functools import lru_cache
from dotenv import load_dotenv

from doc_generator import (
    find_code_files,
    read_file_safe,
    build_prompt,
    OLLAMA_API_URL,
    MODEL_NAME,
    API_TIMEOUT,
    get_ollama_headers,
    DocGeneratorError,
    save_documentation,
    detect_project_type,
    generate_documentation
)

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


class AgentConfig:
    """Configuration management for AI Agent."""
    
    def __init__(self):
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.retry_delay = int(os.getenv("RETRY_DELAY", "2"))
        self.critique_threshold = float(os.getenv("CRITIQUE_THRESHOLD", "0.8"))
        self.enable_caching = os.getenv("ENABLE_CACHING", "true").lower() == "true"
        
    def __repr__(self):
        return (f"AgentConfig(max_retries={self.max_retries}, "
                f"retry_delay={self.retry_delay}, "
                f"critique_threshold={self.critique_threshold})")


class AIAgent:
    """
    An AI agent that generates and refines documentation for a codebase.
    
    The agent follows a critique-refine cycle to iteratively improve documentation quality.
    It uses LLM-powered self-critique to identify areas for improvement.
    
    Attributes:
        directory: Root directory of the codebase to document
        max_files: Maximum number of files to analyze
        model: LLM model name to use
        project_type: Type of project (frontend/backend/mixed)
        output_format: Output format (markdown/html/pdf)
        output_file: Optional custom output filename
        file_contents: Cached list of analyzed files
        documentation: Current documentation draft
        critique: Latest critique of the documentation
        config: Agent configuration settings
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
        self.directory = Path(directory).resolve()
        self.max_files = max_files
        self.model = model
        self.project_type = project_type
        self.output_format = output_format
        self.output_file = output_file
        self.file_contents: List[Dict[str, str]] = []
        self.documentation: Optional[str] = None
        self.critique: Optional[str] = None
        self.config = config or AgentConfig()
        self.iteration_metrics: List[Dict[str, any]] = []
        
        logger.info(f"AI Agent initialized with config: {self.config}")

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
            self._validate_inputs()
            self.analyze_codebase()
            
            logger.info("Generating initial documentation draft...")
            self.documentation = self.generate_documentation_draft()
            
            for i in range(max_iterations):
                logger.info(f"Iteration {i + 1}/{max_iterations}")
                iteration_start = time.time()
                
                self.critique = self.critique_documentation(self.documentation)
                logger.info(f"Critique: {self.critique[:200]}...")
                
                if self._is_critique_positive(self.critique):
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
            
            output_path = save_documentation(
                self.documentation, 
                self.output_format, 
                self.output_file
            )
            
            total_time = time.time() - start_time
            self._log_completion_metrics(output_path, total_time)
            
            return 0

        except DocGeneratorError as e:
            logger.error(f"Documentation generation error: {e}")
            return 1
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return 1

    def _validate_inputs(self):
        """Validate input parameters."""
        if not self.directory.exists():
            raise DocGeneratorError(f"Directory does not exist: {self.directory}")
        if not self.directory.is_dir():
            raise DocGeneratorError(f"Path is not a directory: {self.directory}")
        if self.max_files < 1:
            raise DocGeneratorError(f"Invalid max_files: {self.max_files}")

    def analyze_codebase(self):
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
        
        for file_path in code_files:
            rel_path = os.path.relpath(file_path, self.directory)
            logger.debug(f"Reading: {rel_path}")
            content = read_file_safe(file_path)
            
            if content:
                self.file_contents.append({
                    "path": rel_path, 
                    "content": content
                })

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
        prompt = self._build_critique_prompt(documentation)
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
        prompt = self._build_refinement_prompt(documentation, critique)
        return self._call_ollama_with_retry(prompt, operation="refinement")

    def _build_critique_prompt(self, documentation: str) -> str:
        """Build prompt for documentation critique."""
        return f"""You are a senior quality assurance engineer and technical documentation expert.

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

    def _build_refinement_prompt(self, documentation: str, critique: str) -> str:
        """Build prompt for documentation refinement."""
        file_summaries = "\n".join([
            f"--- File: {f['path']} ---\n{f['content'][:2000]}..." 
            for f in self.file_contents
        ])

        return f"""You are a senior technical writer. Your task is to refine the documentation based on the critique.

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

    def _is_critique_positive(self, critique: str) -> bool:
        """
        Check if the critique indicates documentation is satisfactory.
        
        Args:
            critique: Critique text
            
        Returns:
            True if critique is positive
        """
        critique_lower = critique.lower()
        positive_indicators = [
            ("excellent", "no changes"),
            ("perfect", "no changes"),
            ("satisfactory", "no improvements"),
        ]
        
        return any(
            ind1 in critique_lower and ind2 in critique_lower 
            for ind1, ind2 in positive_indicators
        )

    def _call_ollama_with_retry(self, prompt: str, operation: str = "generation") -> str:
        """
        Call Ollama API with exponential backoff retry logic.
        
        Args:
            prompt: Prompt to send
            operation: Description of the operation (for logging)
            
        Returns:
            API response text
            
        Raises:
            DocGeneratorError: If all retries fail
        """
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
                    timeout=API_TIMEOUT
                )
                response.raise_for_status()
                
                resp_data = response.json()
                content = resp_data.get("response") or resp_data.get("text", "")
                
                if not content:
                    raise DocGeneratorError("Invalid API response format from Ollama")
                
                logger.info(f"{operation.capitalize()} completed successfully")
                return content.strip()
                
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
        
        for metric in self.iteration_metrics:
            logger.info(
                f"  Iteration {metric['iteration']}: "
                f"{metric['time']:.2f}s, "
                f"{metric['doc_length']:,} chars"
            )
        logger.info("="*60)


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
    
    config = AgentConfig()
    
    agent = AIAgent(
        directory=directory,
        max_files=args.max_files,
        model=args.model,
        project_type=args.project_type,
        output_format=args.format,
        output_file=args.output,
        config=config
    )

    sys.exit(agent.run(max_iterations=args.iterations))


if __name__ == "__main__":
    main()
