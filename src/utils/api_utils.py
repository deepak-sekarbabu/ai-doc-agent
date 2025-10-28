"""API utilities for the AI Documentation Agent."""

import os
import logging
import time
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional
import requests

logger = logging.getLogger(__name__)

# Configure Ollama API URL based on mode
OLLAMA_MODE = os.getenv("OLLAMA_MODE", "cloud").lower()
if OLLAMA_MODE == "local":
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
else:
    OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "https://ollama.com/api/generate")

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss:120b-cloud")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "300"))


class DocGeneratorError(Exception):
    """Base exception for documentation generator errors."""
    pass


def get_ollama_headers() -> Dict[str, str]:
    """Build request headers with optional API key authentication."""
    headers = {"Content-Type": "application/json"}
    api_key = os.getenv("OLLAMA_API_KEY")
    
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    return headers


class ResponseCache:
    """
    Simple file-based cache for API responses.
    
    This class provides a file-based caching mechanism to store and retrieve
    API responses, reducing redundant calls to the LLM API and speeding up
    repeated documentation generations.
    """

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
        """
        Remove expired cache entries and enforce max entries limit.
        
        This method cleans up the cache by removing entries that have exceeded
        the maximum age and enforcing the maximum number of entries limit.
        """
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
        """
        Get cached response for a prompt and model.
        
        Args:
            prompt: The original prompt that was sent to the API
            model: The model that was used for the API call
            
        Returns:
            Cached response if found and not expired, None otherwise
        """
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
        """
        Cache a response for a prompt and model.
        
        Args:
            prompt: The original prompt that was sent to the API
            model: The model that was used for the API call
            response: The API response to cache
        """
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


def call_ollama_api(
    prompt: str, 
    model: str, 
    max_retries: int = 3, 
    retry_delay: int = 2, 
    api_timeout: int = 300,
    use_cache: bool = False,
    cache: Optional[ResponseCache] = None
) -> str:
    """
    Call Ollama API with retry logic and optional caching.

    This function handles all API communication with the Ollama service, including
    retry logic with exponential backoff, JSON response parsing, and optional
    response caching.

    Args:
        prompt: The prompt to send to the API
        model: The model to use
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries (seconds)
        api_timeout: API timeout (seconds)
        use_cache: Whether to use caching
        cache: Cache instance if using caching

    Returns:
        API response text

    Raises:
        DocGeneratorError: If all retries fail or response is invalid
    """
    # Check cache first if enabled
    if use_cache and cache:
        cached_response = cache.get(prompt, model)
        if cached_response:
            logger.info("Using cached response")
            return cached_response

    for attempt in range(max_retries):
        try:
            logger.info(f"Sending request to Ollama (attempt {attempt + 1})")
            
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                },
                headers=get_ollama_headers(),
                timeout=api_timeout
            )
            response.raise_for_status()
            
            try:
                resp_data = response.json()
            except ValueError as e:  # JSON decode error
                logger.error(f"Failed to decode JSON response: {e}")
                logger.debug(f"Raw response: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                    continue
                else:
                    raise DocGeneratorError(f"Invalid JSON response from API: {e}")
            
            content = resp_data.get("response") or resp_data.get("text", "")
            
            if not content:
                logger.error(f"Empty response received: {resp_data}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                    continue
                else:
                    raise DocGeneratorError("Invalid API response format from Ollama - no content returned")

            content = content.strip()

            # Cache the response if caching is enabled
            if use_cache and cache:
                cache.set(prompt, model, content)

            logger.info("API call completed successfully")
            return content
            
        except requests.Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
            else:
                raise DocGeneratorError(f"API timeout after {max_retries} attempts")
                
        except requests.RequestException as e:
            logger.error(f"Request failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
            else:
                raise DocGeneratorError(f"API request failed after {max_retries} attempts: {e}")
        except Exception as e:
            logger.error(f"Unexpected error on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))
            else:
                raise DocGeneratorError(f"Unexpected error after {max_retries} attempts: {e}")