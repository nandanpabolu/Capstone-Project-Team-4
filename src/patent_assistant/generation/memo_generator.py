"""
Invention Memo Generator.

Generates invention disclosure memos using LLM and prior art context.
Supports FAST (concise) and DETAILED (comprehensive) modes.
"""

from typing import List, Dict, Any, Literal
from loguru import logger

from .llm_client import get_ollama_client
from .prompts import create_memo_prompt, SYSTEM_PROMPT_MEMO
from .prompts_fast import get_fast_memo_prompt

GenerationMode = Literal["fast", "detailed"]


def generate_invention_memo(
    invention_description: str,
    prior_art: List[Dict[str, Any]] = None,
    temperature: float = 0.7,
    max_tokens: int = 3000,
    mode: GenerationMode = "fast",
) -> Dict[str, Any]:
    """
    Generate an invention disclosure memo.
    
    Args:
        invention_description: Description of the invention
        prior_art: List of prior art passages (doc_id, text, score)
        temperature: Generation temperature (0.0-2.0)
        max_tokens: Maximum tokens to generate
        mode: "fast" for concise output (~90s) or "detailed" for comprehensive (~180s)
    
    Returns:
        Dict with keys: memo_text, citations, generation_time_ms, model_used, mode
    
    Raises:
        RuntimeError: If generation fails
    """
    logger.info(f"Generating invention memo (mode={mode}) for {len(invention_description)} char description")
    
    # Handle empty prior art
    if prior_art is None:
        prior_art = []
    
    # Get Ollama client
    client = get_ollama_client()
    
    # Check if Ollama is available
    if not client.check_health():
        raise RuntimeError(
            "Ollama is not available. Please ensure:\n"
            "1. Ollama is installed (brew install ollama)\n"
            "2. Ollama service is running (ollama serve)\n"
            "3. Mistral model is pulled (ollama pull mistral:latest)"
        )
    
    # Create prompt based on mode and set appropriate timeout
    if mode == "fast":
        prompt = get_fast_memo_prompt(invention_description, prior_art)
        timeout = 180  # 3 minutes for fast mode
        logger.info("Using FAST mode - concise output (~90s, 3min timeout)")
    else:
        prompt = create_memo_prompt(invention_description, prior_art)
        timeout = 360  # 6 minutes for detailed mode
        logger.info("Using DETAILED mode - comprehensive output (~180s, 6min timeout)")
    
    logger.debug(f"Prompt length: {len(prompt)} chars")
    
    # Generate memo
    try:
        result = client.generate_with_retry(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT_MEMO,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
        )
        
        memo_text = result["text"]
        
        # Extract citations from prior art
        citations = []
        for passage in prior_art:
            citations.append({
                "patent_id": passage.get("doc_id", "Unknown"),
                "relevance": passage.get("score", 0.0),
                "text_snippet": passage.get("text", "")[:200] + "...",  # First 200 chars
            })
        
        logger.info(f"Successfully generated memo ({len(memo_text)} chars, {len(citations)} citations)")
        
        return {
            "memo_text": memo_text,
            "citations": citations,
            "generation_time_ms": result["time_ms"],
            "model_used": result["model"],
            "tokens_generated": result["tokens"],
            "mode": mode,
        }
        
    except Exception as e:
        logger.error(f"Memo generation failed: {e}")
        raise RuntimeError(f"Failed to generate invention memo: {str(e)}")


def format_memo_sections(memo_text: str) -> Dict[str, str]:
    """
    Parse generated memo into structured sections.
    
    Args:
        memo_text: Raw memo text from LLM
    
    Returns:
        Dict mapping section names to content
    """
    sections = {}
    current_section = "preamble"
    current_content = []
    
    for line in memo_text.split("\n"):
        # Check if line is a section header (starts with ##)
        if line.strip().startswith("##"):
            # Save previous section
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            
            # Start new section
            current_section = line.strip("#").strip().lower().replace(" ", "_")
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section] = "\n".join(current_content).strip()
    
    return sections

