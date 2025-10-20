"""
Test script for generation endpoints.

Tests memo and draft generation with sample invention description.
"""

import requests
import json
import time

API_BASE = "http://localhost:8000"

# Sample invention description
INVENTION = """
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

def test_memo_generation():
    """Test invention memo generation."""
    print("\n" + "="*80)
    print("TESTING: Invention Memo Generation")
    print("="*80 + "\n")
    
    # Prepare request
    payload = {
        "invention_description": INVENTION,
        "context_chunks": None,  # No prior art for this test
        "include_citations": True,
        "max_tokens": 2000,
        "temperature": 0.7,
    }
    
    print("Sending request to /generate/memo...")
    print(f"Invention length: {len(INVENTION)} chars\n")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_BASE}/generate/memo",
            json=payload,
            timeout=180  # 3 minutes
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS ({elapsed:.1f}s)")
            print(f"\nGeneration time: {result['generation_time_ms']:.0f}ms")
            print(f"Model used: {result['model_used']}")
            print(f"Memo length: {len(result['draft'])} chars")
            print(f"Citations: {len(result['citations'])}")
            
            print("\n" + "-"*80)
            print("GENERATED MEMO:")
            print("-"*80)
            print(result['draft'][:500] + "..." if len(result['draft']) > 500 else result['draft'])
            print("-"*80 + "\n")
            
            return True
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ FAILED: Request timed out (> 3 minutes)")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_draft_generation():
    """Test patent draft generation."""
    print("\n" + "="*80)
    print("TESTING: Patent Draft Generation")
    print("="*80 + "\n")
    
    # Prepare request
    payload = {
        "invention_description": INVENTION,
        "context_chunks": None,
        "include_citations": True,
        "max_tokens": 3000,
        "temperature": 0.7,
    }
    
    print("Sending request to /generate/draft...")
    print(f"Invention length: {len(INVENTION)} chars\n")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_BASE}/generate/draft",
            json=payload,
            timeout=180
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS ({elapsed:.1f}s)")
            print(f"\nGeneration time: {result['generation_time_ms']:.0f}ms")
            print(f"Model used: {result['model_used']}")
            print(f"Draft length: {len(result['draft'])} chars")
            print(f"Sections: {', '.join(result['sections'])}")
            print(f"Citations: {len(result['citations'])}")
            
            print("\n" + "-"*80)
            print("GENERATED DRAFT (first 800 chars):")
            print("-"*80)
            print(result['draft'][:800] + "...")
            print("-"*80 + "\n")
            
            return True
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ FAILED: Request timed out (> 3 minutes)")
        return False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_health():
    """Test health endpoint."""
    print("\n" + "="*80)
    print("TESTING: Health Check")
    print("="*80 + "\n")
    
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API is {result['status']}")
            print(f"   Version: {result['version']}")
            print(f"   Offline mode: {result['offline_mode']}")
            return result['status'] == 'healthy'
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("# GENERATION ENDPOINT TEST SUITE")
    print("#"*80)
    
    # Test health first
    if not test_health():
        print("\n❌ API is not healthy. Exiting.")
        exit(1)
    
    # Run tests
    results = {
        "memo": test_memo_generation(),
        "draft": test_draft_generation(),
    }
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Memo Generation:  {'✅ PASSED' if results['memo'] else '❌ FAILED'}")
    print(f"Draft Generation: {'✅ PASSED' if results['draft'] else '❌ FAILED'}")
    print("="*80 + "\n")
    
    if all(results.values()):
        print("🎉 All tests passed! Generation layer is working!\n")
        exit(0)
    else:
        print("⚠️  Some tests failed. Check logs above.\n")
        exit(1)

