#!/usr/bin/env python3
"""
Quick test script for Home Controller API
Run this after starting the server to verify all endpoints work
"""

import requests
import sys
from typing import Dict

BASE_URL = "http://localhost:8000"


def test_endpoint(method: str, endpoint: str, description: str) -> bool:
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:  # POST
            response = requests.post(url, timeout=5)
        
        if response.status_code == 200:
            print(f"✓ {description}")
            return True
        else:
            print(f"✗ {description} (Status: {response.status_code})")
            print(f"  Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ {description} (Connection Error - Is server running?)")
        return False
    except Exception as e:
        print(f"✗ {description} (Error: {e})")
        return False


def main():
    print("=" * 60)
    print("Home Controller API Test")
    print("=" * 60)
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        if response.status_code == 200:
            print("✓ Server is running")
            print()
        else:
            print("✗ Server responded with unexpected status")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server at", BASE_URL)
        print("  Please start the server with: uvicorn src.main:app --reload")
        sys.exit(1)
    
    results = []
    
    # Test Light endpoints
    print("Testing Light Endpoints:")
    print("-" * 60)
    results.append(test_endpoint("GET", "/light/modes", "GET /light/modes"))
    results.append(test_endpoint("POST", "/light/on", "POST /light/on"))
    results.append(test_endpoint("POST", "/light/off", "POST /light/off"))
    results.append(test_endpoint("POST", "/light/bright", "POST /light/bright"))
    results.append(test_endpoint("POST", "/light/dark", "POST /light/dark"))
    results.append(test_endpoint("POST", "/light/all-bright", "POST /light/all-bright"))
    print()
    
    # Test AC endpoints
    print("Testing AC Endpoints:")
    print("-" * 60)
    results.append(test_endpoint("GET", "/ac/status", "GET /ac/status"))
    results.append(test_endpoint("POST", "/ac/aircon/on", "POST /ac/aircon/on"))
    results.append(test_endpoint("POST", "/ac/heater/on", "POST /ac/heater/on"))
    results.append(test_endpoint("POST", "/ac/off", "POST /ac/off"))
    results.append(test_endpoint("POST", "/ac/aircon/temp/up", "POST /ac/aircon/temp/up"))
    results.append(test_endpoint("POST", "/ac/heater/temp/up", "POST /ac/heater/temp/up"))
    results.append(test_endpoint("POST", "/ac/heater/temp/down", "POST /ac/heater/temp/down"))
    results.append(test_endpoint("POST", "/ac/timer/on", "POST /ac/timer/on"))
    results.append(test_endpoint("POST", "/ac/timer/up", "POST /ac/timer/up"))
    results.append(test_endpoint("POST", "/ac/timer/down", "POST /ac/timer/down"))
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Test Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print(f"✗ {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)

