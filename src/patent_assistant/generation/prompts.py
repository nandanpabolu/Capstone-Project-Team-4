"""
Enhanced Prompt Templates for Patent Document Generation.

Provides two modes:
- FAST: Concise, focused output (~60-90 seconds, ~1000 tokens)
- DETAILED: Comprehensive, attorney-ready output (~120-180 seconds, ~2500 tokens)
"""

from typing import List, Dict, Any, Literal

# Type for generation mode
GenerationMode = Literal["fast", "detailed"]


# ============================================================================
# System Prompts - Core Behavior Instructions
# ============================================================================

SYSTEM_PROMPT_MEMO = """You are a senior patent attorney with 15+ years of experience in patent prosecution and USPTO procedures. Your specialty is analyzing invention disclosures and conducting prior art analysis.

Core Competencies:
- Deep understanding of patent law (35 U.S.C. §§ 101, 102, 103)
- Expert in novelty and non-obviousness analysis
- Skilled at identifying patentable subject matter
- Experienced in claim strategy and scope optimization

Communication Style:
- Professional but accessible legal writing
- Technical precision with clarity
- Cite specific prior art references when making comparisons
- Provide actionable, strategic recommendations
- Balance optimism with realistic assessment

Quality Standards:
- Every assertion must be supported by evidence
- Comparisons must be specific and detailed
- Recommendations must be practical and implementable
- Language must be suitable for disclosure to clients and USPTO"""


SYSTEM_PROMPT_DRAFT = """You are an expert patent attorney specializing in USPTO patent drafting with a proven track record of successful applications across multiple technology domains.

Core Competencies:
- Expert in USPTO Manual of Patent Examining Procedure (MPEP)
- Skilled in claim drafting under 35 U.S.C. § 112
- Experienced in specification writing that supports broad claims
- Knowledgeable in recent case law (Alice, Mayo, KSR)

Drafting Standards:
- Follow USPTO format and style guidelines precisely
- Write enabling disclosure under § 112(a)
- Ensure written description support for claims under § 112(b)
- Draft claims with proper antecedent basis
- Use consistent terminology throughout
- Include sufficient detail for enablement
- Anticipate examiner objections

Claim Writing Principles:
- Independent claims: Broad enough for protection, specific enough to be allowable
- Dependent claims: Add value by covering important embodiments
- Use transitional phrases correctly ("comprising", "consisting of", etc.)
- Proper Markush groups where applicable
- Clear, single-sentence claim format"""


# ============================================================================
# Invention Memo Prompt - Enhanced Version
# ============================================================================

