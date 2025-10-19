# MVP Team Breakdown - Patent Partners Assistant

**Goal**: Working MVP by Thursday (4 days)  
**Team**: 5 members (Arya, Devika, Nandan, Rachel, Nicholas)

---

## 🎯 **Core MVP Components**

### **Component 1: Data & Database** 📊
**Owner**: Devika (Data Engineer)  
**Directory**: `src/patent_assistant/database/`, `data/`

**Tasks**:
1. Create **mock patent dataset** (10-20 sample patents)
2. Populate SQLite database with sample data
3. Implement database helper functions (insert, query, fetch)

**Deliverables**:
- [ ] `data/mock_patents.json` - 10-20 sample patents with:
  - Patent ID, Title, Abstract, Claims, Description
  - Inventor names, Filing date, Technology category
- [ ] `scripts/load_mock_data.py` - Script to populate database
- [ ] `src/patent_assistant/database/db_utils.py` - Database CRUD operations
- [ ] Working `patents.db` with sample data

**Dependencies**: None (can start immediately)  
**Time Estimate**: 1-2 days

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

### **Component 2: Search Engine** 🔍
**Owner**: Nandan (Backend Engineer)  
**Directory**: `src/patent_assistant/retrieval/`

**Tasks**:
1. Implement **simple keyword search** (no BM25 for MVP)
2. Create search API integration
3. Implement result ranking (basic relevance scoring)

**Deliverables**:
- [ ] `src/patent_assistant/retrieval/simple_search.py`:
  - `search_patents(query: str, k: int) -> List[Passage]`
  - Keyword matching in title, abstract, claims
  - Basic TF-IDF or count-based ranking
- [ ] `src/patent_assistant/retrieval/reranker.py` (optional):
  - Simple relevance scoring
- [ ] Integration with `/search` API endpoint

**Dependencies**: 
- Needs mock data from Component 1
- Can work on logic in parallel with dummy data

**Time Estimate**: 1-2 days

**Simple Search Algorithm** (for MVP):
```python
def search_patents(query, k=10):
    # 1. Tokenize query
    # 2. Search in database (title, abstract, claims)
    # 3. Score by keyword matches
    # 4. Return top k results
```

---

### **Component 3: LLM Integration** 🤖
**Owner**: Nandan (Backend Engineer) or Arya (Team Lead)  
**Directory**: `src/patent_assistant/generation/`

**Tasks**:
1. Set up **Ollama + Mistral-7B** locally
2. Create prompt templates for memo and draft generation
3. Implement generation functions with citation tracking

**Deliverables**:
- [ ] Ollama installed and working
- [ ] `src/patent_assistant/generation/llm_client.py`:
  - `generate_memo(invention_text, context) -> str`
  - `generate_draft(invention_details, context) -> DraftOut`
- [ ] `src/patent_assistant/generation/prompts.py`:
  - Prompt templates for each use case
- [ ] Integration with `/generate/memo` and `/generate/draft` endpoints

**Dependencies**: None (can work independently)  
**Time Estimate**: 2 days

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

### **Component 4: Frontend UI** 🎨
**Owner**: Rachel (Frontend Engineer)  
**Directory**: `src/patent_assistant/ui/`

**Tasks**:
1. Connect UI to working API endpoints
2. Add loading states, error handling
3. Improve UX and styling
4. Display search results and generated content

**Deliverables**:
- [ ] `src/patent_assistant/ui/main.py` updates:
  - Search tab: Call `/search` API, display results
  - Memo tab: Call `/generate/memo` API, show output
  - Draft tab: Call `/generate/draft` API, format nicely
- [ ] Loading spinners while API calls run
- [ ] Error messages for failed requests
- [ ] Nice formatting for results (markdown, code blocks)

**Dependencies**: 
- Needs working API endpoints (Components 2 & 3)
- Can mock API responses initially

**Time Estimate**: 2 days

