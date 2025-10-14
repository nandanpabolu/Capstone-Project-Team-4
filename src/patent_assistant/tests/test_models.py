"""
Unit tests for Pydantic models.

Tests the core data models used throughout the application.
"""

import pytest
from datetime import datetime
from patent_assistant.models.core import (
    PatentDocument,
    Chunk,
    Passage,
    SearchRequest,
    GenerateRequest,
    DraftOut,
    HealthResponse,
)


class TestPatentDocument:
    """Test PatentDocument model."""
    
    def test_patent_document_creation(self):
        """Test basic patent document creation."""
        patent = PatentDocument(
            patent_id="US12345678",
            title="Test Patent",
            abstract="A test patent for unit testing",
        )
        
        assert patent.patent_id == "US12345678"
        assert patent.title == "Test Patent"
        assert patent.abstract == "A test patent for unit testing"
        assert isinstance(patent.created_at, datetime)


class TestChunk:
    """Test Chunk model."""
    
    def test_chunk_creation(self):
        """Test basic chunk creation."""
        chunk = Chunk(
            id=1,
            patent_id="US12345678",
            section="abstract",
            chunk_text="Test chunk text",
            char_start=0,
            char_end=16,
            token_count=4,
        )
        
        assert chunk.id == 1
        assert chunk.patent_id == "US12345678"
        assert chunk.section == "abstract"
        assert chunk.char_start == 0
        assert chunk.char_end == 16
        assert chunk.token_count == 4


class TestPassage:
    """Test Passage model."""
    
    def test_passage_creation(self):
        """Test basic passage creation."""
        passage = Passage(
            patent_id="US12345678",
            section="abstract",
            text="Test passage text",
            char_start=0,
            char_end=18,
            score=0.95,
        )
        
        assert passage.patent_id == "US12345678"
        assert passage.section == "abstract"
        assert passage.score == 0.95


class TestSearchRequest:
    """Test SearchRequest model."""
    
    def test_search_request_creation(self):
        """Test basic search request creation."""
        request = SearchRequest(
            query="machine learning",
            top_k=10,
        )
        
        assert request.query == "machine learning"
        assert request.top_k == 10
        assert request.include_abstract is True
    
    def test_search_request_validation(self):
        """Test search request validation."""
        # Test empty query
        with pytest.raises(ValueError):
            SearchRequest(query="")
        
        # Test query too long
        with pytest.raises(ValueError):
            SearchRequest(query="x" * 1001)
        
        # Test invalid top_k
        with pytest.raises(ValueError):
            SearchRequest(query="test", top_k=0)


class TestGenerateRequest:
    """Test GenerateRequest model."""
    
    def test_generate_request_creation(self):
        """Test basic generate request creation."""
        request = GenerateRequest(
            invention_description="A new machine learning algorithm",
        )
        
        assert request.invention_description == "A new machine learning algorithm"
        assert request.include_citations is True
        assert request.max_tokens == 2048
        assert request.temperature == 0.7
    
    def test_generate_request_validation(self):
        """Test generate request validation."""
        # Test description too short
        with pytest.raises(ValueError):
            GenerateRequest(invention_description="short")
        
        # Test invalid max_tokens
        with pytest.raises(ValueError):
            GenerateRequest(
                invention_description="A valid description",
                max_tokens=50,
            )


class TestDraftOut:
    """Test DraftOut model."""
    
    def test_draft_out_creation(self):
        """Test basic draft output creation."""
        draft = DraftOut(
            draft="Generated draft content",
            generation_time_ms=1000.0,
            model_used="llama2:7b",
        )
        
        assert draft.draft == "Generated draft content"
        assert draft.generation_time_ms == 1000.0
        assert draft.model_used == "llama2:7b"
        assert draft.citations == []
        assert draft.sections == []


class TestHealthResponse:
    """Test HealthResponse model."""
    
    def test_health_response_creation(self):
        """Test basic health response creation."""
        response = HealthResponse(
            status="healthy",
            version="0.1.0",
            offline_mode=True,
        )
        
        assert response.status == "healthy"
        assert response.version == "0.1.0"
        assert response.offline_mode is True
        assert isinstance(response.timestamp, datetime)