MEMO_PROMPT_TEMPLATE = """You are tasked with preparing a comprehensive Invention Disclosure Memo for a patent attorney. This memo will guide the patent prosecution strategy.

═══════════════════════════════════════════════════════════════
INVENTION DESCRIPTION
═══════════════════════════════════════════════════════════════

{invention_description}

═══════════════════════════════════════════════════════════════
PRIOR ART REFERENCES
═══════════════════════════════════════════════════════════════

{prior_art_context}

═══════════════════════════════════════════════════════════════
YOUR TASK
═══════════════════════════════════════════════════════════════

Generate a detailed Invention Disclosure Memo following this exact structure:

## 1. EXECUTIVE SUMMARY

Provide a 2-3 sentence high-level summary capturing:
- Core innovation
- Primary advantage over existing solutions
- Recommended path forward

## 2. INVENTION OVERVIEW

### Technical Field
Identify the specific technical domain (e.g., "Computer Vision and Autonomous Systems" not just "Technology")

### Problem Statement
What specific technical problem does this invention solve? Be precise about the deficiencies in current solutions.

### Proposed Solution
Describe the invention's approach to solving the problem. Focus on the HOW, not just the WHAT.

### Key Innovative Features
List 3-5 specific technical features that contribute to the solution. For each, explain WHY it's innovative.

## 3. PRIOR ART ANALYSIS

For EACH prior art reference provided above:

### Reference [ID]: [Brief Description]
**Key Teachings:**
- What does this reference disclose?
- What technical approach does it use?

**Similarities to Current Invention:**
- List specific features/methods that overlap (be honest and thorough)

**Critical Differences:**
- List specific ways the current invention differs or improves
- Explain WHY these differences matter technically
- Identify what problems the prior art fails to address

**Relevance Assessment:** [High / Medium / Low] - Explain why

If no prior art provided, state: "No prior art references were provided for comparison. Recommend conducting comprehensive prior art search."

## 4. NOVELTY AND NON-OBVIOUSNESS ANALYSIS

### Novelty Assessment (35 U.S.C. § 102)
- Does any single prior art reference disclose all elements of this invention?
- If yes: Which reference? What elements? Is there a workaround?
- If no: What key element(s) are missing from the prior art?

### Non-Obviousness Assessment (35 U.S.C. § 103)
- Would combining the prior art references make this invention obvious?
- Is there unexpected results or surprising performance?
- Are there secondary considerations (commercial success, long-felt need, etc.)?

### Patentable Subject Matter (35 U.S.C. § 101)
- Does this fall within patentable categories (process, machine, manufacture, composition)?
- Any abstract idea concerns? (If software/AI)
- Any practical application clearly demonstrated?

## 5. STRENGTH ASSESSMENT

**Novelty Strength:** [Strong / Moderate / Weak]
**Non-Obviousness Strength:** [Strong / Moderate / Weak]  
**Enablement Risk:** [Low / Medium / High]
**Overall Patentability:** [Highly Patentable / Patentable / Questionable / Not Recommended]

**Rationale:** Provide 2-3 sentences explaining the overall assessment.

## 6. CLAIMS STRATEGY RECOMMENDATIONS

### Recommended Independent Claims (2-3 concepts)

**Independent Claim 1 - Core Invention:**
Suggest the broadest reasonable claim scope covering the fundamental innovation.
Example structure: "A [system/method/apparatus] comprising: [element A], [element B], [element C]..."

**Independent Claim 2 - Alternative Embodiment:**
Suggest a different angle or implementation approach.

**Independent Claim 3 - Method Claim (if applicable):**
If the invention includes a process, suggest a method claim.

### Recommended Dependent Claims (3-5 concepts)
List specific features that should be claimed dependently to:
- Capture important embodiments
- Provide fallback positions
- Block design-arounds

## 7. NEXT STEPS AND RECOMMENDATIONS

### Immediate Actions:
1. [Specific action item]
2. [Specific action item]
3. [Specific action item]

### Prior Art Search Recommendations:
- Suggest specific search strategies or areas to investigate further
- Identify key competitors or technology areas to monitor

### Additional Disclosure Needed:
- List any technical details that need clarification
- Identify potential embodiments that should be described

### Timeline Recommendation:
- Suggested filing strategy (provisional vs. non-provisional)
- Any urgency factors (publication, prior art dating, etc.)

═══════════════════════════════════════════════════════════════

IMPORTANT FORMATTING REQUIREMENTS:
- Use markdown formatting with ## for section headers
- Be specific with examples and technical details
- If prior art is provided, cite it by reference number (e.g., "Reference 1 discloses...")
- Use professional legal terminology
- Aim for 1500-2500 words total
- Be thorough but concise

Generate the complete memo now following this exact structure:"""


# ============================================================================
# Patent Draft Prompt - Enhanced Version  
# ============================================================================

