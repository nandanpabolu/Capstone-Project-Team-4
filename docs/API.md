# Patent Partners Assistant - API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2024-10-08T10:30:00Z"
}
```

### Search Patents
```http
POST /search
```

**Request Body:**
```json
{
  "query": "machine learning algorithm",
  "top_k": 10,
  "include_abstract": true
}
```

**Response:**
```json
{
  "results": [
    {
      "patent_id": "US12345678",
      "title": "Machine Learning Method",
      "abstract": "A method for...",
      "score": 0.95,
      "sections": ["abstract", "claims"]
    }
  ],
  "total_results": 10,
  "query_time_ms": 150
}
```

### Get RAG Context
```http
POST /rag/context
```

**Request Body:**
```json
{
  "query": "invention description",
  "max_chunks": 24,
  "window_size": 1
}
```

**Response:**
```json
{
  "context": [
    {
      "patent_id": "US12345678",
      "section": "abstract",
      "text": "Context text...",
      "char_start": 100,
      "char_end": 200,
      "score": 0.92
    }
  ],
  "total_chunks": 24
}
```

### Generate Invention Memo
```http
POST /generate/memo
```

**Request Body:**
```json
{
  "invention_description": "My invention is...",
  "context_chunks": [...],
  "include_citations": true
}
```

**Response:**
```json
{
  "memo": "Generated memo text with citations...",
  "citations": [
    {
      "patent_id": "US12345678",
      "section": "abstract",
      "char_start": 100,
      "char_end": 200
    }
  ],
  "generation_time_ms": 5000
}
```

### Generate Patent Draft
```http
POST /generate/draft
```

**Request Body:**
```json
{
  "invention_description": "My invention is...",
  "draft_type": "abstract",
  "context_chunks": [...]
}
```

**Response:**
```json
{
  "draft": "Generated draft text...",
  "citations": [...],
  "sections": ["abstract", "summary"],
  "generation_time_ms": 8000
}
```

### Export Document
```http
POST /export/docx
```

**Request Body:**
```json
{
  "content": "Document content...",
  "filename": "patent_draft.docx",
  "sections": ["abstract", "summary", "claims"]
}
```

**Response:**
```json
{
  "file_path": "/exports/patent_draft.docx",
  "file_size": 25600,
  "export_time_ms": 500
}
```

## Error Responses

All endpoints return standard HTTP status codes and error responses:

```json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "timestamp": "2024-10-08T10:30:00Z"
}
```

## Rate Limiting

- No rate limiting for local development
- Production deployment may include rate limiting

## Authentication

- No authentication required for local development
- Production deployment may include API key authentication
