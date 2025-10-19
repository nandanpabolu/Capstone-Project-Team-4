# MVP Component Dependencies

## 🔗 Visual Dependency Map

```
┌─────────────────────────────────────────────────────────────┐
│                         DAY 1-2                             │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────────┐         ┌──────────────────┐
    │  Component 1     │         │  Component 3     │
    │  Mock Data       │         │  LLM Setup       │
    │  (Devika)        │         │  (Nandan/Arya)   │
    │                  │         │                  │
    │  - JSON patents  │         │  - Ollama        │
    │  - Load script   │         │  - Prompts       │
    │  - DB utils      │         │  - Gen functions │
    └────────┬─────────┘         └────────┬─────────┘
             │                            │
             │ Provides                   │ Provides
             │ sample data                │ generation
             ▼                            ▼
    ┌──────────────────┐         ┌──────────────────┐
    │  Component 2     │         │  Component 4     │
    │  Search Engine   │         │  Frontend UI     │
    │  (Nandan)        │         │  (Rachel)        │
    │                  │         │                  │
    │  - Simple search │         │  - Mock APIs     │
    │  - Ranking       │         │  - UI polish     │
    └────────┬─────────┘         └────────┬─────────┘
             │                            │
             │                            │
             └──────────┬─────────────────┘
                        │
                        │ Both feed into
                        ▼

┌─────────────────────────────────────────────────────────────┐
│                         DAY 3                                │
└─────────────────────────────────────────────────────────────┘

                ┌──────────────────┐
                │  Component 5     │
                │  API Integration │
                │  (Nandan)        │
                │                  │
                │  - Wire endpoints│
                │  - Error handling│
                └────────┬─────────┘
                         │
                         │ Connects everything
                         ▼
              ┌─────────────────────┐
              │   Working APIs      │
              │  - /search          │
              │  - /generate/memo   │
              │  - /generate/draft  │
              └──────────┬──────────┘
                         │
                         │ Used by
                         ▼
                ┌──────────────────┐
                │  Component 4     │
                │  UI Updates      │
                │  (Rachel)        │
                │                  │
                │  - Connect to    │
                │    real APIs     │
                └─────────┬────────┘
                          │
                          │ Tested by
                          ▼

┌─────────────────────────────────────────────────────────────┐
│                         DAY 4                                │
└─────────────────────────────────────────────────────────────┘

                ┌──────────────────┐
                │  Component 6     │
                │  Testing & QA    │
                │  (Nicholas)      │
                │                  │
                │  - Unit tests    │
                │  - Integration   │
                │  - E2E tests     │
                └─────────┬────────┘
                          │
                          │ Validates
                          ▼
                ┌──────────────────┐
                │  Component 7     │
                │  Demo Ready      │
                │  (All Team)      │
                │                  │
                │  - Polish        │
                │  - Documentation │
                └──────────────────┘
```

---

## 🔄 Work Can Happen in Parallel

### **Parallel Track A** (Data → Search)
```
Devika (Data)
    ↓
Creates mock patents
    ↓
Nandan (Search) ← Uses data to build search
    ↓
API endpoint /search
```

### **Parallel Track B** (LLM → Generation)
```
Nandan/Arya (LLM)
    ↓
Sets up Ollama + Prompts
    ↓
API endpoints /generate/*
```

### **Parallel Track C** (UI Development)
```
Rachel (UI)
    ↓
Builds UI with mock responses
    ↓
Tuesday: Connects to real APIs
```

### **Parallel Track D** (Testing)
```
Nicholas (Testing)
    ↓
Writes tests as components are ready
    ↓
Validates integration
```

---

## ⏰ Critical Path (Must Happen in Order)

### **Monday End of Day Checkpoint**:
1. ✅ Devika: Mock data ready
2. ✅ Nandan: Ollama tested and working
3. ✅ Rachel: UI mockups done

**Blocker**: If mock data not ready, Nandan can't test search

### **Tuesday Morning Checkpoint**:
1. ✅ Nandan: Search function complete
2. ✅ Nandan: Generation functions complete

**Blocker**: If these not done, can't wire APIs

### **Tuesday End of Day Checkpoint**:
1. ✅ Nandan: APIs wired up and tested
2. ✅ Rachel: UI connected to APIs

