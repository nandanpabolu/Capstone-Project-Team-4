"""
FastAPI main application for Patent Partners Assistant.

Provides RESTful API endpoints for patent search, generation, and export.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import time
import sys
from pathlib import Path
from typing import List

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from ..models.core import (
    SearchRequest,
    GenerateRequest,
    DraftOut,
    HealthResponse,
    ErrorResponse,
    ContextPack,
)
from ..generation import (
    generate_invention_memo,
    generate_patent_draft as gen_draft,
    export_memo_to_docx,
    export_draft_to_docx,
    check_ollama_available,
)
from config.settings import settings
from loguru import logger
import os
import tempfile

# Initialize FastAPI app
app = FastAPI(
    title="Patent Partners Assistant API",
    description="Offline AI-powered patent assistant for search, analysis, and document generation",
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    # Check Ollama availability
    ollama_available = check_ollama_available()
    
    return HealthResponse(
        status="healthy" if ollama_available else "degraded",
        version=settings.app_version,
        offline_mode=settings.is_offline,
    )


@app.post("/search")
async def search_patents(request: SearchRequest):
    """
    Search for relevant patents using hybrid BM25 + vector search.
    
    TODO: Implement actual search logic
    """
    # Placeholder implementation
    return {
        "results": [],
        "total_results": 0,
        "query_time_ms": 0,
        "message": "Search functionality not yet implemented"
    }


@app.post("/rag/context", response_model=ContextPack)
async def get_rag_context(request: SearchRequest):
    """
    Get context passages for RAG (Retrieval-Augmented Generation).
    
    TODO: Implement RAG context retrieval
    """
    # Placeholder implementation
    return ContextPack(
        passages=[],
        total_chunks=0,
        query=request.query,
        retrieval_time_ms=0.0,
    )


@app.post("/generate/memo", response_model=DraftOut)
async def generate_memo_endpoint(request: GenerateRequest):
    """
    Generate an invention memo comparing the invention to prior art.
    """
    try:
        logger.info("Received memo generation request")
        
        # Convert context_chunks to prior_art format if provided
        prior_art = []
        if request.context_chunks:
            for chunk in request.context_chunks:
                prior_art.append({
                    "doc_id": chunk.doc_id,
                    "text": chunk.text,
                    "score": chunk.score,
                })
        
        # Generate memo
        result = generate_invention_memo(
            invention_description=request.invention_description,
            prior_art=prior_art,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            mode=request.mode,
        )
        
        logger.info("Memo generated successfully")
        
        return DraftOut(
            draft=result["memo_text"],
            citations=result["citations"],
            sections=["memo"],
            generation_time_ms=result["generation_time_ms"],
            model_used=result["model_used"],
        )
        
    except Exception as e:
        logger.error(f"Memo generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/draft", response_model=DraftOut)
async def generate_draft_endpoint(request: GenerateRequest):
    """
    Generate a patent draft (abstract, summary, claims).
    """
    try:
        logger.info("Received draft generation request")
        
        # Convert context_chunks to prior_art format if provided
        prior_art = []
        if request.context_chunks:
            for chunk in request.context_chunks:
                prior_art.append({
                    "doc_id": chunk.doc_id,
                    "text": chunk.text,
                    "score": chunk.score,
                })
        
        # Generate draft
        result = gen_draft(
            invention_description=request.invention_description,
            prior_art=prior_art,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            mode=request.mode,
        )
        
        logger.info("Draft generated successfully")
        
        return DraftOut(
            draft=result["draft_text"],
            citations=result["citations"],
            sections=result["sections"],
            generation_time_ms=result["generation_time_ms"],
            model_used=result["model_used"],
        )
        
    except Exception as e:
        logger.error(f"Draft generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/export/docx")
async def export_document(request: dict):
    """
    Export generated content to DOCX format.
    """
    try:
        logger.info("Received DOCX export request")
        
        # Extract required fields
        content = request.get("content")
        doc_type = request.get("type", "memo")  # "memo" or "draft"
        title = request.get("title", "Patent Document")
        citations = request.get("citations", [])
        
        if not content:
            raise HTTPException(status_code=400, detail="Content is required")
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        filename = f"{doc_type}_{int(time.time())}.docx"
        output_path = os.path.join(temp_dir, filename)
        
        # Export based on type
        if doc_type == "memo":
            file_path = export_memo_to_docx(
                memo_text=content,
                citations=citations,
                output_path=output_path,
                invention_title=title,
            )
        else:  # draft
            file_path = export_draft_to_docx(
                draft_text=content,
                citations=citations,
                output_path=output_path,
                patent_title=title,
            )
        
        logger.info(f"Document exported to {file_path}")
        
        # Return file
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"DOCX export failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return ErrorResponse(
        error=str(exc),
        detail="An unexpected error occurred",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
