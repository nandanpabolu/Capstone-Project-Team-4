"""
Core Pydantic models for the Patent Partners Assistant.

Defines the data structures used throughout the application.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PatentDocument(BaseModel):
    """Represents a patent document with metadata."""
    
    patent_id: str = Field(..., description="Unique patent identifier")
    title: str = Field(..., description="Patent title")
    abstract: str = Field(..., description="Patent abstract")
    publication_date: Optional[datetime] = Field(None, description="Publication date")
    cpc_class: Optional[str] = Field(None, description="CPC classification")
    inventor: Optional[str] = Field(None, description="Inventor name(s)")
    assignee: Optional[str] = Field(None, description="Assignee organization")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Chunk(BaseModel):
    """Represents a text chunk for search and retrieval."""
    
    id: int = Field(..., description="Unique chunk identifier")
    patent_id: str = Field(..., description="Associated patent ID")
    section: str = Field(..., description="Document section (title, abstract, claims, description)")
    chunk_text: str = Field(..., description="Chunk content")
    char_start: int = Field(..., description="Start character position")
    char_end: int = Field(..., description="End character position")
    token_count: int = Field(..., description="Number of tokens in chunk")
    embedding_id: Optional[int] = Field(None, description="FAISS embedding index")


class Passage(BaseModel):
    """Represents a search result passage with metadata."""
    
    patent_id: str = Field(..., description="Patent identifier")
    section: str = Field(..., description="Document section")
    text: str = Field(..., description="Passage text")
    char_start: int = Field(..., description="Start character position")
    char_end: int = Field(..., description="End character position")
    score: float = Field(..., description="Relevance score")
    title: Optional[str] = Field(None, description="Patent title")
    abstract: Optional[str] = Field(None, description="Patent abstract")


class ContextPack(BaseModel):
    """Represents a collection of passages for RAG context."""
    
    passages: List[Passage] = Field(..., description="List of relevant passages")
    total_chunks: int = Field(..., description="Total number of chunks")
    query: str = Field(..., description="Original search query")
    retrieval_time_ms: Optional[float] = Field(None, description="Retrieval time in milliseconds")


class SearchRequest(BaseModel):
    """Request model for patent search."""
    
    query: str = Field(..., description="Search query", min_length=1, max_length=1000)
    top_k: int = Field(default=10, description="Number of results to return", ge=1, le=100)
    include_abstract: bool = Field(default=True, description="Include abstract in results")
    sections: Optional[List[str]] = Field(None, description="Specific sections to search")
    cpc_filter: Optional[str] = Field(None, description="CPC classification filter")


class GenerateRequest(BaseModel):
    """Request model for document generation."""
    
    invention_description: str = Field(..., description="Description of the invention", min_length=10)
    context_chunks: Optional[List[Passage]] = Field(None, description="Context passages for generation")
    include_citations: bool = Field(default=True, description="Include patent citations")
    max_tokens: int = Field(default=2048, description="Maximum tokens to generate", ge=100, le=4096)
    temperature: float = Field(default=0.7, description="Generation temperature", ge=0.0, le=2.0)
    mode: str = Field(default="fast", description="Generation mode: 'fast' (concise, ~90s) or 'detailed' (comprehensive, ~180s)")


class DraftOut(BaseModel):
    """Output model for generated patent drafts."""
    
    draft: str = Field(..., description="Generated draft content")
    citations: List[Dict[str, Any]] = Field(default_factory=list, description="Patent citations")
    sections: List[str] = Field(default_factory=list, description="Generated sections")
    generation_time_ms: float = Field(..., description="Generation time in milliseconds")
    model_used: str = Field(..., description="LLM model used for generation")


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    offline_mode: bool = Field(..., description="Whether offline mode is enabled")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