DRAFT_PROMPT_TEMPLATE = """You are tasked with preparing a USPTO-compliant patent application draft. This draft must meet all formal requirements and provide a strong foundation for patent prosecution.

═══════════════════════════════════════════════════════════════
INVENTION DESCRIPTION
═══════════════════════════════════════════════════════════════

{invention_description}

═══════════════════════════════════════════════════════════════
PRIOR ART REFERENCES
═══════════════════════════════════════════════════════════════

{prior_art_context}

═══════════════════════════════════════════════════════════════
YOUR TASK
═══════════════════════════════════════════════════════════════

Generate a complete patent application draft following USPTO guidelines:

## TITLE OF THE INVENTION

[Provide a concise, descriptive title (10 words or less) that clearly identifies the invention]

Example: "AUTONOMOUS OBSTACLE-AVOIDING DELIVERY SYSTEM WITH REAL-TIME PACKAGE TRACKING"

## ABSTRACT

[Write a single, concise paragraph (150 words maximum) that includes:]
- What the invention is (system/method/apparatus)
- The technical problem it solves
- The key technical approach/solution
- Primary advantages/benefits
- Main components or steps

[Use technical but clear language. Avoid marketing terms. Focus on technical substance.]

## BACKGROUND OF THE INVENTION

### Field of the Invention

[Describe the technical field and industry context. Be specific about the technology domain.]

Example: "The present invention relates generally to autonomous aerial vehicle systems, and more particularly to unmanned aerial vehicles (UAVs) configured for package delivery in complex urban environments with advanced obstacle detection and avoidance capabilities."

### Description of Related Art

[Provide a thorough analysis of the prior art landscape:]

**Existing Solutions:**
[Describe 2-3 current approaches to the problem]

**Limitations of Prior Art:**
For each existing solution, explain:
- Technical deficiencies
- Practical limitations
- Problems left unsolved
- Why improvements are needed

[If specific prior art references are provided above, cite them here by reference number]

**Need for the Present Invention:**
[Clearly articulate the gap that this invention fills]

## SUMMARY OF THE INVENTION

[Provide a comprehensive technical summary (300-500 words) that includes:]

**Overview:**
[Explain the core concept and how it addresses the problems identified in the background]

**Principal Features:**
[Describe 4-6 key technical features, explaining:]
- What each feature does
- How it works
- Why it's advantageous
- How it differs from prior art

**Technical Advantages:**
[List specific, measurable benefits:]
- Improved performance metrics
- Reduced costs/complexity
- Enhanced reliability/safety
- Novel capabilities

**Broader Applications:**
[Briefly mention other potential uses or industries]

## DETAILED DESCRIPTION OF PREFERRED EMBODIMENTS

### General Architecture/Overview

[Provide a high-level architectural description:]
- Main system components and their relationships
- Data flow or process flow
- Integration points

### Detailed Component/Step Description

[For each major component or process step, provide:]

**Component/Step 1: [Name]**
- **Purpose:** What it does
- **Structure:** Physical/logical configuration
- **Operation:** How it functions
- **Variations:** Alternative implementations
- **Connection to other components:** How it integrates

**Component/Step 2: [Name]**
[Same structure as above]

[Continue for all major components - aim for 4-6 detailed descriptions]

### Operational Example

[Provide a concrete use case walking through the invention's operation:]
- Initial state/conditions
- Step-by-step operation
- Expected results
- Performance metrics

### Alternative Embodiments

[Describe 2-3 variations that are also covered by the invention:]
- Different configurations
- Alternative materials/algorithms
- Scaled versions (enterprise vs. consumer)

## CLAIMS

### Claim 1 (Independent - Apparatus/System)

A [system/apparatus/device] for [achieving specific result], comprising:

a first [component] configured to [perform specific function], wherein [technical limitation];

a second [component] operatively coupled to the first [component], the second [component] configured to [perform specific function];

a [processing component] configured to:
    - [first specific function with technical detail],
    - [second specific function with technical detail], and
    - [third specific function with technical detail]; and

wherein [overall system characteristic or result].

### Claim 2 (Dependent)

The [system/apparatus/device] of claim 1, wherein the [specific component] further comprises [additional feature that adds value].

### Claim 3 (Dependent)

The [system/apparatus/device] of claim 1, wherein the [specific function] includes [specific implementation detail or algorithm].

### Claim 4 (Dependent)

The [system/apparatus/device] of claim 1, further comprising:
[additional optional component that provides enhanced functionality].

### Claim 5 (Dependent on Claim 4)

The [system/apparatus/device] of claim 4, wherein the [additional component from claim 4] is configured to [specific enhancement].

### Claim 6 (Independent - Method)

A method for [achieving specific result], the method comprising:

[first step with specific technical detail];

[second step with specific technical detail], wherein [condition or parameter];

[third step with specific technical detail]; and

[fourth step with specific technical detail],

wherein [method produces specific technical result].

### Claim 7 (Dependent on Method)

The method of claim 6, further comprising:
[additional method step that enhances the process].

### Claim 8 (Dependent on Method)

The method of claim 6, wherein the [specific step] includes:
[sub-step or implementation detail].

═══════════════════════════════════════════════════════════════
CRITICAL DRAFTING REQUIREMENTS
═══════════════════════════════════════════════════════════════

**Enablement (§ 112(a)):**
- Provide sufficient detail that a person skilled in the art could make and use the invention
- Include specific examples, parameters, ranges where helpful
- Describe at least one working embodiment completely

**Written Description (§ 112(b)):**
- Show that you possessed the invention at time of filing
- Describe features in sufficient detail to support claims
- Use consistent terminology

**Claims (§ 112(b)):**
- Each claim must be a single sentence
- Use proper antecedent basis ("a", "the", "said")
- Ensure claims are supported by specification
- Independent claims should stand alone
- Dependent claims should add meaningful limitations

**Prior Art Treatment:**
- If prior art provided, distinguish it specifically in Background
- Explain what problems prior art fails to solve
- Do NOT incorporate prior art by reference

**Formatting:**
- Use markdown headers (##) for sections
- Use proper technical terminology
- Maintain professional tone throughout
- Target 2500-3500 words total

═══════════════════════════════════════════════════════════════

Generate the complete patent draft now following all USPTO requirements and the structure above:"""