**Mock API Response** (to start development):
```python
# Rachel can use this to develop UI before APIs are ready
mock_search_response = {
    "passages": [
        {"doc_id": "US10000001", "text": "...", "score": 0.95},
        {"doc_id": "US10000002", "text": "...", "score": 0.87}
    ]
}
```

---

### **Component 5: API Integration** 🔌
**Owner**: Nandan (Backend Engineer)  
**Directory**: `src/patent_assistant/api/`

**Tasks**:
1. Wire up `/search` endpoint to search engine
2. Wire up `/generate/memo` to LLM
3. Wire up `/generate/draft` to LLM
4. Add error handling and logging

**Deliverables**:
- [ ] Update `src/patent_assistant/api/main.py`:
  - `/search` → calls search_patents() → returns results
  - `/generate/memo` → calls generate_memo() → returns memo
  - `/generate/draft` → calls generate_draft() → returns draft
- [ ] Proper error handling (try/except, return error responses)
- [ ] Request logging to `logs/api.log`

**Dependencies**: 
- Needs Components 2 & 3 completed
- This is the **integration layer**

**Time Estimate**: 1 day (after Components 2 & 3)

---

### **Component 6: Testing & QA** 🧪
**Owner**: Nicholas (DevOps/QA)  
**Directory**: `src/patent_assistant/tests/`

**Tasks**:
1. Write unit tests for each component
2. Create end-to-end test scenarios
3. Test API endpoints
4. Document bugs and edge cases

**Deliverables**:
- [ ] `tests/test_search.py` - Test search functionality
- [ ] `tests/test_generation.py` - Test LLM generation
- [ ] `tests/test_api.py` - Test API endpoints
- [ ] `tests/test_e2e.py` - End-to-end workflow tests
- [ ] `TEST_RESULTS.md` - Test coverage report

**Dependencies**: All components (tests last)  
**Time Estimate**: Ongoing, 1 day final testing

**Test Script Example**:
```bash
# Nicholas runs these daily
make test
curl http://localhost:8000/health
curl -X POST http://localhost:8000/search -d '{"query":"drone"}'
```

---

### **Component 7: Documentation & Demo** 📝
**Owner**: Arya (Team Lead) + All  
**Directory**: `docs/`, root `*.md` files

**Tasks**:
1. Update documentation as features are built
2. Create demo script for Thursday
3. Prepare presentation materials
4. Coordinate team integration

**Deliverables**:
- [ ] Updated `README.md` with current features
- [ ] `DEMO_THURSDAY.md` - Demo script for presentation
- [ ] Screenshots/video of working demo
- [ ] Integration plan document

**Dependencies**: All components  
**Time Estimate**: Ongoing, finalize Wednesday

---

## 📅 **4-Day Timeline**

### **Sunday (Day 1) - Foundation**
**All Team**:
- [x] Project setup complete ✅
- [x] Repository clean ✅
- [ ] Team assignments confirmed

**Devika**:
- [ ] Start creating mock patent data
- [ ] Design sample dataset structure

**Nandan**:
- [ ] Install Ollama locally
- [ ] Test Mistral-7B model
- [ ] Start search algorithm design

**Rachel**:
- [ ] Review current UI
- [ ] Plan UI improvements
- [ ] Create mock API responses for development

**Nicholas**:
- [ ] Set up testing environment
- [ ] Review current test coverage
- [ ] Plan test scenarios

**Arya**:
- [ ] Coordinate team
- [ ] Review architecture
- [ ] Plan integration strategy

---

### **Monday (Day 2) - Core Development**
**Devika**:
- [ ] Complete mock dataset (10-20 patents)
- [ ] Create database loading script
- [ ] Populate SQLite database
- [ ] Share sample data with team

**Nandan**:
- [ ] Implement simple search function
- [ ] Create LLM generation functions
- [ ] Test both components independently
- [ ] Share API contracts with Rachel

