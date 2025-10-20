"""
Patent Draft Generator.

Generates USPTO-formatted patent drafts using LLM.
"""

from typing import List, Dict, Any
from loguru import logger

from .llm_client import get_ollama_client
from .prompts import create_draft_prompt, SYSTEM_PROMPT_DRAFT


def generate_patent_draft(
    invention_description: str,
    prior_art: List[Dict[str, Any]] = None,
    temperature: float = 0.7,
    max_tokens: int = 4000,
) -> Dict[str, Any]:
    """
    Generate a patent draft.
    
    Args:
        invention_description: Description of the invention
        prior_art: List of prior art passages (doc_id, text, score)
        temperature: Generation temperature (0.0-2.0)
        max_tokens: Maximum tokens to generate
    
    Returns:
        Dict with keys: draft_text, sections, citations, generation_time_ms, model_used
    
    Raises:
        RuntimeError: If generation fails
    """
    logger.info(f"Generating patent draft for {len(invention_description)} char description")
    
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
    
    # Create prompt
    prompt = create_draft_prompt(invention_description, prior_art)
    
    logger.debug(f"Prompt length: {len(prompt)} chars")
    
    # Generate draft
    try:
        result = client.generate_with_retry(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPT_DRAFT,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        draft_text = result["text"]
        
        # Parse sections
        sections_dict = parse_draft_sections(draft_text)
        section_names = list(sections_dict.keys())
        
        # Extract citations from prior art
        citations = []
        for passage in prior_art:
            citations.append({
                "patent_id": passage.get("doc_id", "Unknown"),
                "relevance": passage.get("score", 0.0),
                "text_snippet": passage.get("text", "")[:200] + "...",
            })
        
        logger.info(f"Successfully generated draft ({len(draft_text)} chars, {len(section_names)} sections, {len(citations)} citations)")
        
        return {
            "draft_text": draft_text,
            "sections": section_names,
            "sections_dict": sections_dict,
            "citations": citations,
            "generation_time_ms": result["time_ms"],
            "model_used": result["model"],
            "tokens_generated": result["tokens"],
        }
        
    except Exception as e:
        logger.error(f"Draft generation failed: {e}")
        raise RuntimeError(f"Failed to generate patent draft: {str(e)}")


def parse_draft_sections(draft_text: str) -> Dict[str, str]:
    """
    Parse generated draft into structured sections.
    
    Args:
        draft_text: Raw draft text from LLM
    
    Returns:
        Dict mapping section names to content
    """
    sections = {}
    current_section = "preamble"
    current_content = []
    
    for line in draft_text.split("\n"):
        line_stripped = line.strip()
        
        # Check if line is a major section header (##) or minor (###)
        if line_stripped.startswith("##"):
            # Save previous section
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            
            # Start new section
            section_name = line_stripped.strip("#").strip()
            # Normalize section name
            current_section = section_name.lower().replace(" ", "_")
            current_content = []
        else:
            current_content.append(line)
    
    # Save last section
    if current_content:
        sections[current_section] = "\n".join(current_content).strip()
    
    return sections


def format_draft_for_export(draft_text: str, metadata: Dict[str, Any] = None) -> str:
    """
    Format draft with metadata for export.
    
    Args:
        draft_text: Raw draft text
        metadata: Optional metadata (title, inventors, filing date, etc.)
    
    Returns:
        Formatted draft string
    """
    if metadata is None:
        metadata = {}
    
    formatted = []
    
    # Add header if metadata provided
    if metadata:
        formatted.append("=" * 80)
        formatted.append("PATENT APPLICATION DRAFT")
        formatted.append("=" * 80)
        formatted.append("")
        
        if "title" in metadata:
            formatted.append(f"Title: {metadata['title']}")
        if "inventors" in metadata:
            formatted.append(f"Inventors: {', '.join(metadata['inventors'])}")
        if "filing_date" in metadata:
            formatted.append(f"Filing Date: {metadata['filing_date']}")
        
        formatted.append("")
        formatted.append("=" * 80)
        formatted.append("")
    
    # Add draft text
    formatted.append(draft_text)
    
    return "\n".join(formatted)


def extract_claims(draft_text: str) -> List[str]:
    """
    Extract individual claims from draft text.
    
    Args:
        draft_text: Full draft text
    
    Returns:
        List of individual claims
    """
    claims = []
    in_claims_section = False
    current_claim = []
    
    for line in draft_text.split("\n"):
        line_stripped = line.strip()
        
        # Detect claims section
        if "## CLAIMS" in line_stripped.upper() or "## INDEPENDENT CLAIM" in line_stripped.upper():
            in_claims_section = True
            continue
        
        # Detect end of claims section
        if in_claims_section and line_stripped.startswith("##") and "CLAIM" not in line_stripped.upper():
            break
        
        # Extract claims
        if in_claims_section:
            # Check if line starts a new claim (numbered)
            if line_stripped and (line_stripped[0].isdigit() or line_stripped.startswith("Claim")):
                # Save previous claim
                if current_claim:
                    claims.append(" ".join(current_claim))
                current_claim = [line_stripped]
            elif line_stripped:  # Continuation of current claim
                current_claim.append(line_stripped)
    
    # Save last claim
    if current_claim:
        claims.append(" ".join(current_claim))
    
    return claims