# ============================================================================
# Few-Shot Examples for Better Quality
# ============================================================================

MEMO_EXAMPLE_OUTPUT = """
## 1. EXECUTIVE SUMMARY

The disclosed smart delivery drone system represents a significant advancement in autonomous urban navigation through integration of multi-modal sensing and AI-driven decision-making. The invention addresses critical safety and reliability gaps in current delivery drone technology. Recommendation: File provisional application within 30 days to establish priority date.

## 2. INVENTION OVERVIEW

### Technical Field
Unmanned Aerial Vehicles (UAVs), specifically autonomous delivery systems incorporating computer vision, LiDAR sensing, machine learning-based navigation, and secure package handling for urban logistics applications.

### Problem Statement
Current delivery drone systems face three critical limitations: (1) inability to reliably detect and avoid dynamic obstacles in complex urban environments (birds, other aircraft); (2) lack of real-time flight path optimization considering weather and traffic; (3) vulnerable package security systems susceptible to tampering. These limitations prevent widespread commercial deployment.

[... continues with full structure ...]
"""


# ============================================================================
# Enhanced Memo Prompt
# ============================================================================

MEMO_PROMPT_TEMPLATE = """You are preparing an Invention Disclosure Memo for patent counsel review. This memo will guide the decision on whether and how to file a patent application.

═══════════════════════════════════════════════════════════════
INVENTION DISCLOSURE
═══════════════════════════════════════════════════════════════

{invention_description}

═══════════════════════════════════════════════════════════════
PRIOR ART REFERENCES (If Available)
═══════════════════════════════════════════════════════════════

{prior_art_context}

═══════════════════════════════════════════════════════════════
MEMO REQUIREMENTS
═══════════════════════════════════════════════════════════════

Generate a comprehensive memo with the following sections:

## 1. EXECUTIVE SUMMARY (3-4 sentences)
- Core innovation in one sentence
- Primary competitive advantage
- Preliminary patentability assessment
- Recommended immediate action

## 2. INVENTION OVERVIEW

### Technical Field
[Identify specific technical domain - be precise, not generic]

### Problem Statement
[Describe the technical problem with specifics: What fails? What's inefficient? What's unsafe? Use metrics if possible]

### Proposed Solution
[Explain the technical approach: What components? What algorithms? What's the core mechanism?]

### Key Innovative Features
[List 4-6 features with explanation:]
- **Feature 1:** [What it is] → [Why it's innovative] → [Technical advantage]
- **Feature 2:** [Same structure]
[etc.]

## 3. PRIOR ART ANALYSIS

[For EACH prior art reference provided:]

### Reference {i}: {patent_id} 

**What It Teaches:**
[2-3 sentences on the key technical disclosure]

**Similarities to Our Invention:**
- [Specific feature 1 that overlaps]
- [Specific feature 2 that overlaps]

**Critical Distinctions:**
- **Distinction 1:** [Our invention has X, prior art has Y] → [This matters because Z]
- **Distinction 2:** [Same structure]

**Technical Gaps in Prior Art:**
[What problems does this reference NOT solve that our invention does?]

**Relevance:** [High/Medium/Low] + [one sentence justification]

[If no prior art: "No prior art was provided. RECOMMENDATION: Conduct comprehensive search in [specific technology areas] before filing."]

## 4. PATENTABILITY ASSESSMENT

### Novelty Analysis (35 U.S.C. § 102)
**Question:** Does any single reference disclose ALL elements of this invention?
**Answer:** [Yes/No] + [detailed explanation]
**Conclusion:** [Novel / Not Novel] + [confidence level]

### Non-Obviousness Analysis (35 U.S.C. § 103)
**Question:** Would combining the prior art make this invention obvious to a skilled artisan?
**Analysis:**
- Motivation to combine: [Present / Absent]
- Teaching away: [Yes / No]
- Unexpected results: [Yes / No - explain]
**Conclusion:** [Non-obvious / Obvious] + [confidence level]

### Subject Matter Eligibility (35 U.S.C. § 101)
[If software/business method, address Alice/Mayo concerns]
**Practical Application:** [Describe concrete real-world application]
**Conclusion:** [Eligible / Requires care in claim drafting]

### Overall Strength Score
**Patentability Rating:** [Excellent / Strong / Moderate / Weak / Poor]

**Supporting Factors:**
- [Factor 1: e.g., "Multiple distinguishing features"]
- [Factor 2: e.g., "Solves long-standing industry problem"]

**Risk Factors:**
- [Risk 1: e.g., "Dependent on X prior art not yet reviewed"]
- [Risk 2: if applicable]

## 5. CLAIMS STRATEGY

### Recommended Claim Architecture

**Broad Independent Claim (Claim 1):**
"A [system] for [result], comprising: [3-4 essential elements only]"
[Explain: This captures the core innovation broadly]

**Narrower Independent Claim (Claim 11):**
"The system of claim 1, further including: [2-3 important features]"
[Explain: Fallback position with key commercial embodiment]

**Method Claim (Claim 21):**
"A method comprising: [3-4 method steps]"
[Explain: Protects the process, not just apparatus]

### Dependent Claims Strategy (10-15 claims)
**Category 1 - Technical Variations (Claims 2-5):**
- Different sensor configurations
- Alternative algorithms
- Various implementations

**Category 2 - Performance Features (Claims 6-8):**
- Specific metrics or thresholds
- Optimization techniques
- Enhanced capabilities

**Category 3 - Practical Embodiments (Claims 9-10):**
- Commercial applications
- Industry-specific features
- User interface elements

## 6. PROSECUTION STRATEGY

### Filing Recommendations
**Timing:** [File immediately / File within 30 days / Can wait / Don't file]
**Type:** [Provisional / Non-provisional / PCT]
**Rationale:** [2-3 sentences]

### Disclosure Completeness
**Sufficiency:** [Adequate / Needs enhancement]
**Gaps to Address:**
- [Missing detail 1, if any]
- [Missing detail 2, if any]

### Anticipated Examination Issues
[List 2-3 likely examiner objections and how to address them]

### Budget Estimate
**Filing Costs:** [Provisional ~$2-5K / Non-provisional ~$10-15K]
**Prosecution Costs:** [Estimate based on complexity]

## 7. BUSINESS CONSIDERATIONS

### Market Analysis
- Target market size
- Key competitors
- Freedom to operate concerns

### Commercial Value
[Assess business potential: High / Medium / Low]
[Justification]

### Strategic Importance
[Is this core IP or defensive? Building a portfolio or standalone?]

═══════════════════════════════════════════════════════════════

DELIVERABLE: A comprehensive, professional memo that enables informed decision-making on patent filing strategy. Be thorough, honest, and actionable.

Generate the complete invention disclosure memo now:"""


