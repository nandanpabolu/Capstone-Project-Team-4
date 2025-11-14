"""
System Integration Tests for Patent Partners Assistant.

Tests the complete system including API endpoints, generation, and export.
"""

import requests
import time
import pytest
from typing import Dict, Any

API_BASE = "http://localhost:8000"
TIMEOUT = 240  # 4 minutes for generation tests

# Sample invention for testing
SAMPLE_INVENTION = """
A smart delivery drone system that uses advanced computer vision and machine learning 
to navigate obstacles in urban environments. The drone can autonomously detect and avoid 
birds, buildings, power lines, and other aircraft. It uses a combination of LIDAR, cameras, 
and GPS for navigation. The system includes a package delivery mechanism with secure locking 
and real-time tracking capabilities.

Key features:
- 360-degree obstacle detection using multiple cameras
- AI-powered flight path optimization
- Secure package compartment with biometric verification
- Real-time communication with ground control
- Weather-adaptive flight algorithms
"""

SAMPLE_MEDICAL_DEVICE = """
A smart wearable health monitoring system that uses multiple biometric sensors 
and AI to predict medical emergencies before they occur. 

Technical Components:
- ECG sensor array with 12-lead capability
- Pulse oximeter for blood oxygen monitoring
- 3-axis accelerometer for fall detection
- Temperature sensor
- Galvanic skin response sensor

AI/ML Features:
- Real-time anomaly detection using LSTM neural networks
- Predictive models trained on 1M+ patient records
- Pattern recognition for early warning signs (48-72 hours advance)
- Personalized baseline learning

Safety Features:
- Automatic emergency services notification with GPS location
- Family/caregiver alerts
- Medical history transmission to first responders
- Battery backup (72 hours)
"""


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test that API health endpoint is responsive."""
        response = requests.get(f"{API_BASE}/health", timeout=5)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "offline_mode" in data
        assert "timestamp" in data
    
    def test_health_check_ollama_status(self):
        """Test that health check includes Ollama status."""
        response = requests.get(f"{API_BASE}/health", timeout=5)
        data = response.json()
        
        assert "ollama_available" in data
        # If ollama is available, it should be True
        if data.get("ollama_available"):
            assert isinstance(data["ollama_available"], bool)


class TestMemoGeneration:
    """Test invention memo generation."""
    
    def test_memo_generation_basic(self):
        """Test basic memo generation with sample invention."""
        payload = {
            "invention_description": SAMPLE_INVENTION,
            "context_chunks": None,
            "include_citations": True,
            "max_tokens": 2000,
            "temperature": 0.7,
        }
        
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/generate/memo",
            json=payload,
            timeout=TIMEOUT
        )
        elapsed = time.time() - start_time
        
        assert response.status_code == 200, f"Failed with: {response.text}"
        
        result = response.json()
        assert "draft" in result
        assert "generation_time_ms" in result
        assert "model_used" in result
        assert "citations" in result
        
        # Check content quality
        assert len(result["draft"]) > 100, "Memo too short"
        assert isinstance(result["citations"], list)
        
        print(f"\n✅ Memo generation completed in {elapsed:.1f}s")
        print(f"   Draft length: {len(result['draft'])} chars")
        print(f"   Citations: {len(result['citations'])}")
    
    def test_memo_generation_detailed(self):
        """Test memo generation with more complex input."""
        payload = {
            "invention_description": SAMPLE_MEDICAL_DEVICE,
            "context_chunks": None,
            "include_citations": True,
            "max_tokens": 3500,
            "temperature": 0.7,
        }
        
        response = requests.post(
            f"{API_BASE}/generate/memo",
            json=payload,
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        result = response.json()
        
        # Check for comprehensive output
        assert len(result["draft"]) > 500, "Detailed memo too short"
        
        # Check for key sections (case-insensitive)
        draft_lower = result["draft"].lower()
        assert any(term in draft_lower for term in ["summary", "overview", "invention"])
        
        print(f"\n✅ Detailed memo generated")
        print(f"   Draft length: {len(result['draft'])} chars")


class TestDraftGeneration:
    """Test patent draft generation."""
    
    def test_draft_generation_basic(self):
        """Test basic patent draft generation."""
        payload = {
            "invention_description": SAMPLE_INVENTION,
            "context_chunks": None,
            "include_citations": True,
            "max_tokens": 3000,
            "temperature": 0.7,
        }
        
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/generate/draft",
            json=payload,
            timeout=TIMEOUT
        )
        elapsed = time.time() - start_time
        
        assert response.status_code == 200, f"Failed with: {response.text}"
        
        result = response.json()
        assert "draft" in result
        assert "sections" in result
        assert "generation_time_ms" in result
        assert "model_used" in result
        
        # Check content
        assert len(result["draft"]) > 100, "Draft too short"
        assert isinstance(result["sections"], list)
        assert len(result["sections"]) > 0, "No sections generated"
        
        print(f"\n✅ Draft generation completed in {elapsed:.1f}s")
        print(f"   Draft length: {len(result['draft'])} chars")
        print(f"   Sections: {', '.join(result['sections'][:5])}")
    
    def test_draft_generation_comprehensive(self):
        """Test comprehensive patent draft generation."""
        payload = {
            "invention_description": SAMPLE_MEDICAL_DEVICE,
            "context_chunks": None,
            "include_citations": True,
            "max_tokens": 4500,
            "temperature": 0.7,
        }
        
        response = requests.post(
            f"{API_BASE}/generate/draft",
            json=payload,
            timeout=TIMEOUT
        )
        
        assert response.status_code == 200
        result = response.json()
        
        # Check for USPTO-compliant sections
        draft_lower = result["draft"].lower()
        expected_sections = ["title", "abstract", "background", "claims"]
        found_sections = [s for s in expected_sections if s in draft_lower]
        
        assert len(found_sections) >= 2, f"Missing key sections. Found: {found_sections}"
        
        print(f"\n✅ Comprehensive draft generated")
        print(f"   Draft length: {len(result['draft'])} chars")
        print(f"   Sections found: {', '.join(found_sections)}")


class TestExportEndpoint:
    """Test document export functionality."""
    
    def test_export_docx(self):
        """Test DOCX export endpoint."""
        payload = {
            "content": "# Test Patent Draft\n\nThis is a test document.",
            "filename": "test_export.docx",
            "document_type": "draft"
        }
        
        response = requests.post(
            f"{API_BASE}/export/docx",
            json=payload,
            timeout=10
        )
        
        assert response.status_code == 200
        
        # Response should be a file or JSON with file path
        if response.headers.get("content-type") == "application/json":
            result = response.json()
            assert "file_path" in result or "filename" in result
            print(f"\n✅ Export successful: {result.get('filename', 'document created')}")
        else:
            # Binary response - file download
            assert len(response.content) > 0
            print(f"\n✅ Export successful: {len(response.content)} bytes")


class TestGenerationOptions:
    """Test generation with different options."""
    
    def test_temperature_variation(self):
        """Test generation with different temperature settings."""
        for temp in [0.5, 0.7, 0.9]:
            payload = {
                "invention_description": SAMPLE_INVENTION[:200],
                "context_chunks": None,
                "max_tokens": 500,
                "temperature": temp,
            }
            
            response = requests.post(
                f"{API_BASE}/generate/memo",
                json=payload,
                timeout=120
            )
            
            assert response.status_code == 200
            result = response.json()
            assert len(result["draft"]) > 0
            
            print(f"✅ Temperature {temp}: {len(result['draft'])} chars generated")
    
    def test_token_limits(self):
        """Test generation with different token limits."""
        for max_tokens in [500, 1000, 2000]:
            payload = {
                "invention_description": SAMPLE_INVENTION,
                "context_chunks": None,
                "max_tokens": max_tokens,
                "temperature": 0.7,
            }
            
            response = requests.post(
                f"{API_BASE}/generate/memo",
                json=payload,
                timeout=120
            )
            
            assert response.status_code == 200
            result = response.json()
            
            print(f"✅ Max tokens {max_tokens}: {len(result['draft'])} chars generated")


class TestErrorHandling:
    """Test error handling and validation."""
    
    def test_empty_description(self):
        """Test that empty descriptions are rejected."""
        payload = {
            "invention_description": "",
            "max_tokens": 1000,
        }
        
        response = requests.post(
            f"{API_BASE}/generate/memo",
            json=payload,
            timeout=10
        )
        
        # Should return 422 (validation error) or 400 (bad request)
        assert response.status_code in [400, 422]
    
    def test_missing_required_fields(self):
        """Test that missing required fields are rejected."""
        payload = {
            "max_tokens": 1000,
        }
        
        response = requests.post(
            f"{API_BASE}/generate/memo",
            json=payload,
            timeout=10
        )
        
        assert response.status_code in [400, 422]
    
    def test_invalid_endpoint(self):
        """Test that invalid endpoints return 404."""
        response = requests.get(
            f"{API_BASE}/invalid/endpoint",
            timeout=5
        )
        
        assert response.status_code == 404


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])

