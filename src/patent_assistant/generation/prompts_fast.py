"""
FAST MODE Prompts - Concise, Quick Generation.

Optimized for speed (~60-90 seconds) with focused output.
Target: 800-1500 words, 1000-1500 tokens
"""

from typing import List, Dict, Any


# ============================================================================
# FAST MODE - Memo Prompt
# ============================================================================

MEMO_PROMPT_FAST = """Generate a focused Invention Disclosure Memo.

INVENTION:
{invention_description}

PRIOR ART:
{prior_art_context}

Create a concise memo with these sections:

## 1. EXECUTIVE SUMMARY
[2-3 sentences: Core innovation, main advantage, recommendation]

## 2. INVENTION OVERVIEW
- **Technical Field:** [Specific domain]
- **Problem Solved:** [What fails in current solutions]
- **Our Solution:** [How we address it]
- **Key Innovations:** 
  • [Feature 1 + why it's novel]
  • [Feature 2 + why it's novel]
  • [Feature 3 + why it's novel]

## 3. PRIOR ART ANALYSIS
[For each reference:]
**{patent_id}:** [What it teaches] → [How we differ] → [Why difference matters]

[If no prior art: "No prior art provided. Recommend search before filing."]

## 4. PATENTABILITY ASSESSMENT
- **Novelty (§ 102):** [Novel/Not Novel] - [Key distinguishing feature]
- **Non-Obviousness (§ 103):** [Strong/Moderate/Weak] - [Why]
- **Subject Matter (§ 101):** [Eligible] - [Practical application]
- **Overall Rating:** [Excellent/Strong/Moderate/Weak]

## 5. CLAIMS STRATEGY
**Independent Claim 1:** "A [system] comprising: [element A], [element B], [element C]..."
[Explain scope in one sentence]

**Dependent Claims (3-5):** [List specific features to claim]

## 6. NEXT STEPS
**Recommendation:** [File provisional/File non-provisional/Wait/Don't file]
**Timeline:** [Immediate/Within 30 days/No rush]
**Key Actions:** [2-3 bullet points]

Format with markdown. Be specific but concise. Target 800-1200 words total."""


# ============================================================================
# FAST MODE - Draft Prompt
# ============================================================================

DRAFT_PROMPT_FAST = """Generate a concise USPTO patent draft.

INVENTION:
{invention_description}

PRIOR ART:
{prior_art_context}

Generate these sections:

## TITLE
[Descriptive title, under 15 words]

## ABSTRACT
[Single paragraph, 100-150 words: what the invention is, how it works, key benefit]

## BACKGROUND

### Field of the Invention
[One paragraph: specific technical field and industry application]

### Description of Related Art
[One paragraph: current solutions, their limitations, and why improvement is needed]

## SUMMARY OF THE INVENTION
[2-3 paragraphs covering:
- What the invention is and how it solves the problem
- Main components or steps
- Key advantages over prior art]

## DETAILED DESCRIPTION

### System Architecture
[Describe overall structure and main components]

### Operation
[Explain how it works with a concrete example]

### Alternative Embodiment
[Briefly describe one variation]

## CLAIMS

### Claim 1
A [system/apparatus] for [achieving result], comprising:

a [first element] configured to [function];

a [second element] operatively coupled to the [first element], configured to [function]; and

a [third element] configured to [function],

wherein [overall system characteristic or result].

### Claim 2
The [system] of claim 1, wherein the [specific element] further comprises [additional feature].

### Claim 3
The [system] of claim 1, wherein the [specific function] includes [implementation detail].

### Claim 4
The [system] of claim 1, further comprising a [additional component] configured to [enhanced function].

### Claim 5
A method for [achieving result], comprising:

[first step with technical detail];

[second step with technical detail]; and

[third step with technical detail],

wherein [result is achieved].

### Claim 6
The method of claim 5, further comprising [additional step].

Use proper USPTO format. Keep concise. Target 1200-1800 words total."""


def get_fast_memo_prompt(invention_description: str, prior_art: List[Dict[str, Any]]) -> str:
    """Get fast mode memo prompt."""
    from .prompts import format_prior_art_context
    prior_art_text = format_prior_art_context(prior_art) if prior_art else "No prior art provided."
    
    return MEMO_PROMPT_FAST.format(
        invention_description=invention_description,
        prior_art_context=prior_art_text,
    )


def get_fast_draft_prompt(invention_description: str, prior_art: List[Dict[str, Any]]) -> str:
    """Get fast mode draft prompt."""
    from .prompts import format_prior_art_context
    prior_art_text = format_prior_art_context(prior_art) if prior_art else "No prior art provided."
    
    return DRAFT_PROMPT_FAST.format(
        invention_description=invention_description,
        prior_art_context=prior_art_text,
    )

