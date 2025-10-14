#!/bin/bash

# Patent Partners Assistant - Server Startup Script
# This script starts both the API and UI servers without reload issues

echo "🚀 Starting Patent Partners Assistant..."

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated. Activating now..."
    source venv/bin/activate
fi

# Start API server in background (without reload to avoid file watching issues)
echo "📡 Starting FastAPI server on http://localhost:8000..."
uvicorn src.patent_assistant.api.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

# Wait a moment for API to start
sleep 3

# Start Streamlit UI
echo "🖥️  Starting Streamlit UI on http://localhost:8501..."
echo "Press Ctrl+C to stop both servers"
streamlit run src/patent_assistant/ui/main.py --server.port 8501 &
UI_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping servers..."
    kill $API_PID 2>/dev/null
    kill $UI_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C
trap cleanup SIGINT

# Wait for both processes
wait
