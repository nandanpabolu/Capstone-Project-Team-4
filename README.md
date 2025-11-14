# Patent Partners Assistant

**AI-Powered Patent Analysis & Document Generation System**  
*Team 4 - Patent Partners | Capstone Project | Fall 2024*

An offline, privacy-first AI assistant that helps patent attorneys and inventors with invention disclosure memos and patent draft generation using local LLM technology.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.119.0-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Known Limitations](#-known-limitations)
- [Team](#-team)
- [License](#-license)

---

## 🎯 Overview

Patent Partners Assistant is a production-ready system designed to assist patent professionals with:

- **Invention Memo Generation**: Automated creation of comprehensive invention disclosure memos with technical analysis and patentability assessment
- **Patent Draft Generation**: USPTO-compliant patent documents including title, abstract, background, summary, detailed description, and claims
- **Document Export**: Professional DOCX format for legal review and editing
- **Offline Operation**: Complete privacy with local processing - no external API calls or data transmission

### Key Differentiators

- ✅ **100% Offline**: All processing happens locally using Ollama + Mistral-7B
- ✅ **Privacy-First**: No data leaves your machine - ideal for confidential inventions
- ✅ **Cost-Effective**: $0/month operational cost using open-source models
- ✅ **Production-Ready**: Type-safe, tested, and fully documented codebase
- ✅ **Professional Output**: USPTO-compliant formatting and legal terminology

---

## ✨ Features

### Current Features (MVP)

#### ✅ Invention Memo Generation
- Comprehensive invention analysis and documentation
- Technical field assessment
- Prior art considerations
- Patentability evaluation
- Business and prosecution strategy recommendations
- Configurable output length and detail level

#### ✅ Patent Draft Generation
- USPTO-compliant document structure
- Title generation
- Abstract writing
- Background of invention
- Summary of invention
- Detailed description
- Independent and dependent claims
- Section-based output for easy editing

#### ✅ Document Export
- Professional DOCX format
- Proper legal formatting
- Section headers and styling
- Ready for attorney review

#### ✅ Interactive Web UI
- User-friendly Streamlit interface
- Real-time generation status
- Tabbed section viewing
- Download functionality
- API status monitoring

#### ✅ RESTful API
- FastAPI backend
- Auto-generated documentation
- Type-safe request/response models
- Comprehensive error handling
- CORS support for frontend integration

### Planned Features (Sprint 2+)

- 🔄 Prior-art search with USPTO patent database
- 🔄 Hybrid search (BM25 + vector embeddings)
- 🔄 Citation validation and linking
- 🔄 Multi-document comparison
- 🔄 Editable draft interface

---

## 🏗️ Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                             │
│                                                                     │
│  ┌────────────────────────────┐      ┌───────────────────────────┐ │
│  │   Streamlit Web UI         │      │   API Documentation       │ │
│  │   (Port 8501)              │      │   (FastAPI /docs)         │ │
│  │                            │      │                           │ │
│  │  • Invention Memo Page     │      │  • Interactive Swagger    │ │
│  │  • Patent Draft Page       │      │  • Request/Response       │ │
│  │  • Download Manager        │      │  • Schema Viewer          │ │
│  └──────────┬─────────────────┘      └───────────────┬───────────┘ │
│             │                                        │             │
└─────────────┼────────────────────────────────────────┼─────────────┘
              │                                        │
              │          HTTP Requests                 │
              ▼                                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API LAYER (FastAPI)                            │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │   /health    │  │ /generate/   │  │    /export/docx          │ │
│  │   Endpoint   │  │  memo        │  │    Endpoint              │ │
│  └──────────────┘  │  draft       │  └──────────────────────────┘ │
│                    └──────────────┘                               │
│                                                                     │
│  Pydantic Models • Error Handling • CORS • Logging                 │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    GENERATION LAYER                                 │
│                                                                     │
│  ┌────────────────────┐         ┌────────────────────┐            │
│  │  Memo Generator    │         │  Draft Generator   │            │
│  │                    │         │                    │            │
│  │  • Prompts         │         │  • USPTO Format    │            │
│  │  • Fast Mode       │         │  • Section Parser  │            │
│  │  • Detailed Mode   │         │  • Claims Writer   │            │
│  └─────────┬──────────┘         └──────────┬─────────┘            │
│            │                               │                       │
│            └───────────┬───────────────────┘                       │
│                        ▼                                           │
│            ┌──────────────────────┐                                │
│            │   LLM Client         │                                │
│            │   (OllamaClient)     │                                │
│            │                      │                                │
│            │  • Retry Logic       │                                │
│            │  • Timeout Handling  │                                │
│            │  • Stream Support    │                                │
│            └───────────┬──────────┘                                │
└────────────────────────┼───────────────────────────────────────────┘
                         │
                         │  HTTP (Port 11434)
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    LOCAL LLM (Ollama)                               │
│                                                                     │
│               Mistral-7B-Instruct Model                             │
│               • 7 billion parameters                                │
│               • 4.1 GB model size                                   │
│               • Instruction-tuned                                   │
│               • Local inference                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Input (Invention Description)
         │
         ▼
  API Validation (Pydantic)
         │
         ▼
  Generation Layer
    • Select appropriate prompt template
    • Configure generation parameters (tokens, temperature)
    • Add mode-specific instructions
         │
         ▼
  LLM Client
    • Format request for Ollama API
    • Set timeout (3-6 minutes based on mode)
    • Add retry logic (3 attempts)
         │
         ▼
  Ollama (Local)
    • Load Mistral-7B model
    • Generate response (60-180 seconds)
    • Stream tokens back
         │
         ▼
  Post-Processing
    • Parse sections
    • Extract citations
    • Format structure
         │
         ▼
  Response (JSON)
    • Draft text
    • Sections list
    • Generation metadata
    • Citations (if available)
         │
         ▼
  UI Display / DOCX Export
```

### Component Interaction

```
┌───────────────┐
│ config/       │  ← Settings management (Pydantic Settings)
│ settings.py   │     • Environment variables
└───────┬───────┘     • Configuration defaults
        │             • Directory initialization
        ▼
┌───────────────────────────────────────────────────────────┐
│                    src/patent_assistant/                  │
│                                                           │
│  ┌─────────────┐    ┌──────────────┐   ┌──────────────┐ │
│  │   models/   │◄───┤     api/     │──►│ generation/  │ │
│  │   core.py   │    │    main.py   │   │ *.py         │ │
│  │             │    └──────────────┘   └──────┬───────┘ │
│  │ • Requests  │                               │         │
│  │ • Responses │                               │         │
│  │ • Documents │                               ▼         │
│  └─────────────┘                      ┌──────────────┐  │
│                                       │  export.py   │  │
│  ┌─────────────┐                      │              │  │
│  │ database/   │                      │ • DOCX       │  │
│  │ schema.py   │                      │ • Formatting │  │
│  │             │                      └──────────────┘  │
│  │ (Future)    │                                        │
│  └─────────────┘    ┌──────────────┐                   │
│                     │     ui/      │                    │
│  ┌─────────────┐    │   main.py    │                   │
│  │   tests/    │    │              │                    │
│  │ test_*.py   │    │ • Streamlit  │                    │
│  └─────────────┘    │ • UI Logic   │                    │
│                     └──────────────┘                    │
└───────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend Technologies

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.9+ | Primary programming language |
| **FastAPI** | 0.119.0 | High-performance API framework |
| **Pydantic** | Latest | Data validation and settings |
| **Uvicorn** | Latest | ASGI web server |
| **SQLite** | 3.x | Database (planned for search) |

### Frontend Technologies

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Streamlit** | 1.50.0 | Web UI framework |
| **streamlit-option-menu** | Latest | Navigation components |

### AI & Machine Learning

| Technology | Version | Purpose |
|-----------|---------|---------|
| **Ollama** | Latest | Local LLM inference engine |
| **Mistral-7B-Instruct** | 7B params | Text generation model |
| **FAISS** | Latest | Vector search (planned) |
| **BM25 (pytantivy)** | Latest | Keyword search (planned) |

### Document Processing

| Technology | Version | Purpose |
|-----------|---------|---------|
| **python-docx** | Latest | DOCX file generation |
| **lxml** | Latest | XML parsing (for USPTO data) |

### Development Tools

| Technology | Purpose |
|-----------|---------|
| **pytest** | Unit and integration testing |
| **black** | Code formatting |
| **isort** | Import sorting |
| **loguru** | Structured logging |
| **rich** | Terminal formatting |

---

## 📦 Installation

### Prerequisites

Before installation, ensure you have:

- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **Ollama** - [Download](https://ollama.ai/download)
- **8GB+ RAM** (16GB recommended for smooth operation)
- **10GB free disk space** (for model and dependencies)

### Step 1: Clone Repository

```bash
git clone https://github.com/nandanpabolu/Capstone-Project-Team-4.git
cd Capstone-Project-Team-4
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install and Configure Ollama

```bash
# Install Ollama (if not already installed)
# Visit: https://ollama.ai/download

# Pull the Mistral model (4.1 GB download)
ollama pull mistral:latest

# Verify installation
ollama list
```

### Step 5: Initialize Project Structure

```bash
# Create necessary directories and verify setup
make setup
```

### Step 6: Verify Installation

```bash
# Quick verification that all components are working
python -c "import fastapi, streamlit, requests; print('✓ All dependencies installed')"
ollama list | grep mistral && echo "✓ Mistral model installed"
```

---

## 🚀 Usage

### Quick Start

Start both the API and UI servers:

```bash
# Option 1: Use the startup script (recommended)
./start_servers.sh

# Option 2: Use Make commands
make api    # Terminal 1
make ui     # Terminal 2
```

### Manual Server Start

**Terminal 1 - API Server:**
```bash
source venv/bin/activate
uvicorn src.patent_assistant.api.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Streamlit UI:**
```bash
source venv/bin/activate
streamlit run src/patent_assistant/ui/main.py --server.port 8501
```

### Access the Application

- **Streamlit UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Using the UI

#### 1. Generate Invention Memo

1. Open http://localhost:8501
2. Click **"Invention Memo"** tab
3. Enter your invention description (minimum 50 characters)
4. Select generation mode:
   - **Fast & Concise**: 60-90 seconds, ~1500 tokens
   - **Detailed & Comprehensive**: 120-180 seconds, ~3500 tokens
5. Adjust parameters (optional):
   - Temperature: 0.1 (focused) to 1.0 (creative)
   - Max tokens: Output length control
6. Click **"Generate Invention Memo"**
7. Wait for generation (progress shown)
8. Review output in expandable sections
9. Download as text file

#### 2. Generate Patent Draft

1. Click **"Patent Draft"** tab
2. Enter invention description
3. Select mode and adjust parameters
4. Click **"Generate Patent Draft"**
5. View sections in tabs:
   - Full Draft
   - Title
   - Abstract
   - Background
   - Summary
   - Claims
6. Download as text or DOCX

#### 3. Sample Invention Text

Use this sample for testing:

```
A smart delivery drone system that uses advanced computer vision and machine 
learning to navigate obstacles in urban environments. The drone can autonomously 
detect and avoid birds, buildings, power lines, and other aircraft. It uses a 
combination of LIDAR, cameras, and GPS for navigation.

Key features:
- 360-degree obstacle detection using multiple cameras
- AI-powered flight path optimization
- Secure package compartment with biometric verification
- Real-time communication with ground control
- Weather-adaptive flight algorithms
- Automatic battery management and return-to-base
```

### Using the API Directly

#### Health Check

```bash
curl http://localhost:8000/health
```

#### Generate Memo

```bash
curl -X POST http://localhost:8000/generate/memo \
  -H "Content-Type: application/json" \
  -d '{
    "invention_description": "Your invention here...",
    "max_tokens": 2000,
    "temperature": 0.7
  }'
```

#### Generate Draft

```bash
curl -X POST http://localhost:8000/generate/draft \
  -H "Content-Type: application/json" \
  -d '{
    "invention_description": "Your invention here...",
    "max_tokens": 3000,
    "temperature": 0.7
  }'
```

See [API Documentation](#-api-documentation) for complete endpoint details.

---

## 🧪 Testing

### Run All Tests

We provide a comprehensive test runner that checks all system components:

```bash
# Make sure servers are running first
./start_servers.sh

# In another terminal, run tests
python run_tests.py
```

The test runner checks:
- ✅ API health and availability
- ✅ Ollama connection and model status
- ✅ Memo generation functionality
- ✅ Draft generation functionality
- ✅ Document export capability
- ✅ Error handling and validation
- ✅ Unit tests for data models

### Run Specific Test Suites

```bash
# Unit tests only
pytest src/patent_assistant/tests/ -v

# Integration tests only
pytest tests/ -v

# With coverage report
pytest --cov=src/patent_assistant --cov-report=html
```

### Expected Test Output

```
================================================================================
           PATENT PARTNERS ASSISTANT - TEST SUITE
================================================================================

System Test Runner
API Base URL: http://localhost:8000

Testing: API Health Check... ✓ PASS API v0.1.0, Ollama: True
Testing: Unit Tests (Pydantic Models)... ✓ PASS All unit tests passed
Testing: Memo Generation... ✓ PASS 87.3s, 2543 chars
Testing: Patent Draft Generation... ✓ PASS 92.1s, 3821 chars, 6 sections
Testing: Document Export (DOCX)... ✓ PASS Export successful
Testing: Error Handling & Validation... ✓ PASS Validation working

================================================================================
                            TEST SUMMARY
================================================================================
Tests Run:    6
Tests Passed: 6
Tests Failed: 0
Success Rate: 100%

🎉 ALL TESTS PASSED! System is working correctly.
```

### Troubleshooting Test Failures

**If API tests fail:**
```bash
# Check if API is running
curl http://localhost:8000/health

# Restart API
pkill -f uvicorn
uvicorn src.patent_assistant.api.main:app --host 0.0.0.0 --port 8000
```

**If generation tests fail:**
```bash
# Check Ollama status
ollama list

# Pull Mistral model if missing
ollama pull mistral:latest

# Test Ollama directly
ollama run mistral:latest "Hello, test"
```

---

## 📂 Project Structure

```
patent-partners-assistant/
│
├── config/                          # Configuration management
│   └── settings.py                  # Centralized settings (Pydantic)
│
├── data/                            # Data storage
│   ├── raw/                         # Original patent files (future)
│   ├── processed/                   # Processed data and database
│   └── exports/                     # Generated DOCX files
│
├── docs/                            # Documentation
│   ├── API.md                       # API endpoint documentation
│   └── ARCHITECTURE.md              # System architecture details
│
├── indexes/                         # Search indexes (future)
│   ├── bm25/                        # BM25 keyword search
│   └── faiss/                       # Vector embeddings
│
├── logs/                            # Application logs
│   ├── api.log                      # API request logs
│   ├── generation.log               # LLM generation logs
│   └── retrieval.log                # Search logs (future)
│
├── src/patent_assistant/            # Main application code
│   │
│   ├── api/                         # FastAPI backend
│   │   ├── __init__.py
│   │   └── main.py                  # API endpoints and routing
│   │
│   ├── database/                    # Database operations
│   │   ├── __init__.py
│   │   └── schema.py                # SQLite schema definitions
│   │
│   ├── generation/                  # LLM integration
│   │   ├── __init__.py
│   │   ├── llm_client.py            # Ollama client wrapper
│   │   ├── memo_generator.py        # Invention memo generation
│   │   ├── draft_generator.py       # Patent draft generation
│   │   ├── export.py                # DOCX export functionality
│   │   ├── prompts.py               # Detailed mode prompts
│   │   └── prompts_fast.py          # Fast mode prompts
│   │
│   ├── models/                      # Data models
│   │   ├── __init__.py
│   │   └── core.py                  # Pydantic models (requests/responses)
│   │
│   ├── tests/                       # Unit tests
│   │   ├── __init__.py
│   │   └── test_models.py           # Model validation tests
│   │
│   └── ui/                          # Streamlit interface
│       ├── __init__.py
│       └── main.py                  # Web UI implementation
│
├── tests/                           # System integration tests
│   ├── __init__.py
│   └── test_system.py               # End-to-end tests
│
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
├── Makefile                         # Build automation
├── pyproject.toml                   # Project metadata and config
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
├── run_tests.py                     # Comprehensive test runner
└── start_servers.sh                 # Server startup script
```

### Key Directories Explained

- **`config/`**: Centralized configuration using Pydantic Settings. All environment variables and defaults are managed here.
  
- **`src/patent_assistant/`**: Main application package following best practices for Python project structure.

- **`api/`**: FastAPI application with RESTful endpoints, CORS middleware, and error handling.

- **`generation/`**: Core LLM integration. Includes prompt engineering, client wrappers, and generation orchestration.

- **`models/`**: Type-safe data models using Pydantic for request validation, response serialization, and documentation.

- **`ui/`**: Streamlit web interface providing user-friendly access to generation features.

- **`tests/`**: System-level integration tests that verify end-to-end functionality.

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (optional - defaults are provided):

```bash
# Application Settings
APP_NAME="Patent Partners Assistant"
APP_VERSION="0.1.0"
DEBUG=true
LOG_LEVEL="INFO"

# Database
DB_PATH="./data/processed/patents.db"

# LLM Configuration
LLM_MODEL="mistral:latest"
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2048
OLLAMA_BASE_URL="http://localhost:11434"

# API Configuration
API_HOST="0.0.0.0"
API_PORT=8000

# UI Configuration
STREAMLIT_PORT=8501

# Privacy Mode
OFFLINE=true
```

### Adjusting Generation Parameters

Edit `config/settings.py` to change defaults:

```python
class Settings(BaseSettings):
    # LLM Configuration
    llm_model: str = "mistral:latest"       # Change model
    llm_temperature: float = 0.7            # Creativity (0.0-1.0)
    llm_max_tokens: int = 2048              # Max output length
    
    # Timeouts (in seconds)
    generation_timeout: int = 300           # 5 minutes default
```

### Model Selection

Ollama supports multiple models. To use a different model:

```bash
# List available models
ollama list

# Pull a different model
ollama pull llama2:13b        # Larger, more capable
ollama pull codellama:7b      # Code-specialized
ollama pull neural-chat:7b    # Conversation-optimized

# Update config
# Edit .env or settings.py:
LLM_MODEL="llama2:13b"
```

---

## 📚 API Documentation

### Base URL

```
http://localhost:8000
```

### Endpoints

#### 1. Health Check

**GET** `/health`

Check API and Ollama availability.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "offline_mode": true,
  "ollama_available": true,
  "timestamp": "2024-11-14T10:30:00Z"
}
```

#### 2. Generate Invention Memo

**POST** `/generate/memo`

Generate a comprehensive invention disclosure memo.

**Request Body:**
```json
{
  "invention_description": "Your invention description here (min 50 chars)",
  "context_chunks": null,
  "include_citations": true,
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "draft": "Generated memo text...",
  "generation_time_ms": 87340.5,
  "model_used": "mistral:latest",
  "citations": [],
  "sections": ["Executive Summary", "Technical Analysis", ...]
}
```

**Parameters:**
- `invention_description` (required): Text describing the invention (50-10000 chars)
- `context_chunks` (optional): Prior art context (not yet implemented)
- `include_citations` (optional): Whether to include citations (default: true)
- `max_tokens` (optional): Maximum output tokens (default: 2048)
- `temperature` (optional): Creativity level 0.0-1.0 (default: 0.7)

#### 3. Generate Patent Draft

**POST** `/generate/draft`

Generate a USPTO-compliant patent application draft.

**Request Body:**
```json
{
  "invention_description": "Your invention description here",
  "context_chunks": null,
  "include_citations": true,
  "max_tokens": 3000,
  "temperature": 0.7
}
```

**Response:**
```json
{
  "draft": "Generated patent draft...",
  "generation_time_ms": 92180.3,
  "model_used": "mistral:latest",
  "citations": [],
  "sections": ["Title", "Abstract", "Background", "Summary", "Claims"]
}
```

#### 4. Export to DOCX

**POST** `/export/docx`

Export generated content to Microsoft Word format.

**Request Body:**
```json
{
  "content": "Content to export...",
  "filename": "patent_draft.docx",
  "document_type": "draft"
}
```

**Response:**
```json
{
  "filename": "patent_draft.docx",
  "file_path": "/data/exports/patent_draft.docx",
  "file_size": 25600
}
```

### Error Responses

All endpoints return standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid parameters)
- **422**: Validation Error (Pydantic validation failed)
- **500**: Internal Server Error
- **503**: Service Unavailable (Ollama not accessible)

**Error Format:**
```json
{
  "detail": "Error message here",
  "error": "Specific error type",
  "timestamp": "2024-11-14T10:30:00Z"
}
```

### Interactive Documentation

Visit http://localhost:8000/docs for interactive API documentation with:
- Try-it-out functionality
- Request/response schemas
- Authentication testing
- Example payloads

---

## 👨‍💻 Development

### Setting Up Development Environment

```bash
# Clone and setup
git clone https://github.com/nandanpabolu/Capstone-Project-Team-4.git
cd Capstone-Project-Team-4
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black isort flake8
```

### Code Style

We follow PEP 8 with Black formatting:

```bash
# Format code
black src/

# Sort imports
isort src/

# Check style
flake8 src/
```

### Running in Development Mode

```bash
# API with auto-reload
uvicorn src.patent_assistant.api.main:app --reload --host 0.0.0.0 --port 8000

# UI with auto-reload (built-in)
streamlit run src/patent_assistant/ui/main.py --server.port 8501
```

### Adding New Features

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** following the project structure

3. **Add tests** in appropriate test directory

4. **Update documentation** (README, API docs, etc.)

5. **Run tests** to ensure nothing breaks
   ```bash
   python run_tests.py
   pytest
   ```

6. **Format code**
   ```bash
   black src/
   isort src/
   ```

7. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: Add your feature description"
   git push origin feature/your-feature-name
   ```

8. **Open Pull Request** on GitHub

### Adding New LLM Prompts

Prompts are in `src/patent_assistant/generation/`:

- `prompts.py` - Detailed mode prompts
- `prompts_fast.py` - Fast mode prompts

Example structure:
```python
MEMO_TEMPLATE = """You are a patent attorney...

Invention Description:
{invention_description}

Generate a comprehensive memo with:
1. Executive Summary
2. Technical Analysis
...
"""
```

### Logging

We use `loguru` for structured logging:

```python
from loguru import logger

logger.info("Generation started", invention_length=len(description))
logger.error("Generation failed", error=str(e))
```

Logs are written to:
- `logs/api.log` - API requests and responses
- `logs/generation.log` - LLM generation events
- Console output (development mode)

---

## ⚠️ Known Limitations

### Current MVP Limitations

1. **No Prior Art Search**: The system can generate memos and drafts but cannot yet search actual USPTO patents for prior art. This is planned for Sprint 2.

2. **No Citation Validation**: While the system includes citation fields, it cannot validate citations against real patents yet.

3. **No Multi-Language Support**: Currently supports English only.

4. **Generation Time**: Local LLM inference takes 60-180 seconds depending on mode. This is inherent to local processing but ensures privacy.

5. **Output Quality**: Generated content requires attorney review and editing. This is an assistant tool, not a replacement for professional legal expertise.

6. **Model Size**: Limited to 7B parameter model for broader hardware compatibility. Larger models would provide better quality but require more resources.

### System Requirements

- **Minimum**: 8GB RAM, 10GB disk space
- **Recommended**: 16GB RAM, 20GB disk space, dedicated GPU (optional)
- **Network**: Ollama initial model download requires internet; operation is fully offline after setup

### Performance Considerations

- First generation after server start is slower (cold start)
- Concurrent requests are queued (single worker by default)
- Very long descriptions (>2000 words) may hit token limits

---

## 👥 Team

**Team 4 - Patent Partners**  
Capstone Project, Fall 2024

| Role | Name | Responsibilities |
|------|------|-----------------|
| **Team Lead** | Arya Koirala | Project management, Safety & Crisis |
| **Data Engineer** | Devika Amalkar | Data pipeline, USPTO ingestion |
| **Backend Engineer** | Nandan P | API, LLM integration, Generation |
| **Frontend Engineer** | Rachel Mathew | UI/UX, Streamlit interface |
| **DevOps/QA** | Nicholas Joseph | Testing, CI/CD, Deployment |

### Contributions

This project is open-source and welcomes contributions! See [Development](#-development) section for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- **Mistral-7B**: Apache 2.0 License
- **Ollama**: MIT License
- **FastAPI**: MIT License
- **Streamlit**: Apache 2.0 License
- See individual package licenses in `requirements.txt`

---

## 📞 Contact & Support

- **Repository**: https://github.com/nandanpabolu/Capstone-Project-Team-4
- **Issues**: https://github.com/nandanpabolu/Capstone-Project-Team-4/issues
- **Discussions**: https://github.com/nandanpabolu/Capstone-Project-Team-4/discussions

---

## 🙏 Acknowledgments

- **Mistral AI** for the excellent open-source Mistral-7B model
- **Ollama** for making local LLM inference accessible
- **USPTO** for public patent data access
- Our capstone advisors and mentors

---

## ⚠️ Disclaimer

**This tool is for educational and research purposes only. It is not a replacement for professional legal counsel or patent attorney expertise.**

Generated documents should always be reviewed and edited by qualified patent professionals before filing. The system provides assistance and acceleration, not legal advice.

---

**Built with ❤️ by Team 4 - Patent Partners**

*Last Updated: November 14, 2024*