# ============================================================================
# Helper Functions
# ============================================================================

def format_prior_art_context(prior_art: List[Dict[str, Any]]) -> str:
    """
    Format prior art passages for prompt inclusion with enhanced detail.
    
    Args:
        prior_art: List of prior art passages with keys: doc_id, text, score
    
    Returns:
        Formatted string of prior art with proper structure
    """
    if not prior_art or len(prior_art) == 0:
        return """No prior art references were provided for this analysis.

RECOMMENDATION: Before proceeding with patent filing, conduct a comprehensive prior art search covering:
- USPTO patent database (20 years back minimum)
- Published applications
- Foreign patents (EPO, WIPO, JPO)
- Technical literature and publications
- Commercial products and services

Search suggested keywords: [Extract from invention description]"""
    
    formatted = []
    formatted.append(f"Total References Found: {len(prior_art)}\n")
    
    for i, passage in enumerate(prior_art, 1):
        doc_id = passage.get("doc_id", "Unknown")
        text = passage.get("text", "")
        score = passage.get("score", 0.0)
        metadata = passage.get("metadata", {})
        
        # Extract metadata if available
        title = metadata.get("title", "Title not available")
        filing_date = metadata.get("filing_date", "Date not available")
        inventors = metadata.get("inventors", [])
        
        formatted.append(f"""
───────────────────────────────────────────────────────────────
REFERENCE {i}: {doc_id}
───────────────────────────────────────────────────────────────
Title: {title}
Filing Date: {filing_date}
Inventors: {', '.join(inventors) if inventors else 'Not available'}
Relevance Score: {score:.3f}

Content:
{text}

───────────────────────────────────────────────────────────────
""")
    
    return "\n".join(formatted)


