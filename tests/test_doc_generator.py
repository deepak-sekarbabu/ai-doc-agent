#!/usr/bin/env python3
"""
Unit tests for doc_generator.py module.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.doc_generator import (
    detect_project_type,
    find_code_files,
    read_file_safe,
    extract_docstrings,
    extract_jsdoc,
    build_prompt,
    save_documentation,
    DocGeneratorError,
    OllamaConnectionError
)


class TestDocGenerator(unittest.TestCase):
    """Test cases for documentation generator functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_detect_project_type_frontend(self):
        """Test frontend project type detection."""
        # Create a frontend project structure
        package_json = Path(self.temp_dir) / "package.json"
        package_json.write_text('{"name": "test", "version": "1.0.0"}')

        result = detect_project_type(self.temp_dir)
        self.assertEqual(result, "frontend")

    def test_detect_project_type_backend(self):
        """Test backend project type detection."""
        # Create a backend project structure
        requirements_txt = Path(self.temp_dir) / "requirements.txt"
        requirements_txt.write_text("flask==2.0.0\n")

        result = detect_project_type(self.temp_dir)
        self.assertEqual(result, "backend")

    def test_detect_project_type_mixed(self):
        """Test mixed project type detection."""
        # Create both frontend and backend indicators
        package_json = Path(self.temp_dir) / "package.json"
        package_json.write_text('{"name": "test", "version": "1.0.0"}')

        requirements_txt = Path(self.temp_dir) / "requirements.txt"
        requirements_txt.write_text("flask==2.0.0\n")

        result = detect_project_type(self.temp_dir)
        self.assertEqual(result, "mixed")

    def test_detect_project_type_unknown(self):
        """Test unknown project type detection."""
        # Empty directory should return mixed
        result = detect_project_type(self.temp_dir)
        self.assertEqual(result, "mixed")

    def test_find_code_files_basic(self):
        """Test basic file discovery."""
        # Create some test files
        py_file = Path(self.temp_dir) / "test.py"
        py_file.write_text("print('hello')")

        js_file = Path(self.temp_dir) / "test.js"
        js_file.write_text("console.log('hello');")

        # Create a non-code file that should be ignored
        txt_file = Path(self.temp_dir) / "readme.txt"
        txt_file.write_text("This is a text file")

        files = find_code_files(self.temp_dir, max_files=10)

        # Should find both code files
        self.assertEqual(len(files), 2)
        self.assertIn(str(py_file), files)
        self.assertIn(str(js_file), files)
        self.assertNotIn(str(txt_file), files)

    def test_find_code_files_with_ignored_directories(self):
        """Test that ignored directories are skipped."""
        # Create files in ignored directories
        node_modules_dir = Path(self.temp_dir) / "node_modules"
        node_modules_dir.mkdir()

        js_file = node_modules_dir / "lib.js"
        js_file.write_text("console.log('ignored');")

        # Create file in regular directory
        valid_js = Path(self.temp_dir) / "app.js"
        valid_js.write_text("console.log('valid');")

        files = find_code_files(self.temp_dir, max_files=10)

        # Should only find the valid file
        self.assertEqual(len(files), 1)
        self.assertIn(str(valid_js), files)
        self.assertNotIn(str(js_file), files)

    def test_read_file_safe_success(self):
        """Test successful file reading."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content)

        result = read_file_safe(str(test_file))
        self.assertEqual(result, test_content)

    def test_read_file_safe_nonexistent(self):
        """Test reading nonexistent file."""
        result = read_file_safe(str(Path(self.temp_dir) / "nonexistent.txt"))
        self.assertIsNone(result)

    def test_extract_docstrings_simple(self):
        """Test docstring extraction."""
        code = '''
def hello():
    """This is a simple function."""
    return "hello"

class MyClass:
    """This is a class docstring."""
    pass
'''
        result = extract_docstrings(code)
        expected = {
            "def hello": "This is a simple function.",
            "class MyClass": "This is a class docstring."
        }
        self.assertEqual(result, expected)

    def test_extract_docstrings_empty(self):
        """Test docstring extraction with no docstrings."""
        code = "print('no docstrings here')"
        result = extract_docstrings(code)
        self.assertEqual(result, {})

    def test_extract_jsdoc_simple(self):
        """Test JSDoc extraction."""
        code = '''
/**
 * This is a function
 * @param {string} name - The name parameter
 * @returns {string} The greeting
 */
function greet(name) {
    return `Hello ${name}`;
}
'''
        result = extract_jsdoc(code)
        expected = {
            "greet": "This is a function\n@param {string} name - The name parameter\n@returns {string} The greeting"
        }
        self.assertEqual(result, expected)

    def test_build_prompt_structure(self):
        """Test prompt building structure."""
        file_summaries = "File: test.py\nprint('hello')"
        docstring_info = "def hello: A test function"

        prompt = build_prompt(file_summaries, docstring_info, "markdown", "backend")

        # Check that key elements are present
        self.assertIn("backend codebase", prompt)
        self.assertIn("File: test.py", prompt)
        self.assertIn("def hello: A test function", prompt)
        self.assertIn("Generate documentation in well-structured Markdown format", prompt)

    def test_save_documentation_markdown(self):
        """Test markdown documentation saving."""
        content = "# Test Documentation\n\nThis is a test."

        # Change to temp directory to avoid conflicts
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('src.doc_generator.Path') as mock_path_class:
                mock_output_dir = mock_path_class.return_value
                mock_output_dir.mkdir = MagicMock()
                mock_output_dir.__truediv__.return_value = mock_path_class.return_value
                mock_path_class.return_value.__str__ = lambda self: f"{temp_dir}/test_docs.md"

                with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
                    result = save_documentation(content, "markdown", "test_docs")

                # Should return a path string
                self.assertIsInstance(result, str)
                self.assertIn("test_docs.md", result)

    def test_save_documentation_invalid_format(self):
        """Test saving with invalid format."""
        content = "Test content"

        # This should not raise an error, but fall back to markdown
        with patch('src.doc_generator.Path') as mock_path_class:
            mock_output_dir = mock_path_class.return_value
            mock_output_dir.mkdir = MagicMock()
            mock_output_dir.__truediv__.return_value = mock_path_class.return_value
            mock_path_class.return_value.__str__ = lambda self: "/tmp/test.md"

            with patch('builtins.open', unittest.mock.mock_open()):
                result = save_documentation(content, "pdf", "test_docs")

            # Should fall back to markdown
            self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
