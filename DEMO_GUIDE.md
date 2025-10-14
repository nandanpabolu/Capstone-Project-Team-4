# Patent Partners Assistant - Demo Guide

## 🎯 **Demo Tomorrow - Quick Start**

### **1. Start the System (2 minutes)**
```bash
# Activate virtual environment
source venv/bin/activate

# Start API server (Terminal 1)
make api

# Start Streamlit UI (Terminal 2) 
make ui
```

### **2. Demo URLs**
- **Streamlit UI**: http://localhost:8501
- **API Server**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### **3. Demo Script (Optional)**
```bash
# Run automated demo
python demo_script.py
```

---

## 🎬 **Demo Flow (5-7 minutes)**

### **Opening (1 minute)**
- "This is the Patent Partners Assistant - an offline AI-powered patent analysis tool"
- "Built for Team 4's capstone project, it helps lawyers with prior art search and patent drafting"

### **Show Streamlit UI (2 minutes)**
1. **Open**: http://localhost:8501
2. **Navigate tabs**:
   - **Idea Input**: "Users can describe their invention here"
   - **Prior Art Search**: "Search for existing patents"
   - **Invention Memo**: "Generate comparison memos"
   - **Export Draft**: "Export patent documents"

### **Show API (2 minutes)**
1. **Open**: http://localhost:8000/docs
2. **Test endpoints**:
   - **Health Check**: Shows system status
   - **Search**: Patent search functionality
   - **Generate Memo**: AI memo generation
   - **Generate Draft**: Patent draft creation

### **Technical Highlights (1-2 minutes)**
- **Offline Operation**: No external API calls
- **Hybrid Search**: BM25 + Vector search ready
- **Citation System**: Proper patent references
- **Export Functionality**: DOCX generation
- **Clean Architecture**: FastAPI + Streamlit + SQLite

---

## 🚀 **Key Talking Points**

### **Problem Solved**
- "Patent lawyers spend hours on repetitive tasks"
- "Existing tools require cloud access (privacy concerns)"
- "Our solution: completely offline, local processing"

### **Technical Architecture**
- **Backend**: FastAPI with SQLite database
- **Frontend**: Streamlit for lawyer-friendly interface
- **Search**: Hybrid BM25 + FAISS vector search
- **AI**: Local LLM integration (Ollama + Llama 2)
- **Privacy**: All data stays on local machine

### **Current Status**
- ✅ **Sprint 1 Complete**: System foundation, API, UI
- ✅ **Working Demo**: All endpoints functional
- 🔄 **Sprint 2 Next**: USPTO data ingestion, search implementation
- 🔄 **Sprint 3 Final**: Export functionality, polish

### **Future Features**
- Real patent data processing
- Advanced search with reranking
- Citation validation and retry logic
- Professional document export

---

## 🛠️ **Troubleshooting**

### **If API won't start:**
```bash
source venv/bin/activate
uvicorn src.patent_assistant.api.main:app --reload --host 0.0.0.0 --port 8000
```

### **If Streamlit won't start:**
```bash
source venv/bin/activate
streamlit run src/patent_assistant/ui/main.py --server.port 8501
```

### **If ports are busy:**
```bash
# Kill processes on ports
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9
```

---

## 📋 **Demo Checklist**

- [ ] Virtual environment activated
- [ ] API server running (http://localhost:8000)
- [ ] Streamlit UI running (http://localhost:8501)
- [ ] Health check passes
- [ ] All API endpoints responding
- [ ] UI tabs working
- [ ] Demo script passes (optional)

---

## 🎯 **Success Metrics**

- **System Status**: All green ✅
- **Response Time**: < 1 second for all endpoints
- **UI Responsiveness**: Smooth navigation
- **API Documentation**: Interactive and clear
- **Offline Mode**: Confirmed working

**You're ready to impress tomorrow!** 🚀
