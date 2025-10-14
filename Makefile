# Patent Partners Assistant - Makefile
# Team 4 Capstone Project

.PHONY: help setup install ingest index api ui test clean lint format

# Default target
help:
	@echo "Patent Partners Assistant - Available Commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  setup     - Initialize project and create directories"
	@echo "  install   - Install dependencies with Poetry"
	@echo ""
	@echo "Data Processing:"
	@echo "  ingest    - Ingest patent data from USPTO XML"
	@echo "  index     - Build BM25 and FAISS search indexes"
	@echo ""
	@echo "Development:"
	@echo "  api       - Start FastAPI server"
	@echo "  ui        - Launch Streamlit UI"
	@echo "  test      - Run unit tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint      - Run linting checks"
	@echo "  format    - Format code with black and isort"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean     - Clean up temporary files and logs"

# Setup project directories and environment
setup:
	@echo "Setting up Patent Partners Assistant..."
	@mkdir -p data/{raw,processed}
	@mkdir -p logs indexes config docs scripts
	@echo "✅ Project directories created"
	@echo "Run 'make install' to install dependencies"

# Install dependencies
install:
	@echo "Installing dependencies with pip..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"
	@echo "Run 'source venv/bin/activate' to activate virtual environment"

# Ingest patent data
ingest:
	@echo "Ingesting patent data..."
	python scripts/ingest_patents.py
	@echo "✅ Patent data ingested"

# Build search indexes
index:
	@echo "Building search indexes..."
	python scripts/build_indexes.py
	@echo "✅ Search indexes built"

# Start FastAPI server
api:
	@echo "Starting FastAPI server..."
	uvicorn src.patent_assistant.api.main:app --reload --host 0.0.0.0 --port 8000

# Launch Streamlit UI
ui:
	@echo "Launching Streamlit UI..."
	streamlit run src/patent_assistant/ui/main.py --server.port 8501

# Run tests
test:
	@echo "Running tests..."
	pytest src/patent_assistant/tests/ -v

# Lint code
lint:
	@echo "Running linting checks..."
	flake8 src/patent_assistant/

# Format code
format:
	@echo "Formatting code..."
	black src/patent_assistant/
	isort src/patent_assistant/

# Clean up
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup complete"

# Development workflow
dev: setup install
	@echo "Development environment ready!"
	@echo "Next steps:"
	@echo "  1. make ingest    # Load patent data"
	@echo "  2. make index     # Build search indexes"
	@echo "  3. make api       # Start API server"
	@echo "  4. make ui        # Launch UI (in another terminal)"
