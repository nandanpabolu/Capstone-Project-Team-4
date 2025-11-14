# Patent Partners Assistant - System Architecture

## Overview

The Patent Partners Assistant is a production-ready, offline-first system that uses local LLM technology to assist patent professionals with invention memo and patent draft generation. The architecture prioritizes privacy, type safety, and maintainability.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                    │
│                                                          │
│  ┌──────────────────┐         ┌──────────────────────┐  │
│  │  Streamlit UI    │         │   FastAPI /docs      │  │
│  │  (Port 8501)     │         │   (Interactive)      │  │
│  └──────────────────┘         └──────────────────────┘  │
└────────────────┬─────────────────────────┬───────────────┘
                 │                         │
                 │      HTTP/REST          │
                 ▼                         ▼
┌─────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                    │
│                       (FastAPI)                          │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ /health  │  │ /generate│  │ /export  │             │
│  │ Endpoint │  │ Endpoints│  │ Endpoint │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                          │
│  • Pydantic Validation                                   │
│  • CORS Middleware                                       │
│  • Error Handling                                        │
│  • Logging                                               │
└────────────────┬───────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                 │
│                                                          │
│  ┌──────────────────┐         ┌──────────────────────┐  │
│  │ Memo Generator   │         │ Draft Generator      │  │
│  │                  │         │                      │  │
│  │ • Prompt Select  │         │ • USPTO Format       │  │
│  │ • Mode Config    │         │ • Section Parser     │  │
│  └──────────────────┘         └──────────────────────┘  │
│                                                          │
│  ┌──────────────────┐         ┌──────────────────────┐  │
│  │ LLM Client       │         │ Export Manager       │  │
│  │                  │         │                      │  │
│  │ • Ollama API     │         │ • DOCX Generation    │  │
│  │ • Retry Logic    │         │ • Formatting         │  │
│  └──────────────────┘         └──────────────────────┘  │
└────────────────┬───────────────────────────────────────┘
                 │
                 │      HTTP (Port 11434)
                 ▼
┌─────────────────────────────────────────────────────────┐
│                      INFERENCE LAYER                     │
│                                                          │
│                   Ollama + Mistral-7B                    │
│                   • Local Inference                      │
│                   • No External APIs                     │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Presentation Layer

#### Streamlit UI (`src/patent_assistant/ui/main.py`)

**Purpose**: User-friendly web interface for patent professionals

**Key Features**:
- Tab-based navigation (Memo, Draft, About)
- Real-time generation progress
- API status monitoring
- Parameter configuration
- Document download

**Technology Stack**:
- Streamlit 1.50.0
- streamlit-option-menu for navigation
- requests library for API calls

**User Flow**:
1. User enters invention description
2. Selects generation mode (Fast/Detailed)
3. Adjusts parameters (temperature, tokens)
4. Initiates generation
5. Views progress and results
6. Downloads output

#### Interactive API Documentation

**Purpose**: Developer-friendly API exploration

**Features**:
- Swagger UI at `/docs`
- ReDoc at `/redoc`
- Try-it-out functionality
- Schema visualization
- Example requests/responses

### 2. Application Layer

#### FastAPI Server (`src/patent_assistant/api/main.py`)

**Purpose**: RESTful API providing generation and export services

**Key Components**:

1. **Middleware**:
   - CORS (Cross-Origin Resource Sharing)
   - Request logging
   - Error handling

2. **Endpoints**:
   - `GET /health` - Health check with Ollama status
   - `POST /generate/memo` - Invention memo generation
   - `POST /generate/draft` - Patent draft generation
   - `POST /export/docx` - Document export

3. **Validation**:
   - Pydantic models for all requests
   - Type checking and conversion
   - Business logic validation

4. **Error Handling**:
   - HTTP exception mapping
   - Structured error responses
   - Logging for debugging

**Configuration**:
- Host: 0.0.0.0 (all interfaces)
- Port: 8000
- Workers: 1 (single-threaded for resource management)

### 3. Business Logic Layer

#### Data Models (`src/patent_assistant/models/core.py`)

**Purpose**: Type-safe data structures using Pydantic

**Key Models**:

```python
class GenerateRequest(BaseModel):
    """Request for memo/draft generation"""
    invention_description: str = Field(..., min_length=50, max_length=10000)
    context_chunks: Optional[List[Passage]] = None
    include_citations: bool = True
    max_tokens: int = Field(default=2048, ge=100, le=8000)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

class DraftOut(BaseModel):
    """Response for generated content"""
    draft: str
    generation_time_ms: float
    model_used: str
    citations: List[Citation] = []
    sections: List[str] = []
```

**Benefits**:
- Automatic validation
- API documentation generation
- Type hints for IDEs
- JSON serialization/deserialization

#### Memo Generator (`src/patent_assistant/generation/memo_generator.py`)

**Purpose**: Generate invention disclosure memos

**Features**:
- Two modes: Fast & Concise, Detailed & Comprehensive
- USPTO legal terminology
- Structured sections
- Citation tracking

**Generation Flow**:
1. Validate input parameters
2. Select prompt template based on mode
3. Configure generation parameters:
   - Fast: 1500 tokens, 180s timeout
   - Detailed: 3500 tokens, 360s timeout
