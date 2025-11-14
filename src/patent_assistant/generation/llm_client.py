"""
LLM Client for Ollama Integration.

Provides a wrapper around Ollama for patent document generation.
"""

import time
from typing import Optional, Dict, Any
import subprocess
import json
import requests
from loguru import logger


class OllamaClient:
    """Client for interacting with local Ollama server."""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral:latest"):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama server URL
            model: Model name to use
        """
        self.base_url = base_url
        self.model = model
        logger.info(f"Initialized Ollama client with model: {model}")
    
    def check_health(self) -> bool:
        """
        Check if Ollama server is running and model is available.
        
        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            # Check if server is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                logger.error(f"Ollama server returned status {response.status_code}")
                return False
            
            # Check if model is available
            models = response.json().get("models", [])
            model_names = [m.get("name", "") for m in models]
            
            if self.model not in model_names:
                logger.warning(f"Model {self.model} not found. Available: {model_names}")
                return False
            
            logger.info("Ollama health check passed")
            return True
            
        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Ollama server. Is it running?")
            return False
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stop_sequences: Optional[list] = None,
        timeout: int = 300,  # 5 minutes default timeout
    ) -> Dict[str, Any]:
        """
        Generate text using Ollama.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            stop_sequences: Stop generation at these sequences
            timeout: Request timeout in seconds (default 300)
        
        Returns:
            Dict with 'text', 'tokens', 'time_ms'
        
        Raises:
            RuntimeError: If generation fails
        """
        start_time = time.time()
        
        try:
            # Prepare request
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            if stop_sequences:
                payload["options"]["stop"] = stop_sequences
            
            # Make request
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=timeout
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"Ollama returned status {response.status_code}: {response.text}")
            
            result = response.json()
            generated_text = result.get("response", "")
            
            elapsed_ms = (time.time() - start_time) * 1000
            
            logger.info(f"Generated {len(generated_text)} chars in {elapsed_ms:.0f}ms")
            
            return {
                "text": generated_text,
                "tokens": result.get("eval_count", 0),
                "time_ms": elapsed_ms,
                "model": self.model,
            }
            
        except requests.exceptions.Timeout:
            raise RuntimeError("Ollama request timed out after 2 minutes")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Could not connect to Ollama. Is the server running?")
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise RuntimeError(f"Generation failed: {str(e)}")
    
    def generate_with_retry(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        max_retries: int = 3,
        timeout: int = 300,  # 5 minutes default
    ) -> Dict[str, Any]:
        """
        Generate with automatic retry on failure.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Max tokens
            max_retries: Maximum retry attempts
            timeout: Request timeout in seconds (default 300)
        
        Returns:
            Generation result dict
        """
        for attempt in range(max_retries):
            try:
                return self.generate(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=timeout,
                )
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise RuntimeError("All retry attempts exhausted")


# Global client instance
_client: Optional[OllamaClient] = None


def get_ollama_client() -> OllamaClient:
    """Get or create global Ollama client instance."""
    global _client
    if _client is None:
        _client = OllamaClient()
    return _client


def check_ollama_available() -> bool:
    """Check if Ollama is available."""
    client = get_ollama_client()
    return client.check_health()

