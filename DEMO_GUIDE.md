# Patent Partners Assistant - Complete Technical Guide

**Team 4 - Patent Partners | Capstone Project**  
**Repository**: https://github.com/nandanpabolu/Capstone-Project-Team-4

---

## Table of Contents
1. [Quick Demo Setup](#quick-demo-setup)
2. [Sprint 1 - What We Built](#sprint-1---what-we-built)
3. [MVP Plan - Thursday Deadline](#mvp-plan---thursday-deadline)
4. [Component Breakdown & Team Assignments](#component-breakdown--team-assignments)
5. [Technical Architecture](#technical-architecture)
6. [Troubleshooting](#troubleshooting)

---

## Quick Demo Setup

### 1. Start the System (2 minutes)
```bash
# Navigate to project
cd ~/Desktop/Full_Time/Projects/Project_Experiment/Capstone

# Activate virtual environment
source venv/bin/activate

# Start both servers
make start
# OR separately:
# make api    # Terminal 1
# make ui     # Terminal 2
```

### 2. Demo URLs
- **Streamlit UI**: http://localhost:8501
- **API Server**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. Demo Flow (5-7 minutes)

**Opening (1 minute)**
- "This is the Patent Partners Assistant - an offline AI-powered patent analysis tool"
- "Built for Team 4's capstone project, it helps lawyers with prior art search and patent drafting"

**Show Streamlit UI (2 minutes)**
1. Open: http://localhost:8501
2. Navigate tabs:
   - **Prior Art Search**: Search for existing patents
   - **Invention Memo**: Generate comparison memos
   - **Patent Draft**: Create patent documents
   - **About**: Project information

**Show API (2 minutes)**
1. Open: http://localhost:8000/docs
2. Test endpoints:
   - **Health Check**: Shows system status
   - **Search**: Patent search functionality
   - **Generate Memo**: AI memo generation
   - **Generate Draft**: Patent draft creation

**Technical Highlights (1-2 minutes)**
- **Offline Operation**: No external API calls
- **Hybrid Search**: BM25 + Vector search (planned)
- **Citation System**: Proper patent references
- **Clean Architecture**: FastAPI + Streamlit + SQLite

---

## Sprint 1 - What We Built

### 1. Professional GitHub Repository
- Complete project structure
- Professional README with badges
- MIT License
- Comprehensive .gitignore
- Clean commit history

### 2. Backend API (FastAPI)

**Endpoints Implemented:**
- `GET /health` - System health check
- `POST /search` - Prior-art search (ready for implementation)
- `POST /generate/memo` - Invention disclosure memo generation
- `POST /generate/draft` - Patent draft generation
- Interactive API documentation at `/docs`

**Features:**
- Type-safe with Pydantic models
- Automatic OpenAPI/Swagger docs
- Error handling framework
- Logging configuration
- Offline mode support

### 3. Frontend UI (Streamlit)

**Tabs Created:**
- **Prior-Art Search** - Natural language patent search
- **Invention Memo** - AI-generated disclosure memos
- **Patent Draft** - Automated draft generation
- **About** - Project information and team

**Features:**
- Modern, clean interface
- Professional navigation
- Responsive layout
- Ready for API integration

### 4. Database Design

**Schema Tables:**
- `patents` - Core patent metadata
- `chunks` - Text segments with character spans
- `inventors` - Inventor information
- `citations` - Patent citation graph
- Optimized indexes for fast retrieval

**Location**: `src/patent_assistant/database/schema.py`

### 5. Data Models (Pydantic)

**Models Created:**
- `PatentDocument` - Complete patent record
- `Chunk` - Text segment with character spans
- `Passage` - Search result with citation
- `SearchRequest` - Search query parameters
- `GenerateRequest` - Generation parameters
- `DraftOut` - Patent draft output
- `ContextPack` - Retrieved context for LLM

**Location**: `src/patent_assistant/models/core.py`

### 6. Tech Stack (All Free)

| Component | Technology | Cost |
|-----------|-----------|------|
| **Language** | Python 3.9+ | Free |
| **Backend** | FastAPI 0.119.0 | Free |
| **Frontend** | Streamlit 1.50.0 | Free |
| **Database** | SQLite 3.x | Free |
| **Vector Search** | FAISS | Free |
| **Embeddings** | sentence-transformers | Free |
| **LLM** | Mistral-7B via Ollama | Free |
| **Testing** | pytest | Free |

**Total Monthly Cost**: $0

### 7. Project Structure

```
Capstone-Project-Team-4/
├── README.md                    # Main documentation
├── LICENSE                      # MIT License
├── Makefile                     # Task automation
├── requirements.txt             # Dependencies
├── setup.py                    # Package setup
├── start_servers.sh            # Server startup script
│
├── config/                     # Configuration
│   └── settings.py
│
├── docs/                       # Documentation
│   ├── API.md
│   └── ARCHITECTURE.md
│
├── scripts/                    # Automation scripts
│   ├── ingest_patents.py
│   └── build_indexes.py
│
├── src/patent_assistant/       # Main application
│   ├── api/                    # FastAPI endpoints
│   ├── ui/                     # Streamlit interface
│   ├── models/                 # Pydantic models
│   ├── database/               # Database schema
│   ├── parsers/                # USPTO parsing
│   ├── retrieval/              # Search engines
│   ├── generation/             # LLM integration
│   └── tests/                  # Unit tests
│
├── data/                       # Data (gitignored)
├── indexes/                    # Search indexes (gitignored)
├── logs/                       # Log files (gitignored)
└── venv/                       # Virtual environment (gitignored)
```

---

## MVP Plan - Thursday Deadline

**Goal**: Working MVP by Thursday (4 days from Sunday, Oct 19)  
**Team**: 5 members (Arya, Devika, Nandan, Rachel, Nicholas)

### Success Criteria

**Must Work** (Core Demo Flow):
1. User enters search query → gets relevant results
2. User enters invention description → gets generated memo
3. User enters patent details → gets generated draft
4. UI looks professional and works smoothly
5. No crashes during demo

**Nice to Have** (If Time):
- Citation highlighting in generated text
- Search filters (by date, category)
- Multiple search results with ranking
- Formatted patent draft (proper sections)

### 4-Day Timeline

**Sunday (Day 1) - Foundation**
- Devika: Start creating mock patent data
- Nandan: Install Ollama, test Mistral-7B
- Rachel: Plan UI improvements
- Nicholas: Setup testing environment
- Arya: Coordinate team

**Monday (Day 2) - Core Development**
- Devika: Complete mock dataset (10-20 patents), populate database
- Nandan: Implement search function + LLM generation
- Rachel: Build UI with mock data
- Nicholas: Write unit tests
- **Deadline**: Mock data ready, Ollama working

**Tuesday (Day 3) - Integration**
- Nandan: Wire up all API endpoints
- Rachel: Connect UI to real APIs
- Devika: Support integration issues
- Nicholas: Integration testing
- **Deadline**: E2E flow working

**Wednesday (Day 4) - Polish & Testing**
- All: Final integration testing
- All: Bug fixes from Tuesday
- Rachel: UI polish
- Nicholas: Final test suite
- Arya: Write demo script
- **Deadline**: Demo-ready system

**Thursday (Day 5) - Demo Day**
- Morning: Final smoke test
- Demo: Present working MVP

---

## Component Breakdown & Team Assignments

### Component 1: Data & Database
**Owner**: Devika (Data Engineer)  
**Directory**: `src/patent_assistant/database/`, `data/`

**Tasks**:
1. Create mock patent dataset (10-20 sample patents)
2. Populate SQLite database with sample data
3. Implement database helper functions

**Deliverables**:
- `data/mock_patents.json` - 10-20 sample patents
- `scripts/load_mock_data.py` - Database loading script
- `src/patent_assistant/database/db_utils.py` - CRUD operations
- Working `patents.db` with sample data

**Dependencies**: None (start immediately)  
**Time**: 1-2 days

**Example Mock Patent**:
```json
{
  "patent_id": "US10000001",
  "title": "Autonomous Delivery Drone with Obstacle Avoidance",
  "abstract": "A delivery drone system using computer vision...",
  "claims": ["1. A drone comprising...", "2. The drone of claim 1..."],
  "description": "Full text description...",
  "inventors": ["John Smith", "Jane Doe"],
  "filing_date": "2023-01-15",
  "category": "Robotics"
}
```

---

### Component 2: Search Engine
**Owner**: Nandan (Backend Engineer)  
**Directory**: `src/patent_assistant/retrieval/`

**Tasks**:
1. Implement simple keyword search (no BM25 for MVP)
2. Create search API integration
3. Implement result ranking

**Deliverables**:
- `src/patent_assistant/retrieval/simple_search.py`
  - `search_patents(query: str, k: int) -> List[Passage]`
  - Keyword matching in title, abstract, claims
  - Basic TF-IDF or count-based ranking
- Integration with `/search` API endpoint

**Dependencies**: Mock data from Devika  
**Time**: 1-2 days

**Simple Search Algorithm**:
```python
def search_patents(query, k=10):
    # 1. Tokenize query
    # 2. Search in database (title, abstract, claims)
    # 3. Score by keyword matches
    # 4. Return top k results
```

---

### Component 3: LLM Integration
**Owner**: Nandan (Backend Engineer) or Arya (Team Lead)  
**Directory**: `src/patent_assistant/generation/`

**Tasks**:
1. Set up Ollama + Mistral-7B locally
2. Create prompt templates
3. Implement generation functions

**Deliverables**:
- Ollama installed and working
- `src/patent_assistant/generation/llm_client.py`
  - `generate_memo(invention_text, context) -> str`
  - `generate_draft(invention_details, context) -> DraftOut`
- `src/patent_assistant/generation/prompts.py`
  - Prompt templates for each use case
- Integration with API endpoints

**Dependencies**: None (parallel work)  
**Time**: 2 days

**Setup Commands**:
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download Mistral
ollama pull mistral:7b-instruct

# Test
ollama run mistral:7b-instruct "Write a patent abstract"
```

**Prompt Template Example**:
```python
MEMO_PROMPT = """You are a patent attorney assistant. 
Given this invention description and prior art, write an invention disclosure memo.

Invention: {invention_text}

Prior Art Found:
{prior_art_passages}

Generate a memo with:
1. Summary of Invention
2. Prior Art Analysis
3. Novelty Assessment
4. Recommendations"""
```

---

### Component 4: Frontend UI
**Owner**: Rachel (Frontend Engineer)  
**Directory**: `src/patent_assistant/ui/`

**Tasks**:
1. Connect UI to working API endpoints
2. Add loading states, error handling
3. Improve UX and styling
4. Display search results and generated content

**Deliverables**:
- Updated `src/patent_assistant/ui/main.py`:
  - Search tab: Call `/search` API, display results
  - Memo tab: Call `/generate/memo` API, show output
  - Draft tab: Call `/generate/draft` API, format nicely
- Loading spinners while API calls run
- Error messages for failed requests
- Nice formatting for results

**Dependencies**: Working API endpoints (Tuesday)  
**Time**: 2 days

---

### Component 5: API Integration
**Owner**: Nandan (Backend Engineer)  
**Directory**: `src/patent_assistant/api/`

**Tasks**:
1. Wire up `/search` endpoint to search engine
2. Wire up `/generate/memo` to LLM
3. Wire up `/generate/draft` to LLM
4. Add error handling and logging

**Deliverables**:
- Updated `src/patent_assistant/api/main.py`
  - All endpoints connected to logic
  - Proper error handling
  - Request logging

**Dependencies**: Search + LLM components  
**Time**: 1 day (Tuesday)

---

### Component 6: Testing & QA
**Owner**: Nicholas (DevOps/QA)  
**Directory**: `src/patent_assistant/tests/`

**Tasks**:
1. Write unit tests for each component
2. Create end-to-end test scenarios
3. Test API endpoints
4. Document bugs and edge cases

**Deliverables**:
- `tests/test_search.py` - Test search functionality
- `tests/test_generation.py` - Test LLM generation
- `tests/test_api.py` - Test API endpoints
- `tests/test_e2e.py` - End-to-end workflow tests
- Test coverage report

**Dependencies**: All components  
**Time**: Ongoing, finalize Wednesday

---

### Component 7: Documentation & Demo
**Owner**: Arya (Team Lead) + All  

**Tasks**:
1. Update documentation as features are built
2. Create demo script for Thursday
3. Prepare presentation materials
4. Coordinate team integration

**Deliverables**:
- Updated documentation
- Demo script for presentation
- Screenshots/video of working demo
- Integration plan

**Dependencies**: All components  
**Time**: Finalize Wednesday

---

## Component Dependencies

### Parallel Work Tracks

**Track A (Data → Search)**:
```
Devika (Data)
    ↓
Creates mock patents
    ↓
Nandan (Search) ← Uses data
    ↓
API endpoint /search
```

**Track B (LLM → Generation)**:
```
Nandan/Arya (LLM)
    ↓
Sets up Ollama + Prompts
    ↓
API endpoints /generate/*
```

**Track C (UI Development)**:
```
Rachel (UI)
    ↓
Builds UI with mock responses
    ↓
Tuesday: Connects to real APIs
```

**Track D (Testing)**:
```
Nicholas (Testing)
    ↓
Writes tests as components ready
    ↓
Validates integration
```

### Critical Handoffs

**Monday 5 PM**:
- Devika → Nandan: Mock data + database
- Nandan → Rachel: API endpoint specs

**Tuesday 10 AM**:
- Nandan → Rachel: Working API endpoints

**Tuesday 5 PM**:
- Rachel → Nicholas: Integrated UI + API

**Wednesday 5 PM**:
- All → Arya: Working demo

### Deliverable Dependencies

| Deliverable | Depends On | Blocks |
|-------------|------------|--------|
| Mock data (Devika) | Nothing | Search implementation |
| Search function (Nandan) | Mock data | /search API |
| LLM setup (Nandan) | Nothing | Generation functions |
| Generation (Nandan) | LLM setup | /generate/* APIs |
| API wiring (Nandan) | Search + Generation | UI integration |
| UI integration (Rachel) | API wiring | E2E testing |
| E2E tests (Nicholas) | UI integration | Demo readiness |

---

## Technical Architecture

### System Flow
```
User → Streamlit UI → FastAPI → {Database, Search, LLM} → Response
```

### Data Flow
1. **Ingestion**: USPTO XML → Parser → SQLite + Text Chunks
2. **Indexing**: Chunks → BM25 Index + FAISS Index
3. **Search**: Query → Hybrid Retrieval → Reranking → Top Results
4. **Generation**: Results + Prompt → Mistral-7B → Cited Output

### Key Design Decisions
- **Offline Mode**: `OFFLINE=true` blocks all outbound HTTP
- **Character Spans**: Track exact citation locations
- **Hybrid Search**: Combine keyword + semantic
- **Type Safety**: Pydantic models everywhere

---

## Troubleshooting

### If API won't start:
```bash
source venv/bin/activate
uvicorn src.patent_assistant.api.main:app --reload --host 0.0.0.0 --port 8000
```

### If Streamlit won't start:
```bash
source venv/bin/activate
streamlit run src/patent_assistant/ui/main.py --server.port 8501
```

### If ports are busy:
```bash
# Kill processes on ports
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9
```

### Clean restart:
```bash
make clean
make install
make start
```

### If servers keep reloading:
```bash
# Use the clean startup script
./start_servers.sh
```

---

## Demo Checklist

- [ ] Virtual environment activated
- [ ] API server running (http://localhost:8000)
- [ ] Streamlit UI running (http://localhost:8501)
- [ ] Health check passes
- [ ] All API endpoints responding
- [ ] UI tabs working

---

## Contact & Resources

- **Repository**: https://github.com/nandanpabolu/Capstone-Project-Team-4
- **Issues**: https://github.com/nandanpabolu/Capstone-Project-Team-4/issues
- **Team Lead**: Arya Koirala
- **Data Engineer**: Devika Amalkar
- **Backend Engineer**: Nandan P
- **Frontend Engineer**: Rachel Mathew
- **DevOps/QA**: Nicholas Joseph

---

*Last updated: October 19, 2025*