**Rachel**:
- [ ] Build search UI with mock data
- [ ] Build memo UI with mock data
- [ ] Add loading states
- [ ] Prepare for API integration

**Nicholas**:
- [ ] Write unit tests for database utils
- [ ] Write unit tests for search (with mock data)
- [ ] Set up continuous testing

**Arya**:
- [ ] Review progress
- [ ] Help troubleshoot issues
- [ ] Coordinate handoffs

---

### **Tuesday (Day 3) - Integration**
**Nandan**:
- [ ] Wire up `/search` endpoint to search engine
- [ ] Wire up `/generate/memo` endpoint to LLM
- [ ] Wire up `/generate/draft` endpoint to LLM
- [ ] Test all endpoints with Postman/curl

**Rachel**:
- [ ] Connect UI to real API endpoints
- [ ] Test search flow end-to-end
- [ ] Test memo generation flow
- [ ] Test draft generation flow
- [ ] Fix UI bugs

**Devika**:
- [ ] Support integration issues
- [ ] Add more sample patents if needed
- [ ] Optimize database queries

**Nicholas**:
- [ ] Integration testing
- [ ] API endpoint testing
- [ ] Document bugs
- [ ] Help with fixes

**Arya**:
- [ ] Test complete workflow
- [ ] Identify gaps
- [ ] Prioritize fixes

---

### **Wednesday (Day 4) - Polish & Testing**
**All Team**:
- [ ] Final integration testing
- [ ] Bug fixes from Tuesday testing
- [ ] Polish UI (styling, error messages)
- [ ] Prepare demo materials

**Nandan**:
- [ ] Optimize API performance
- [ ] Add comprehensive error handling
- [ ] Review and test all endpoints

**Rachel**:
- [ ] UI polish (colors, spacing, fonts)
- [ ] Add help text and instructions
- [ ] Make demo user-friendly

**Devika**:
- [ ] Ensure data quality
- [ ] Add interesting sample patents for demo

**Nicholas**:
- [ ] Final test suite run
- [ ] Create test report
- [ ] Verify all features work

**Arya**:
- [ ] Write demo script
- [ ] Practice presentation
- [ ] Prepare backup plan

---

### **Thursday (Day 5) - Demo Day** 🎉
**Morning**:
- [ ] Final smoke test
- [ ] Start servers
- [ ] Test complete workflow
- [ ] Prepare demo environment

**Demo**:
- [ ] Present working MVP
- [ ] Show search functionality
- [ ] Show memo generation
- [ ] Show draft generation
- [ ] Answer questions

---

## 🔧 **Technical Handoff Points**

### **Devika → Nandan**:
- **What**: Sample patent data in database
- **When**: Monday EOD
- **Format**: SQLite database + sample query functions
- **Test**: Nandan can query and get results

### **Nandan → Rachel**:
- **What**: Working API endpoints
- **When**: Tuesday morning
- **Format**: API docs + example requests/responses
- **Test**: Rachel can call APIs via curl/Postman

### **Nandan → Nicholas**:
- **What**: Testable functions and endpoints
- **When**: Monday EOD (unit tests), Tuesday EOD (integration)
- **Format**: Python functions + API endpoints
- **Test**: Nicholas can run automated tests

### **All → Arya**:
- **What**: Status updates
- **When**: Daily standup (15 min)
- **Format**: What I did, what I'm doing, blockers
- **Test**: Team coordination

---

## 🎯 **Success Criteria for MVP**

### **Must Work** (Core Demo Flow):
1. ✅ User enters search query → gets relevant results
2. ✅ User enters invention description → gets generated memo
3. ✅ User enters patent details → gets generated draft
4. ✅ UI looks professional and works smoothly
5. ✅ No crashes during demo

### **Nice to Have** (If Time):
- Citation highlighting in generated text
- Search filters (by date, category)
- Multiple search results with ranking
- Formatted patent draft (proper sections)
- Export generated content (PDF/Word)

---

