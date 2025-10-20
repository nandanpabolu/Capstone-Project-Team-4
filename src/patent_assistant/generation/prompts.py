"""
Prompt templates for patent document generation.

Contains prompts for invention memos, patent drafts, and citation extraction.
"""

from typing import List, Dict, Any


# System prompts for different generation tasks

SYSTEM_PROMPT_MEMO = """You are an expert patent attorney assistant. Your role is to analyze invention disclosures and prior art to create comprehensive invention disclosure memos. 

You must:
- Be factual and precise
- Cite specific prior art when making comparisons
- Identify novel aspects clearly
- Provide actionable recommendations
- Use professional legal language"""

SYSTEM_PROMPT_DRAFT = """You are an expert patent attorney specializing in USPTO patent drafting. Your role is to create well-structured patent draft sections.

You must:
- Follow USPTO formatting guidelines
- Write clear, technical language
- Include proper patent claim structure
- Reference prior art appropriately
- Ensure claims are specific and enforceable"""


# Memo generation prompt

MEMO_PROMPT_TEMPLATE = """Based on the following invention description and prior art, generate a comprehensive Invention Disclosure Memo.

# INVENTION DESCRIPTION
{invention_description}

# PRIOR ART CONTEXT
{prior_art_context}

# INSTRUCTIONS
Generate a memo with these sections:

## 1. INVENTION SUMMARY
Provide a concise 2-3 sentence summary of the invention.

## 2. TECHNICAL FIELD
Identify the technical field and industry application.

## 3. PRIOR ART ANALYSIS
For each relevant prior art reference:
- Summarize the key teachings
- Identify similarities to the current invention
- Identify differences from the current invention

## 4. NOVELTY ASSESSMENT
- What makes this invention novel compared to prior art?
- What problems does it solve that prior art doesn't?
- What are the key innovative aspects?

## 5. PATENTABILITY RECOMMENDATION
- Overall assessment (Highly Patentable / Patentable / Questionable / Not Patentable)
- Rationale for assessment
- Suggested next steps

## 6. CLAIMS STRATEGY
- Suggest 2-3 independent claim concepts
- Identify potential dependent claim variations

Generate the memo now:"""


# Patent draft generation prompt

DRAFT_PROMPT_TEMPLATE = """Based on the following invention description and prior art, generate patent draft sections.

# INVENTION DESCRIPTION
{invention_description}

# PRIOR ART CONTEXT
{prior_art_context}

# INSTRUCTIONS
Generate the following patent sections in USPTO format:

## TITLE OF THE INVENTION
[Provide a concise, descriptive title]

## ABSTRACT
[Write a single paragraph (150 words max) summarizing the invention, its purpose, and key features]

## BACKGROUND OF THE INVENTION

### Field of the Invention
[Describe the technical field]

### Description of Related Art
[Summarize relevant prior art and their limitations]

## SUMMARY OF THE INVENTION
[Provide a detailed summary of the invention, explaining how it solves the problems identified in the background, including key features and advantages]

## DETAILED DESCRIPTION OF PREFERRED EMBODIMENTS
[Describe the invention in detail, including:
- Main components/steps
- How they work together
- Variations and alternatives
- Specific examples]

## CLAIMS

### Independent Claim 1
[Write a comprehensive independent claim covering the core invention]

### Dependent Claims 2-5
[Write 4 dependent claims that narrow the invention with additional features]

Generate the draft now:"""


# Citation extraction prompt

CITATION_EXTRACTION_PROMPT = """Extract all patent citations from the following text. For each citation, identify:
- Patent number (e.g., US10123456)
- Context where it was mentioned
- Relevance (highly relevant / somewhat relevant / mentioned)

Text:
{text}

Format as:
Patent: [number]
Context: [brief context]
Relevance: [level]
---"""


def format_prior_art_context(prior_art: List[Dict[str, Any]]) -> str:
    """
    Format prior art passages for prompt inclusion.
    
    Args:
        prior_art: List of prior art passages with keys: doc_id, text, score
    
    Returns:
        Formatted string of prior art
    """
    if not prior_art:
        return "No prior art provided."
    
    formatted = []
    for i, passage in enumerate(prior_art, 1):
        doc_id = passage.get("doc_id", "Unknown")
        text = passage.get("text", "")
        score = passage.get("score", 0.0)
        
        formatted.append(f"""
### Prior Art Reference {i}: {doc_id}
Relevance Score: {score:.2f}

{text}
""")
    
    return "\n".join(formatted)


def create_memo_prompt(invention_description: str, prior_art: List[Dict[str, Any]]) -> str:
    """
    Create invention memo generation prompt.
    
    Args:
        invention_description: User's invention description
        prior_art: List of relevant prior art passages
    
    Returns:
        Complete prompt string
    """
    prior_art_text = format_prior_art_context(prior_art)
    
    return MEMO_PROMPT_TEMPLATE.format(
        invention_description=invention_description,
        prior_art_context=prior_art_text,
    )


def create_draft_prompt(invention_description: str, prior_art: List[Dict[str, Any]]) -> str:
    """
    Create patent draft generation prompt.
    
    Args:
        invention_description: User's invention description
        prior_art: List of relevant prior art passages
    
    Returns:
        Complete prompt string
    """
    prior_art_text = format_prior_art_context(prior_art)
    
    return DRAFT_PROMPT_TEMPLATE.format(
        invention_description=invention_description,
        prior_art_context=prior_art_text,
    )


def create_citation_extraction_prompt(text: str) -> str:
    """
    Create citation extraction prompt.
    
    Args:
        text: Text to extract citations from
    
    Returns:
        Complete prompt string
    """
    return CITATION_EXTRACTION_PROMPT.format(text=text)

