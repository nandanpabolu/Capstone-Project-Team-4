# Patent Partners Assistant - Makefile
# Team 4 Capstone Project

.PHONY: help setup install api ui test test-all clean lint format start

# Default target
help:
	@echo "Patent Partners Assistant - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  setup     - Initialize project and create directories"
	@echo "  install   - Install dependencies from requirements.txt"
	@echo ""
	@echo "Development:"
	@echo "  api       - Start FastAPI server"
	@echo "  ui        - Launch Streamlit UI"
	@echo "  start     - Start both API and UI servers"
	@echo ""
	@echo "Testing:"
	@echo "  test      - Run comprehensive system tests"
	@echo "  test-all  - Run all tests (unit + system)"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint      - Run linting checks"
	@echo "  format    - Format code with black and isort"
	@echo "  clean     - Clean up temporary files and cache"

# Setup project directories and environment
setup:
	@echo "Setting up Patent Partners Assistant..."
	@mkdir -p data/{raw,processed,exports}
	@mkdir -p data/processed/backups
	@mkdir -p logs indexes/{bm25,faiss}
	@mkdir -p tests
	@echo "✅ Project directories created"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Create virtual environment: python -m venv venv"
	@echo "  2. Activate it: source venv/bin/activate"
	@echo "  3. Install dependencies: make install"
	@echo "  4. Pull Ollama model: ollama pull mistral:latest"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"
	@echo ""
	@echo "Verify installation:"
	@echo "  python -c 'import fastapi, streamlit; print(\"✓ All packages installed\")'"

# Start FastAPI server
api:
	@echo "🚀 Starting FastAPI server on http://localhost:8000"
	@echo "📚 API docs: http://localhost:8000/docs"
	@echo ""
	uvicorn src.patent_assistant.api.main:app --reload --host 0.0.0.0 --port 8000

# Launch Streamlit UI
ui:
	@echo "🚀 Starting Streamlit UI on http://localhost:8501"
	@echo ""
	streamlit run src/patent_assistant/ui/main.py --server.port 8501

# Start both servers
start:
	@echo "🚀 Starting both API and UI servers..."
	@echo "📡 API: http://localhost:8000"
	@echo "🖥️  UI:  http://localhost:8501"
	@echo ""
	@echo "Press Ctrl+C to stop both servers"
	@echo ""
	./start_servers.sh

# Run comprehensive system tests
test:
	@echo "🧪 Running comprehensive system tests..."
	@echo ""
	@echo "⚠️  Ensure servers are running first:"
	@echo "   Terminal 1: make api"
	@echo "   Terminal 2: make ui"
	@echo ""
	python run_tests.py

# Run all tests (unit + system)
test-all:
	@echo "🧪 Running all tests..."
	@echo ""
	@echo "Running unit tests..."
	pytest src/patent_assistant/tests/ -v
	@echo ""
	@echo "Running system tests..."
	python run_tests.py

# Lint code
lint:
	@echo "🔍 Running linting checks..."
	@echo ""
	@echo "Checking with flake8..."
	-flake8 src/patent_assistant/ --count --show-source --statistics || true
	@echo ""
	@echo "Checking with black (dry-run)..."
	-black src/patent_assistant/ --check || true
	@echo ""
	@echo "Checking with isort (dry-run)..."
	-isort src/patent_assistant/ --check-only || true

# Format code
format:
	@echo "✨ Formatting code..."
	@echo ""
	@echo "Running black..."
	black src/patent_assistant/
	@echo ""
	@echo "Running isort..."
	isort src/patent_assistant/
	@echo ""
	@echo "✅ Code formatting complete"

# Clean up
clean:
	@echo "🧹 Cleaning up temporary files..."
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*~" -delete
	@echo "✅ Cleanup complete"

# Quick start for new users
quickstart: setup
	@echo ""
	@echo "📦 Quick Start Guide:"
	@echo ""
	@echo "1. Install Ollama (if not installed):"
	@echo "   Visit: https://ollama.ai/download"
	@echo ""
	@echo "2. Pull the Mistral model:"
	@echo "   ollama pull mistral:latest"
	@echo ""
	@echo "3. Install Python dependencies:"
	@echo "   make install"
	@echo ""
	@echo "4. Start the servers:"
	@echo "   make start"
	@echo ""
	@echo "5. Access the application:"
	@echo "   UI:  http://localhost:8501"
	@echo "   API: http://localhost:8000/docs"
	@echo ""
	@echo "6. Run tests:"
	@echo "   make test"

# Show system status
status:
	@echo "📊 System Status Check"
	@echo ""
	@echo "Python version:"
	@python --version
	@echo ""
	@echo "Ollama status:"
	@ollama list 2>/dev/null || echo "❌ Ollama not installed or not running"
	@echo ""
	@echo "API server:"
	@curl -s http://localhost:8000/health > /dev/null && echo "✅ Running" || echo "❌ Not running"
	@echo ""
	@echo "UI server:"
	@curl -s http://localhost:8501 > /dev/null && echo "✅ Running" || echo "❌ Not running"