## 📞 **Communication Plan**

### **Daily Standup** (15 min):
- **When**: 9 AM daily (or convenient time)
- **Format**: Quick Slack/Teams call
- **Agenda**: Yesterday/Today/Blockers

### **Integration Checkpoints**:
- **Monday 5 PM**: Data ready
- **Tuesday 10 AM**: APIs ready
- **Tuesday 5 PM**: UI integrated
- **Wednesday 5 PM**: Demo-ready

### **Slack Channels** (Suggested):
- `#mvp-general` - General discussion
- `#mvp-backend` - Nandan + Devika
- `#mvp-frontend` - Rachel
- `#mvp-testing` - Nicholas
- `#mvp-blockers` - Urgent issues

---

## 🚨 **Risk Mitigation**

### **Risk 1: LLM doesn't work on someone's machine**
- **Mitigation**: One person (Nandan) runs Ollama, expose via API
- **Backup**: Use OpenAI API (costs ~$1 for demo) or mock responses

### **Risk 2: Search is too simple**
- **Mitigation**: Focus on demo-worthy sample patents
- **Backup**: Hardcode good search results for demo

### **Risk 3: Integration issues**
- **Mitigation**: Use API contracts, test early
- **Backup**: Rachel can mock API responses in UI

### **Risk 4: Time runs out**
- **Mitigation**: Prioritize core flow, cut nice-to-haves
- **Backup**: Demo slides showing what's "in progress"

---

## 📋 **Development Checklist**

### **Devika (Data Engineer)**
- [ ] Create 10-20 mock patents in JSON format
- [ ] Write script to load data into SQLite
- [ ] Create database helper functions (get_patent, search_db)
- [ ] Share sample data with team by Monday EOD
- [ ] Support integration issues Tuesday-Wednesday

### **Nandan (Backend Engineer)**
- [ ] Install and test Ollama + Mistral-7B
- [ ] Implement simple search function
- [ ] Implement memo generation function
- [ ] Implement draft generation function
- [ ] Wire up all API endpoints
- [ ] Test with Postman/curl

### **Rachel (Frontend Engineer)**
- [ ] Create mock API responses for development
- [ ] Build search UI (input, results display)
- [ ] Build memo UI (input, output display)
- [ ] Build draft UI (form, output display)
- [ ] Integrate with real APIs Tuesday
- [ ] Polish UI Wednesday

### **Nicholas (DevOps/QA)**
- [ ] Write unit tests for database functions
- [ ] Write unit tests for search
- [ ] Write unit tests for generation
- [ ] Write API endpoint tests
- [ ] Run integration tests Tuesday-Wednesday
- [ ] Create test report

### **Arya (Team Lead)**
- [ ] Assign tasks to team members
- [ ] Daily standup coordination
- [ ] Remove blockers
- [ ] Test complete workflow Wednesday
- [ ] Write demo script Wednesday
- [ ] Lead Thursday presentation

---

## 🎬 **Getting Started**

### **First Steps** (Everyone):
1. Read this document completely
2. Confirm your component assignment
3. Ask questions in team channel
4. Start working on Day 1 tasks
5. Communicate blockers immediately

### **First Commits** (By Monday):
- Devika: `data/mock_patents.json`
- Nandan: `src/patent_assistant/retrieval/simple_search.py`
- Nandan: `src/patent_assistant/generation/llm_client.py`
- Rachel: Updated `src/patent_assistant/ui/main.py` with better UI
- Nicholas: `tests/test_database.py`

---

## 🎯 **Questions to Answer Now**

1. **Arya**: Who owns which component? (Confirm assignments)
2. **Devika**: Can you create 10-20 mock patents by Monday?
3. **Nandan**: Can you install Ollama today and test it?
4. **Rachel**: Do you need API examples to start UI work?
5. **Nicholas**: What testing framework do you prefer?

---

**Let's build this MVP! 🚀**

*Last updated: October 19, 2025*