4. Call LLM client with retry logic
5. Parse and structure response
6. Return formatted memo

**Sections Generated**:
- Executive Summary
- Invention Overview
- Technical Field
- Prior Art Analysis
- Novelty Assessment
- Patentability Evaluation
- Claims Strategy
- Prosecution Strategy
- Business Considerations

#### Draft Generator (`src/patent_assistant/generation/draft_generator.py`)

**Purpose**: Generate USPTO-compliant patent drafts

**Features**:
- USPTO formatting standards
- Section-based generation
- Independent and dependent claims
- Legal language compliance

**Generation Flow**:
1. Validate invention description
2. Select USPTO-compliant prompt
3. Configure parameters (2000-4500 tokens)
4. Generate comprehensive draft
5. Parse into sections
6. Validate structure
7. Return formatted draft

**Sections Generated**:
- Title
- Abstract
- Technical Field
- Background of Invention
- Summary of Invention
- Detailed Description
- Claims (Independent + Dependent)

#### LLM Client (`src/patent_assistant/generation/llm_client.py`)

**Purpose**: Wrapper for Ollama API with robust error handling

**Key Features**:

1. **Retry Logic**:
   ```python
   max_retries = 3
   backoff_factor = 2
   # Exponential backoff: 2s, 4s, 8s
   ```

2. **Timeout Management**:
   - Fast mode: 180 seconds
   - Detailed mode: 360 seconds
   - Configurable per request

3. **Error Handling**:
   - Connection errors
   - Timeout errors
   - Validation errors
   - Model availability

4. **API Interface**:
   ```python
   def generate(
       prompt: str,
       max_tokens: int = 2048,
       temperature: float = 0.7,
       timeout: int = 300
   ) -> str:
       """Generate text using Ollama"""
   ```

**Ollama Configuration**:
- Base URL: http://localhost:11434
- Model: mistral:latest (7B parameters)
- Context window: 8192 tokens
- Streaming: Disabled (for simplicity)

#### Export Manager (`src/patent_assistant/generation/export.py`)

**Purpose**: Generate professional DOCX documents

**Features**:
- USPTO-compliant formatting
- Section headers and styling
- Proper legal document structure
- Metadata inclusion

**Export Flow**:
1. Parse markdown/text content
2. Create DOCX document
3. Apply formatting:
   - Heading styles
   - Body text
   - Lists
   - Page breaks
4. Add metadata
5. Save to exports directory

### 4. Configuration Layer

#### Settings Management (`config/settings.py`)

**Purpose**: Centralized configuration using Pydantic Settings

**Features**:
- Environment variable support
- Type validation
- Default values
- Directory initialization

**Key Settings**:

```python
class Settings(BaseSettings):
    # Application
    app_name: str = "Patent Partners Assistant"
    app_version: str = "0.1.0"
    debug: bool = True
    
    # LLM
    llm_model: str = "mistral:latest"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2048
    ollama_base_url: str = "http://localhost:11434"
    
    # Paths
    db_path: str = "./data/processed/patents.db"
    export_path: str = "./data/exports/"
    
    # Privacy
    offline: bool = True
```

**Environment Variable Support**:
- `.env` file loading
- Override defaults
- Production/development configs

### 5. Data Layer (Planned)

#### Database Schema (`src/patent_assistant/database/schema.py`)

**Purpose**: SQLite database for patent storage and search (Sprint 2)

**Planned Tables**:

```sql
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

CREATE TABLE chunks (
    id INTEGER PRIMARY KEY,
    patent_id TEXT,
    section TEXT,
    chunk_text TEXT,
    char_start INTEGER,
    char_end INTEGER,
    token_count INTEGER,
    embedding BLOB,
    FOREIGN KEY (patent_id) REFERENCES patents(patent_id)
);
```

**Future Capabilities**:
- USPTO patent ingestion
- Text chunking for search
- Embedding storage
- Citation validation

## Data Flow Diagrams

### Generation Request Flow

```
User Interface
      │
      │ 1. User Input
      ▼
┌──────────────────────┐
│  Streamlit Frontend  │
│                      │
│  • Collect input     │
│  • Validate locally  │
│  • Show progress     │
└──────────┬───────────┘
           │
           │ 2. HTTP POST Request
           │    (JSON payload)
           ▼
┌──────────────────────┐
│   FastAPI Backend    │
│                      │
│  • Pydantic validate │
│  • Log request       │
│  • Route to handler  │
└──────────┬───────────┘
           │
           │ 3. Call Generator
           ▼
┌──────────────────────┐
│  Memo/Draft Gen      │
│                      │
│  • Select prompt     │
│  • Configure params  │
└──────────┬───────────┘
           │
           │ 4. Generate Text
           ▼
┌──────────────────────┐
│    LLM Client        │
│                      │
│  • Format request    │
│  • Call Ollama API   │
│  • Retry if needed   │
└──────────┬───────────┘
           │
           │ 5. HTTP to Ollama
           ▼
┌──────────────────────┐
│   Ollama + Mistral   │
│                      │
│  • Load model        │
│  • Inference         │
│  • Stream tokens     │
└──────────┬───────────┘
           │
           │ 6. Generated Text
           ▼
┌──────────────────────┐
│  Post-Processing     │
│                      │
│  • Parse sections    │
│  • Extract metadata  │
│  • Format response   │
└──────────┬───────────┘
           │
           │ 7. JSON Response
           ▼
┌──────────────────────┐
│  Frontend Display    │
│                      │
│  • Show content      │
│  • Enable download   │
└──────────────────────┘
```

