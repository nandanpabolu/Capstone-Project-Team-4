#!/usr/bin/env python3
"""
Comprehensive Test Runner for Patent Partners Assistant

This script runs all system tests and provides a clear summary.
Run this to verify the entire system is working correctly.
"""

import sys
import time
import requests
from typing import Dict, Tuple

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

API_BASE = "http://localhost:8000"

# Sample invention for testing
SAMPLE_INVENTION = """
A smart delivery drone system that uses advanced computer vision and machine learning 
to navigate obstacles in urban environments. The drone can autonomously detect and avoid 
birds, buildings, power lines, and other aircraft.

Key features:
- 360-degree obstacle detection using multiple cameras
- AI-powered flight path optimization
- Secure package compartment with biometric verification
- Real-time communication with ground control
"""


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")


def print_test(test_name: str):
    """Print test name."""
    print(f"{Colors.BOLD}Testing:{Colors.END} {test_name}... ", end='', flush=True)


def print_success(message: str = ""):
    """Print success message."""
    print(f"{Colors.GREEN}✓ PASS{Colors.END}", end='')
    if message:
        print(f" {Colors.GREEN}{message}{Colors.END}")
    else:
        print()


def print_failure(message: str = ""):
    """Print failure message."""
    print(f"{Colors.RED}✗ FAIL{Colors.END}", end='')
    if message:
        print(f" {Colors.RED}{message}{Colors.END}")
    else:
        print()


def print_warning(message: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.END}")


def test_api_health() -> Tuple[bool, str]:
    """Test API health endpoint."""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                ollama_status = data.get("ollama_available", False)
                return True, f"API v{data.get('version', 'unknown')}, Ollama: {ollama_status}"
            else:
                return False, f"API unhealthy: {data.get('status')}"
        else:
            return False, f"Status code: {response.status_code}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to API - is it running?"
    except Exception as e:
        return False, str(e)


def test_memo_generation() -> Tuple[bool, str]:
    """Test memo generation endpoint."""
    try:
        payload = {
            "invention_description": SAMPLE_INVENTION,
            "context_chunks": None,
            "include_citations": True,
            "max_tokens": 1500,
            "temperature": 0.7,
        }
        
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/generate/memo",
            json=payload,
            timeout=180
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            draft_len = len(result.get("draft", ""))
            if draft_len > 100:
                return True, f"{elapsed:.1f}s, {draft_len} chars"
            else:
                return False, "Output too short"
        else:
            return False, f"Status {response.status_code}: {response.text[:100]}"
    except requests.exceptions.Timeout:
        return False, "Request timed out (>3 min)"
    except Exception as e:
        return False, str(e)[:100]