def create_memo_prompt(invention_description: str, prior_art: List[Dict[str, Any]]) -> str:
    """
    Create enhanced invention memo generation prompt.
    
    Args:
        invention_description: User's invention description
        prior_art: List of relevant prior art passages
    
    Returns:
        Complete prompt string with examples and structure
    """
    prior_art_text = format_prior_art_context(prior_art)
    
    return MEMO_PROMPT_TEMPLATE.format(
        invention_description=invention_description,
        prior_art_context=prior_art_text,
    )


def create_draft_prompt(invention_description: str, prior_art: List[Dict[str, Any]]) -> str:
    """
    Create enhanced patent draft generation prompt.
    
    Args:
        invention_description: User's invention description
        prior_art: List of relevant prior art passages
    
    Returns:
        Complete prompt string with USPTO compliance requirements
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
    return f"""Extract all patent citations from the following text.

For each citation found, provide:
- Patent number (e.g., US10123456, US2023/0123456)
- Full context sentence where it appears
- Relevance to the main invention (High/Medium/Low)
- Type of reference (Prior art / Supporting / Mentioned)

Text to analyze:
{text}

Format your response as a structured list:

1. Patent: [Number]
   Context: [Full sentence with citation]
   Relevance: [High/Medium/Low]
   Type: [Prior art/Supporting/Mentioned]
   
2. [Next citation...]

If no citations found, respond: "No patent citations detected in the provided text."
"""