## Technology Decisions

### Why FastAPI?

- **Performance**: Async support, high throughput
- **Modern**: Type hints, automatic docs
- **Developer Experience**: Interactive API testing
- **Validation**: Pydantic integration
- **Standards**: OpenAPI/JSON Schema

### Why Streamlit?

- **Rapid Development**: Quick prototyping
- **Python-Native**: No JavaScript needed
- **Built-in Components**: Forms, progress, tabs
- **State Management**: Session state handling
- **Deployment**: Easy hosting options

### Why Ollama + Mistral?

- **Privacy**: Complete local inference
- **Cost**: No API fees
- **Quality**: Strong 7B model performance
- **Compatibility**: Works on consumer hardware
- **Flexibility**: Easy model swapping

### Why SQLite? (Future)

- **Simplicity**: Serverless, file-based
- **Performance**: Fast for < 1M records
- **Portability**: Single file database
- **Reliability**: ACID compliant
- **Zero-Config**: No server setup

## Security & Privacy

### Privacy Architecture

1. **Offline-First Design**:
   - No external API calls (when OFFLINE=true)
   - All data processing local
   - No telemetry or tracking

2. **Data Isolation**:
   - User data never transmitted
   - Logs stored locally only
   - Optional encryption at rest

3. **Network Security**:
   - CORS restrictions
   - Local-only by default (127.0.0.1)
   - HTTPS ready for production

### Audit & Compliance

1. **Logging**:
   - Request/response logging
   - Generation events tracked
   - Error logging for debugging

2. **Traceability**:
   - Generation timestamps
   - Model versions recorded
   - User actions logged

## Performance Characteristics

### Generation Performance

| Mode | Tokens | Time | Memory |
|------|--------|------|--------|
| Fast | 1500 | 60-90s | ~4GB |
| Detailed | 3500 | 120-180s | ~4GB |

**Factors Affecting Performance**:
- CPU speed (single-threaded)
- RAM availability
- Input length
- Model size

### Optimization Strategies

1. **Model Loading**: Keep model in memory (warm start)
2. **Request Queuing**: Single worker prevents memory overflow
3. **Timeout Management**: Prevent hung requests
4. **Retry Logic**: Handle transient failures

### Scalability Considerations

**Current Limitations**:
- Single worker (sequential processing)
- Local inference only
- No load balancing

**Future Enhancements**:
- Multiple worker processes
- Request queuing system
- Distributed inference (multiple machines)
- GPU acceleration support

## Error Handling Strategy

### Error Categories

1. **Validation Errors** (400/422):
   - Invalid input parameters
   - Missing required fields
   - Type mismatches

2. **Service Errors** (503):
   - Ollama not available
   - Model not loaded
   - Timeout exceeded

3. **Internal Errors** (500):
   - Unexpected exceptions
   - Database errors
   - File system errors

### Error Response Format

```json
{
  "detail": "Human-readable error message",
  "error": "ERROR_CODE",
  "timestamp": "2024-11-14T10:30:00Z"
}
```

### Retry Strategy

```python
# Exponential backoff with jitter
for attempt in range(max_retries):
    try:
        return generate_text()
    except Timeout:
        if attempt < max_retries - 1:
            wait = backoff_factor ** attempt + random()
            sleep(wait)
    except UnrecoverableError:
        raise
```

## Future Architecture Plans

### Sprint 2: Search Integration

```
┌─────────────────────────────────────┐
│      USPTO Patent Database          │
│      (Local SQLite Copy)            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│     Hybrid Search Layer             │
│                                     │
│  ┌──────────┐      ┌─────────────┐ │
│  │   BM25   │      │    FAISS    │ │
│  │ (Keyword)│      │  (Semantic) │ │
│  └──────────┘      └─────────────┘ │
│                                     │
│     Fusion & Re-ranking             │
└──────────────┬──────────────────────┘
               │
               ▼
       Generation Layer
     (with Prior Art Context)
```

### Sprint 3: Advanced Features

- Editable draft interface
- Citation validation
- Comparative analysis
- Figure/drawing support
- Multi-inventor collaboration

## Deployment Architecture

### Development

```
Laptop/Workstation
├── Python Virtual Env
├── Ollama (local)
├── FastAPI (dev server)
└── Streamlit (dev server)
```

### Production (Local Deployment)

```
Server/Workstation
├── Python Production WSGI
├── Ollama (systemd service)
├── Nginx (reverse proxy)
├── FastAPI (gunicorn)
└── Streamlit (production mode)
```

---

**Last Updated**: November 14, 2024  
**Architecture Version**: 1.0 (MVP)  
**Team**: Team 4 - Patent Partners
