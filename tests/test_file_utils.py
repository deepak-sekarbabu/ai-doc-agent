#!/usr/bin/env python3
"""
Unit tests for file_utils.py module.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.utils.file_utils import (
    detect_project_type,
    find_code_files,
    read_file_safe,
    _get_allowed_extensions,
    _get_priority_files
)


class TestFileUtils(unittest.TestCase):
    """Test cases for file utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_get_allowed_extensions_frontend(self):
        """Test getting allowed extensions for frontend project."""
        extensions = _get_allowed_extensions("frontend")
        expected = {".js", ".ts", ".tsx", ".jsx", ".vue", ".svelte", ".html", ".css", ".scss"}
        self.assertEqual(extensions, expected)

    def test_get_allowed_extensions_backend(self):
        """Test getting allowed extensions for backend project."""
        extensions = _get_allowed_extensions("backend")
        expected = {".py", ".java", ".cs", ".go", ".php", ".rb", ".rs", ".c", ".cpp", ".h", ".hpp", ".kt", ".swift", ".sql"}
        self.assertEqual(extensions, expected)

    def test_get_allowed_extensions_mixed(self):
        """Test getting allowed extensions for mixed project."""
        extensions = _get_allowed_extensions("mixed")
        # Should return all supported extensions
        self.assertIn(".py", extensions)
        self.assertIn(".js", extensions)

    def test_get_priority_files_frontend(self):
        """Test getting priority files for frontend project."""
        priority_files = _get_priority_files("frontend")
        self.assertIn("package.json", priority_files)
        self.assertIn("App.tsx", priority_files)

    def test_get_priority_files_backend(self):
        """Test getting priority files for backend project."""
        priority_files = _get_priority_files("backend")
        self.assertIn("requirements.txt", priority_files)
        self.assertIn("pom.xml", priority_files)

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

    def test_read_file_safe_unicode_error(self):
        """Test handling of Unicode decode errors."""
        # Create a binary file that can't be decoded as UTF-8
        test_file = Path(self.temp_dir) / "binary.bin"
        with open(test_file, 'wb') as f:
            f.write(b'\x80\x81\x82')  # Invalid UTF-8 bytes
        
        result = read_file_safe(str(test_file))
        # Should return empty string instead of crashing (due to errors="ignore")
        self.assertEqual(result, "")


if __name__ == '__main__':
    unittest.main()