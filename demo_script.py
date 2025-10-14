#!/usr/bin/env python3
"""
Demo Script for Patent Partners Assistant

This script demonstrates all the key features for your demo tomorrow.
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def demo_health_check():
    """Demo the health check endpoint."""
    print("🔍 Testing Health Check...")
    response = requests.get(f"{API_BASE_URL}/health")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {data['status']}")
        print(f"✅ Version: {data['version']}")
        print(f"✅ Offline Mode: {data['offline_mode']}")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def demo_search():
    """Demo the search functionality."""
    print("\n🔍 Testing Patent Search...")
    search_data = {
        "query": "machine learning algorithm for patent analysis",
        "top_k": 10,
        "include_abstract": True
    }
    
    response = requests.post(f"{API_BASE_URL}/search", json=search_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Search completed in {data['query_time_ms']}ms")
        print(f"✅ Found {data['total_results']} results")
        print(f"✅ Message: {data['message']}")
        return True
    else:
        print(f"❌ Search failed: {response.status_code}")
        return False

def demo_rag_context():
    """Demo the RAG context retrieval."""
    print("\n🧠 Testing RAG Context Retrieval...")
    rag_data = {
        "query": "artificial intelligence in patent classification",
        "top_k": 5
    }
    
    response = requests.post(f"{API_BASE_URL}/rag/context", json=rag_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {data['total_chunks']} context chunks")
        print(f"✅ Query: {data['query']}")
        print(f"✅ Retrieval time: {data['retrieval_time_ms']}ms")
        return True
    else:
        print(f"❌ RAG context failed: {response.status_code}")
        return False

def demo_memo_generation():
    """Demo invention memo generation."""
    print("\n📝 Testing Invention Memo Generation...")
    memo_data = {
        "invention_description": "A novel machine learning system that automatically classifies patent documents using transformer-based neural networks and provides real-time prior art analysis for patent attorneys.",
        "include_citations": True,
        "max_tokens": 1000
    }
    
    response = requests.post(f"{API_BASE_URL}/generate/memo", json=memo_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Memo generated in {data['generation_time_ms']}ms")
        print(f"✅ Model used: {data['model_used']}")
        print(f"✅ Sections: {', '.join(data['sections'])}")
        print(f"✅ Citations: {len(data['citations'])} references")
        return True
    else:
        print(f"❌ Memo generation failed: {response.status_code}")
        return False

def demo_draft_generation():
    """Demo patent draft generation."""
    print("\n📄 Testing Patent Draft Generation...")
    draft_data = {
        "invention_description": "An AI-powered patent analysis system that uses natural language processing to identify prior art and generate patent claims automatically.",
        "include_citations": True,
        "max_tokens": 1500
    }
    
    response = requests.post(f"{API_BASE_URL}/generate/draft", json=draft_data)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Draft generated in {data['generation_time_ms']}ms")
        print(f"✅ Model used: {data['model_used']}")
        print(f"✅ Sections: {', '.join(data['sections'])}")
        print(f"✅ Citations: {len(data['citations'])} references")
        return True
    else:
        print(f"❌ Draft generation failed: {response.status_code}")
        return False

def main():
    """Run the complete demo."""
    print("🚀 Patent Partners Assistant - Demo Script")
    print("=" * 50)
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ API server is not running!")
            print("Please start it with: make api")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to API server!")
        print("Please start it with: make api")
        return
    
    print("✅ API server is running!")
    
    # Run all demos
    demos = [
        demo_health_check,
        demo_search,
        demo_rag_context,
        demo_memo_generation,
        demo_draft_generation
    ]
    
    passed = 0
    total = len(demos)
    
    for demo in demos:
        try:
            if demo():
                passed += 1
            time.sleep(1)  # Brief pause between demos
        except Exception as e:
            print(f"❌ Demo failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Demo Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems working perfectly!")
        print("\n📋 Demo Checklist:")
        print("✅ API Server: http://localhost:8000")
        print("✅ Streamlit UI: http://localhost:8501")
        print("✅ API Documentation: http://localhost:8000/docs")
        print("✅ All endpoints responding correctly")
        print("✅ Ready for tomorrow's demo!")
    else:
        print("⚠️  Some issues detected. Check the logs above.")

if __name__ == "__main__":
    main()
