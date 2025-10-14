# Patent Partners Assistant

**Team 4 - Patent Partners** | Capstone Project | Fall 2024

An offline, AI-powered patent assistant that helps lawyers and inventors with prior-art search, invention memo generation, and patent draft creation.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.119.0-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

This system provides:
- **Prior-Art Search**: Natural language search with citations
- **Invention Memo**: Automated summary of inventions vs. prior art  
- **Patent Drafting**: Skeleton patent documents (abstract, summary, claims)
- **Offline Operation**: Complete privacy with local processing

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/nandanpabolu/Capstone-Project-Team-4.git
cd Capstone-Project-Team-4

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize project
make setup

# Start the application
make api    # Terminal 1: Start API server
make ui     # Terminal 2: Start Streamlit UI
```

### Access the Application
- **Streamlit UI**: http://localhost:8501
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
patent-partners-assistant/
├── src/patent_assistant/     # Main application code
│   ├── api/                  # FastAPI endpoints
│   ├── database/             # SQLite operations
│   ├── models/               # Pydantic models
│   ├── parsers/              # USPTO XML parsing
│   ├── retrieval/            # Search & RAG pipeline
│   ├── generation/           # LLM integration
│   ├── ui/                   # Streamlit interface
│   └── tests/                # Unit tests
├── data/                     # Data storage
│   ├── raw/                  # Original patent files
│   └── processed/            # Processed data
├── config/                   # Configuration files
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
├── logs/                     # Application logs
├── indexes/                  # Search indexes
└── pyproject.toml           # Dependencies
```

## 🛠️ Tech Stack

- **Backend**: FastAPI + SQLite
- **UI**: Streamlit
- **Search**: BM25 (pytantivy) + Vector (FAISS)
- **LLM**: Ollama + Llama 2 7B
- **Export**: python-docx

## 📋 Features

### Core Features (MVP)
- [x] Patent data ingestion from USPTO XML
- [x] Hybrid search (BM25 + vector)
- [x] Invention memo generation
- [x] Patent draft export (DOCX)

### Stretch Features
- [ ] Text highlighting for overlaps
- [ ] Editable draft interface
- [ ] Advanced section generation

## 🧪 Testing

```bash
make test
```

## 📊 Data Sources

- **USPTO Bulk Data**: Primary patent text (XML)
- **PatentsView**: Clean metadata (TSV)
- **Synthetic Data**: Evaluation dataset

## 🔒 Privacy & Security

- **Offline Operation**: No external API calls
- **Local Processing**: All data stays on your machine
- **Audit Logging**: Complete operation traceability

## 📅 Timeline

- **Sprint 1** (Oct 20): System foundation & basic search
- **Sprint 2** (Nov 17): RAG pipeline & generation features  
- **Sprint 3** (Dec 4): Export functionality & polish
- **Demo Day** (Dec 11): Senior Design Day presentation

## 👥 Team

- **Team Lead**: Arya Koirala
- **Data Engineer**: Devika Amalkar  
- **Backend Engineer**: Nandan P
- **Frontend Engineer**: Rachel Mathew
- **Safety & Crisis Lead**: Arya Koirala
- **DevOps/QA**: Nicholas Joseph

## 🤝 Contributing

This is a capstone project for Team 4 - Patent Partners. For development:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Team Lead**: Arya Koirala
- **Data Engineer**: Devika Amalkar  
- **Backend Engineer**: Nandan P
- **Frontend Engineer**: Rachel Mathew
- **Safety & Crisis Lead**: Arya Koirala
- **DevOps/QA**: Nicholas Joseph

## 📞 Contact

- **Repository**: [https://github.com/nandanpabolu/Capstone-Project-Team-4](https://github.com/nandanpabolu/Capstone-Project-Team-4)
- **Issues**: [GitHub Issues](https://github.com/nandanpabolu/Capstone-Project-Team-4/issues)

---

**⚠️ Disclaimer**: This tool is for educational and research purposes only. It is not a replacement for professional legal counsel.
