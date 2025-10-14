# Patent Partners Assistant - System Architecture

## Overview

The Patent Partners Assistant is designed as a modular, offline-first system that processes patent data locally to provide search, analysis, and document generation capabilities.

## System Components

### 1. Data Layer
- **SQLite Database**: Stores patent metadata, text content, and chunks
- **File Storage**: Raw XML files and processed data
- **Search Indexes**: BM25 (pytantivy) and vector (FAISS) indexes

### 2. Processing Layer
- **XML Parser**: Extracts patent data from USPTO XML files
- **Text Chunker**: Splits documents into searchable chunks
- **Embedding Generator**: Creates vector representations for semantic search

### 3. Search Layer
- **BM25 Search**: Keyword-based relevance scoring
- **Vector Search**: Semantic similarity using embeddings
- **Hybrid Fusion**: Combines both search methods with z-score normalization

### 4. Generation Layer
- **LLM Integration**: Local Ollama + Llama 2 7B model
- **Citation System**: Ensures proper patent references
- **Document Export**: Generates DOCX files for legal use

### 5. API Layer
- **FastAPI Server**: RESTful endpoints for all operations
- **Request/Response Models**: Pydantic validation
- **Error Handling**: Comprehensive error management

### 6. UI Layer
- **Streamlit Interface**: User-friendly web interface
- **Tab Navigation**: Organized workflow for different tasks
- **Export Integration**: Direct document download

## Data Flow

```
USPTO XML → Parser → SQLite → Chunking → Indexing → Search → Generation → Export
```

## Database Schema

```sql
-- Core patent information
CREATE TABLE patents (
    id INTEGER PRIMARY KEY,
    patent_id TEXT UNIQUE,
    title TEXT,
    abstract TEXT,
    publication_date DATE,
    cpc_class TEXT,
    inventor TEXT,
    assignee TEXT
);

-- Document sections
CREATE TABLE doc_text (
    id INTEGER PRIMARY KEY,
    patent_id TEXT,
    section TEXT,
    content TEXT,
    char_start INTEGER,
    char_end INTEGER
);

-- Searchable chunks
CREATE TABLE chunks (
    id INTEGER PRIMARY KEY,
    patent_id TEXT,
    section TEXT,
    chunk_text TEXT,
    char_start INTEGER,
    char_end INTEGER,
    token_count INTEGER
);
```

## Security & Privacy

- **Offline Operation**: No external API calls when `OFFLINE=true`
- **Local Processing**: All data remains on the user's machine
- **Audit Logging**: Complete operation traceability
- **Data Encryption**: Optional encryption for sensitive data