def test_draft_generation() -> Tuple[bool, str]:
    """Test draft generation endpoint."""
    try:
        payload = {
            "invention_description": SAMPLE_INVENTION,
            "context_chunks": None,
            "include_citations": True,
            "max_tokens": 2000,
            "temperature": 0.7,
        }
        
        start_time = time.time()
        response = requests.post(
            f"{API_BASE}/generate/draft",
            json=payload,
            timeout=180
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            draft_len = len(result.get("draft", ""))
            sections = len(result.get("sections", []))
            if draft_len > 100:
                return True, f"{elapsed:.1f}s, {draft_len} chars, {sections} sections"
            else:
                return False, "Output too short"
        else:
            return False, f"Status {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Request timed out (>3 min)"
    except Exception as e:
        return False, str(e)[:100]


def test_export_endpoint() -> Tuple[bool, str]:
    """Test export endpoint."""
    try:
        payload = {
            "content": "# Test Document\n\nThis is a test.",
            "filename": "test_export.docx",
            "document_type": "draft"
        }
        
        response = requests.post(
            f"{API_BASE}/export/docx",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Export successful"
        else:
            return False, f"Status {response.status_code}"
    except Exception as e:
        return False, str(e)[:100]


def test_error_handling() -> Tuple[bool, str]:
    """Test that API properly handles invalid requests."""
    try:
        # Test with empty description
        payload = {
            "invention_description": "",
            "max_tokens": 1000,
        }
        
        response = requests.post(
            f"{API_BASE}/generate/memo",
            json=payload,
            timeout=5
        )
        
        # Should reject with 400 or 422
        if response.status_code in [400, 422]:
            return True, "Validation working"
        else:
            return False, f"Expected 400/422, got {response.status_code}"
    except Exception as e:
        return False, str(e)[:100]


def run_unit_tests() -> Tuple[bool, str]:
    """Run pytest unit tests."""
    try:
        import subprocess
        result = subprocess.run(
            ["pytest", "src/patent_assistant/tests/", "-v", "--tb=short"],
            capture_output=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True, "All unit tests passed"
        else:
            # Count failures
            output = result.stdout.decode()
            if "failed" in output.lower():
                return False, "Some unit tests failed"
            return False, "Unit tests did not pass"
    except FileNotFoundError:
        return False, "pytest not found - run: pip install pytest"
    except Exception as e:
        return False, str(e)[:100]


def main():
    """Run all tests and report results."""
    print_header("PATENT PARTNERS ASSISTANT - TEST SUITE")
    
    print(f"{Colors.BOLD}System Test Runner{Colors.END}")
    print(f"API Base URL: {API_BASE}\n")
    
    # Track results
    results = {}
    
    # Test 1: API Health
    print_test("API Health Check")
    success, message = test_api_health()
    results["health"] = success
    if success:
        print_success(message)
    else:
        print_failure(message)
        print(f"\n{Colors.RED}Cannot proceed without API. Please start the API server:{Colors.END}")
        print(f"{Colors.YELLOW}  make api{Colors.END}")
        print(f"{Colors.YELLOW}  or: uvicorn src.patent_assistant.api.main:app --host 0.0.0.0 --port 8000{Colors.END}\n")
        sys.exit(1)
    
    # Test 2: Unit Tests
    print_test("Unit Tests (Pydantic Models)")
    success, message = run_unit_tests()
    results["unit_tests"] = success
    if success:
        print_success(message)
    else:
        print_failure(message)
    
    # Test 3: Memo Generation
    print_test("Memo Generation")
    success, message = test_memo_generation()
    results["memo"] = success
    if success:
        print_success(message)
    else:
        print_failure(message)
    
    # Test 4: Draft Generation
    print_test("Patent Draft Generation")
    success, message = test_draft_generation()
    results["draft"] = success
    if success:
        print_success(message)
    else:
        print_failure(message)
    
    # Test 5: Export
    print_test("Document Export (DOCX)")
    success, message = test_export_endpoint()
    results["export"] = success
    if success:
        print_success(message)
    else:
        print_failure(message)
    
    # Test 6: Error Handling
    print_test("Error Handling & Validation")
    success, message = test_error_handling()
    results["validation"] = success
    if success:
        print_success(message)
    else:
        print_failure(message)
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Tests Run:    {total}")
    print(f"{Colors.GREEN}Tests Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}Tests Failed: {total - passed}{Colors.END}")
    print(f"Success Rate: {passed/total*100:.0f}%\n")
    
    # Detailed results
    print(f"{Colors.BOLD}Detailed Results:{Colors.END}")
    for test_name, passed in results.items():
        status = f"{Colors.GREEN}✓ PASS{Colors.END}" if passed else f"{Colors.RED}✗ FAIL{Colors.END}"
        print(f"  {test_name:20s} {status}")
    
    print()
    
    # Final verdict
    if all(results.values()):
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! System is working correctly.{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠️  SOME TESTS FAILED. Please check the errors above.{Colors.END}\n")
        
        # Helpful hints
        if not results.get("memo") or not results.get("draft"):
            print(f"{Colors.YELLOW}Generation tests failed. Common issues:{Colors.END}")
            print(f"  - Is Ollama running? Check: ollama list")
            print(f"  - Is Mistral model installed? Run: ollama pull mistral:latest")
            print(f"  - Check API logs for detailed error messages\n")
        
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Tests interrupted by user.{Colors.END}\n")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}\n")
        sys.exit(1)

