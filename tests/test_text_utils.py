#!/usr/bin/env python3
"""
Unit tests for text_utils.py module.
"""

import unittest
from src.utils.text_utils import (
    extract_docstrings,
    extract_jsdoc,
    clean_markdown_response
)


class TestTextUtils(unittest.TestCase):
    """Test cases for text utility functions."""

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

    def test_extract_docstrings_complex(self):
        """Test docstring extraction with complex docstring."""
        code = '''
def complex_function(x, y):
    """
    This function does something complex.
    
    Args:
        x: First parameter
        y: Second parameter
        
    Returns:
        Result of the operation
    """
    return x + y
'''
        result = extract_docstrings(code)
        self.assertIn("def complex_function", result)
        self.assertIn("Args:", result["def complex_function"])

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

    def test_extract_jsdoc_empty(self):
        """Test JSDoc extraction with no JSDocs."""
        code = "function simple() { return 1; }"
        result = extract_jsdoc(code)
        self.assertEqual(result, {})

    def test_clean_markdown_response(self):
        """Test cleaning markdown response."""
        response = "Some text ```python\nprint('hello')\n``` and more text"
        cleaned = clean_markdown_response(response)
        # The code block should be removed
        self.assertNotIn("```python", cleaned)
        self.assertNotIn("print('hello')", cleaned)
        self.assertIn("Some text", cleaned)
        self.assertIn("and more text", cleaned)

    def test_clean_markdown_response_no_code_blocks(self):
        """Test cleaning markdown response with no code blocks."""
        response = "Just regular text without code blocks."
        cleaned = clean_markdown_response(response)
        self.assertEqual(response, cleaned)

    def test_clean_markdown_response_multiple_code_blocks(self):
        """Test cleaning markdown response with multiple code blocks."""
        response = "Text ```code1``` more text ```code2``` end"
        cleaned = clean_markdown_response(response)
        self.assertNotIn("```code1```", cleaned)
        self.assertNotIn("```code2```", cleaned)
        self.assertIn("Text", cleaned)
        self.assertIn("more text", cleaned)
        self.assertIn("end", cleaned)


if __name__ == '__main__':
    unittest.main()