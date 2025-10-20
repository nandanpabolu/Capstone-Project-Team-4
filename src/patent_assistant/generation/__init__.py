"""LLM integration and document generation."""

from .llm_client import get_ollama_client, check_ollama_available, OllamaClient
from .memo_generator import generate_invention_memo, format_memo_sections
from .draft_generator import generate_patent_draft, parse_draft_sections, extract_claims
from .export import (
    export_to_docx,
    export_memo_to_docx,
    export_draft_to_docx,
    create_docx_document,
    export_memo_to_pdf,
    export_draft_to_pdf,
    create_pdf_document,
)

__all__ = [
    # Client
    "get_ollama_client",
    "check_ollama_available",
    "OllamaClient",
    # Generators
    "generate_invention_memo",
    "format_memo_sections",
    "generate_patent_draft",
    "parse_draft_sections",
    "extract_claims",
    # Export
    "export_to_docx",
    "export_memo_to_docx",
    "export_draft_to_docx",
    "create_docx_document",
    "export_memo_to_pdf",
    "export_draft_to_pdf",
    "create_pdf_document",
]