**Blocker**: If APIs not working, UI can't integrate

### **Wednesday End of Day Checkpoint**:
1. ✅ All: E2E flow working
2. ✅ Nicholas: Tests passing
3. ✅ Arya: Demo script ready

**Blocker**: This is final checkpoint before demo

---

## 📦 Deliverable Dependencies

| Deliverable | Depends On | Blocks |
|-------------|------------|--------|
| Mock data (Devika) | Nothing | Search implementation |
| Search function (Nandan) | Mock data | /search API endpoint |
| LLM setup (Nandan) | Nothing | Generation functions |
| Generation functions (Nandan) | LLM setup | /generate/* endpoints |
| API wiring (Nandan) | Search + Generation | UI integration |
| UI integration (Rachel) | API wiring | E2E testing |
| E2E tests (Nicholas) | UI integration | Demo readiness |

---

## 🚦 Daily Handoffs

### **Monday 5 PM**
**Devika → Nandan**:
- Hand off: `data/mock_patents.json` + `patents.db`
- Nandan tests: Can query database and get results

**Nandan → Rachel**:
- Hand off: API endpoint specs (what they'll return)
- Rachel tests: Can mock these in UI

### **Tuesday 10 AM**
**Nandan → Rachel**:
- Hand off: Working API endpoints (localhost:8000)
- Rachel tests: curl commands work

### **Tuesday 5 PM**
**Rachel → Nicholas**:
- Hand off: Integrated UI + API
- Nicholas tests: E2E workflow

### **Wednesday 5 PM**
**All → Arya**:
- Hand off: Working demo
- Arya tests: Full presentation run-through

---

## 🎯 Who Needs What From Whom

### **Devika Needs**:
- ✅ Database schema (already exists in `schema.py`)
- Patent data format examples (I can provide)

### **Nandan Needs**:
- Mock data from Devika (Monday)
- Patent data format to know what to search

### **Rachel Needs**:
- API specifications from Nandan (Monday)
- Working API endpoints (Tuesday)

### **Nicholas Needs**:
- Testable code from everyone (ongoing)
- Working features to test (Tuesday-Wednesday)

### **Arya Needs**:
- Status updates from everyone (daily)
- Working system to demo (Wednesday)

---

## 💡 Pro Tips for Parallel Work

### **For Devika**:
- Start with 3-5 really good sample patents
- Expand to 20 if time permits
- Make them diverse (different tech areas)
- Include realistic claims and abstracts

### **For Nandan**:
- Don't wait for perfect data - use dummy data first
- Test Ollama installation TODAY
- Keep search simple - keyword matching is fine
- Document API endpoints for Rachel

### **For Rachel**:
- Mock API responses immediately
- Don't block on backend - develop UI independently
- Tuesday is your integration day
- Polish UI on Wednesday

### **For Nicholas**:
- Write test stubs early
- Fill them in as components are ready
- Focus on integration tests Wednesday
- Keep test data separate from real data

### **For Arya**:
- Daily 15-min standups keep everyone aligned
- Identify blockers fast
- Be ready to reassign tasks if someone blocked
- Start demo script Wednesday morning

---

## 🔗 Code Integration Points

### **Point 1: Database Connection**
```python
# Devika creates in db_utils.py
def get_patent(patent_id: str) -> Patent:
    ...

# Nandan uses in search
from database.db_utils import get_patent
```

### **Point 2: Search Function**
```python
# Nandan creates in simple_search.py
def search_patents(query: str, k: int) -> List[Passage]:
    ...

# Nandan uses in API
from retrieval.simple_search import search_patents
```

### **Point 3: Generation Function**
```python
# Nandan creates in llm_client.py
def generate_memo(invention: str, context: List[Passage]) -> str:
    ...

# Nandan uses in API
from generation.llm_client import generate_memo
```

### **Point 4: API Endpoints**
```python
# Nandan exposes in api/main.py
@app.post("/search")
def search_endpoint(request: SearchRequest):
    ...

# Rachel calls from UI
response = requests.post("http://localhost:8000/search", json={...})
```

---

**Everyone can work in parallel for the first 1-2 days, then integrate on Day 3!** 🚀

