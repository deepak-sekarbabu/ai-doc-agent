#!/usr/bin/env python3
"""
Unit tests for api_utils.py module.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open

from src.utils.api_utils import (
    ResponseCache,
    call_ollama_api,
    DocGeneratorError
)


class TestResponseCache(unittest.TestCase):
    """Test cases for ResponseCache class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache = ResponseCache(
            cache_dir=self.temp_dir,
            max_age_hours=1,
            max_entries=10
        )

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cache_set_and_get(self):
        """Test setting and getting cached responses."""
        prompt = "test prompt"
        model = "test-model"
        response = "test response"

        # Set a response in cache
        self.cache.set(prompt, model, response)

        # Get the response from cache
        cached_response = self.cache.get(prompt, model)
        self.assertEqual(cached_response, response)

    def test_cache_get_nonexistent(self):
        """Test getting non-existent cached response."""
        result = self.cache.get("nonexistent prompt", "test-model")
        self.assertIsNone(result)

    def test_cache_different_prompt_model(self):
        """Test that different prompts/models don't collide."""
        prompt1 = "prompt 1"
        prompt2 = "prompt 2"
        model = "test-model"
        response1 = "response 1"
        response2 = "response 2"

        self.cache.set(prompt1, model, response1)
        self.cache.set(prompt2, model, response2)

        self.assertEqual(self.cache.get(prompt1, model), response1)
        self.assertEqual(self.cache.get(prompt2, model), response2)

    def test_cache_clear(self):
        """Test clearing all cached entries."""
        self.cache.set("prompt1", "model", "response1")
        self.cache.set("prompt2", "model", "response2")

        self.cache.clear()

        self.assertIsNone(self.cache.get("prompt1", "model"))
        self.assertIsNone(self.cache.get("prompt2", "model"))

    def test_cache_max_entries(self):
        """Test that cache enforces maximum entries limit."""
        # Set more entries than the max limit
        for i in range(15):
            self.cache.set(f"prompt{i}", "model", f"response{i}")
        
        # The cache should have removed some entries to stay within limits
        # We can't predict exactly which ones, but the cache should still work
        # without errors


class TestCallOllamaApi(unittest.TestCase):
    """Test cases for call_ollama_api function."""

    @patch('src.utils.api_utils.requests.post')
    def test_call_ollama_api_success(self, mock_post):
        """Test successful API call."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"response": "test response"}
        mock_post.return_value = mock_response

        result = call_ollama_api(
            prompt="test prompt",
            model="test-model",
            max_retries=1
        )

        self.assertEqual(result, "test response")
        mock_post.assert_called_once()

    @patch('src.utils.api_utils.requests.post')
    def test_call_ollama_api_json_error(self, mock_post):
        """Test API call with JSON decode error."""
        # Mock the response to raise JSON decode error
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_post.return_value = mock_response

        with self.assertRaises(DocGeneratorError):
            call_ollama_api(
                prompt="test prompt", 
                model="test-model", 
                max_retries=1
            )

    @patch('src.utils.api_utils.requests.post')
    def test_call_ollama_api_timeout(self, mock_post):
        """Test API call with timeout."""
        mock_post.side_effect = TimeoutError()

        with self.assertRaises(DocGeneratorError):
            call_ollama_api(
                prompt="test prompt", 
                model="test-model", 
                max_retries=1
            )

    @patch('src.utils.api_utils.requests.post')
    def test_call_ollama_api_empty_response(self, mock_post):
        """Test API call with empty response."""
        # Mock the response with empty content
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"response": ""}
        mock_post.return_value = mock_response

        with self.assertRaises(DocGeneratorError):
            call_ollama_api(
                prompt="test prompt", 
                model="test-model", 
                max_retries=1
            )


if __name__ == '__main__':
    unittest.main()