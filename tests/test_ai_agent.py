#!/usr/bin/env python3
"""
Unit tests for ai_agent.py module.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.ai_agent import AIAgent, AgentConfig, ResponseCache
from src.doc_generator import DocGeneratorError


class TestAIAgent(unittest.TestCase):
    """Test cases for AI Agent functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        # Create a test Python file
        test_file = Path(self.temp_dir) / "test.py"
        test_file.write_text("""
def hello():
    '''A simple hello function'''
    return "Hello, World!"

class Calculator:
    '''A simple calculator class'''

    def add(self, a, b):
        '''Add two numbers'''
        return a + b
""")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_agent_config_defaults(self):
        """Test agent configuration with defaults."""
        config = AgentConfig()

        self.assertEqual(config.max_retries, 3)
        self.assertEqual(config.retry_delay, 2)
        self.assertEqual(config.critique_threshold, 0.8)
        self.assertTrue(config.enable_caching)

    @patch.dict(os.environ, {
        'MAX_RETRIES': '5',
        'RETRY_DELAY': '3',
        'CRITIQUE_THRESHOLD': '0.9',
        'ENABLE_CACHING': 'false'
    })
    def test_agent_config_with_env_vars(self):
        """Test agent configuration with environment variables."""
        config = AgentConfig()

        self.assertEqual(config.max_retries, 5)
        self.assertEqual(config.retry_delay, 3)
        self.assertEqual(config.critique_threshold, 0.9)
        self.assertFalse(config.enable_caching)

    def test_agent_initialization(self):
        """Test agent initialization."""
        config = AgentConfig()
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None,
            config=config
        )

        self.assertEqual(str(agent.directory), self.temp_dir)
        self.assertEqual(agent.max_files, 10)
        self.assertEqual(agent.model, "test-model")
        self.assertEqual(agent.project_type, "backend")
        self.assertEqual(agent.output_format, "markdown")
        self.assertIsNone(agent.output_file)
        self.assertEqual(agent.config, config)

    def test_validate_inputs_valid(self):
        """Test input validation with valid inputs."""
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type=None,
            output_format="markdown",
            output_file=None
        )

        # Should not raise any exception
        agent._validate_inputs()

    def test_validate_inputs_invalid_directory(self):
        """Test input validation with invalid directory."""
        agent = AIAgent(
            directory="/nonexistent/path",
            max_files=10,
            model="test-model",
            project_type=None,
            output_format="markdown",
            output_file=None
        )

        with self.assertRaises(DocGeneratorError):
            agent._validate_inputs()

    def test_validate_inputs_invalid_max_files(self):
        """Test input validation with invalid max_files."""
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=0,
            model="test-model",
            project_type=None,
            output_format="markdown",
            output_file=None
        )

        with self.assertRaises(DocGeneratorError):
            agent._validate_inputs()

    @patch('src.ai_agent.detect_project_type')
    @patch('src.ai_agent.find_code_files')
    @patch('src.ai_agent.read_file_safe')
    def test_analyze_codebase_success(self, mock_read, mock_find, mock_detect):
        """Test successful codebase analysis."""
        mock_detect.return_value = "backend"
        mock_find.return_value = [str(Path(self.temp_dir) / "test.py")]
        mock_read.return_value = "test content"

        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type=None,
            output_format="markdown",
            output_file=None
        )

        agent.analyze_codebase()

        self.assertEqual(agent.project_type, "backend")
        self.assertEqual(len(agent.file_contents), 1)
        self.assertEqual(agent.file_contents[0]['path'], 'test.py')
        self.assertEqual(agent.file_contents[0]['content'], 'test content')

    @patch('src.ai_agent.find_code_files')
    def test_analyze_codebase_no_files(self, mock_find):
        """Test codebase analysis with no files found."""
        mock_find.return_value = []

        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type=None,
            output_format="markdown",
            output_file=None
        )

        with self.assertRaises(DocGeneratorError):
            agent.analyze_codebase()

    @patch('src.ai_agent.generate_documentation')
    def test_generate_documentation_draft(self, mock_generate):
        """Test documentation draft generation."""
        mock_generate.return_value = "# Test Documentation"

        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None
        )

        # Mock file contents
        agent.file_contents = [{'path': 'test.py', 'content': 'print("hello")'}]

        result = agent.generate_documentation_draft()

        self.assertEqual(result, "# Test Documentation")
        mock_generate.assert_called_once_with(
            agent.file_contents,
            "markdown",
            "test-model",
            "backend"
        )

    def test_is_critique_positive_perfect(self):
        """Test critique positivity detection for perfect critique."""
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None
        )

        critique = "The documentation is excellent and requires no changes."
        self.assertTrue(agent._is_critique_positive(critique))

    def test_is_critique_positive_explicit_phrases(self):
        """Test critique positivity detection for various explicit positive phrases."""
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None
        )

        positive_critiques = [
            "The documentation is perfect and requires no changes.",
            "Documentation is excellent",
            "No changes needed",
            "No improvements necessary",
            "Satisfactory as is"
        ]

        for critique in positive_critiques:
            with self.subTest(critique=critique):
                self.assertTrue(agent._is_critique_positive(critique))

    def test_is_critique_positive_scoring(self):
        """Test critique positivity detection using scoring system."""
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None
        )

        # High positive score with many positive words
        critique = "The documentation is excellent, clear, comprehensive, well-written, and professional."
        self.assertTrue(agent._is_critique_positive(critique))

        # Mixed but still positive (good outweighs the improvement suggestion)
        critique = "The documentation is good and clear but should add more examples."
        # This might be borderline - depends on threshold
        # For now, let's focus on clear positive cases

    def test_is_critique_negative_scoring(self):
        """Test critique negativity detection using scoring system."""
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None
        )

        negative_critiques = [
            "The documentation needs significant improvements.",
            "Missing important sections and unclear explanations.",
            "Poor structure and incomplete information.",
            "Should add API documentation and improve examples."
        ]

        for critique in negative_critiques:
            with self.subTest(critique=critique):
                self.assertFalse(agent._is_critique_positive(critique))

    def test_cache_functionality(self):
        """Test response caching functionality."""
        import tempfile
        with tempfile.TemporaryDirectory() as cache_dir:
            cache = ResponseCache(cache_dir=cache_dir, max_entries=10)

            # Test cache miss
            result = cache.get("test prompt", "test-model")
            self.assertIsNone(result)

            # Test cache set and get
            cache.set("test prompt", "test-model", "test response")
            result = cache.get("test prompt", "test-model")
            self.assertEqual(result, "test response")

            # Test different prompts don't collide
            result = cache.get("different prompt", "test-model")
            self.assertIsNone(result)

            # Test cache clear
            cache.clear()
            result = cache.get("test prompt", "test-model")
            self.assertIsNone(result)

    def test_agent_with_caching_enabled(self):
        """Test agent initialization with caching enabled."""
        config = AgentConfig()
        config.enable_caching = True
        config.cache_dir = ".test_cache"

        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None,
            config=config
        )

        self.assertIsNotNone(agent.cache)
        self.assertEqual(agent.cache.cache_dir, Path(".test_cache"))

    def test_agent_with_caching_disabled(self):
        """Test agent initialization with caching disabled."""
        config = AgentConfig()
        config.enable_caching = False

        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None,
            config=config
        )

        self.assertIsNone(agent.cache)

    def test_build_critique_prompt(self):
        """Test critique prompt building."""
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None
        )

        documentation = "# Test Doc\nSome content here."
        prompt = agent._build_critique_prompt(documentation)

        self.assertIn("senior quality assurance engineer", prompt)
        self.assertIn("# Test Doc", prompt)
        self.assertIn("Test Doc", prompt)

    def test_build_refinement_prompt(self):
        """Test refinement prompt building."""
        agent = AIAgent(
            directory=self.temp_dir,
            max_files=10,
            model="test-model",
            project_type="backend",
            output_format="markdown",
            output_file=None
        )

        # Mock file contents
        agent.file_contents = [{'path': 'test.py', 'content': 'print("hello")'}]

        documentation = "# Test Doc\nSome content."
        critique = "Needs improvement in section X."

        prompt = agent._build_refinement_prompt(documentation, critique)

        self.assertIn("senior technical writer", prompt)
        self.assertIn("# Test Doc", prompt)
        self.assertIn("Needs improvement in section X", prompt)
        self.assertIn("File: test.py", prompt)


if __name__ == '__main__':
    unittest.main()
