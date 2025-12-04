#!/usr/bin/env python3
"""
Master Test Runner for Squirrel Spotter USC
Runs all test suites and provides a comprehensive summary
"""

import sys
import os
import unittest
import time
import requests
from datetime import datetime

# Add test directories to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuration
BASE_URL = "http://localhost:8080"
TEST_SUITES = [
    ("Account Creation Tests", "account_creation_tests.test_account_creation"),
    ("Pin API Tests", "pin_tests.test_pins"),
    ("Leaderboard API Tests", "leaderboard_tests.test_leaderboard_api"),
    ("WebSocket Tests", "websocket_tests.test_websocket"),
]


def check_backend():
    """Check if the backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/api/pins/weekly", timeout=5)
        return True
    except requests.exceptions.ConnectionError:
        return False


def run_all_tests():
    """Run all test suites"""
    
    print("\n" + "="*70)
    print("  SQUIRREL SPOTTER USC - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Backend URL: {BASE_URL}")
    print("="*70 + "\n")
    
    # Check backend
    print("Checking backend status...", end=" ")
    if not check_backend():
        print("✗ FAILED\n")
        print("="*70)
        print("  ERROR: Backend is not running!")
        print("="*70)
        print("\n  Please start the backend first:\n")
        print("    cd backend")
        print("    mvn spring-boot:run")
        print("\n  Wait for: 'Started SquirrelSpotterApplication'\n")
        print("="*70 + "\n")
        return 1
    print("✓ OK\n")
    
    # Track results
    total_tests = 0
    total_failures = 0
    total_errors = 0
    suite_results = []
    
    start_time = time.time()
    
    # Run each test suite
    for suite_name, module_name in TEST_SUITES:
        print("\n" + "-"*70)
        print(f"  Running: {suite_name}")
        print("-"*70 + "\n")
        
        try:
            # Import the test module
            module = __import__(module_name, fromlist=[''])
            
            # Load tests from the module
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(module)
            
            # Run tests
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            # Track results
            tests = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)
            
            total_tests += tests
            total_failures += failures
            total_errors += errors
            
            suite_results.append({
                "name": suite_name,
                "tests": tests,
                "failures": failures,
                "errors": errors,
                "success": failures == 0 and errors == 0
            })
            
        except ImportError as e:
            print(f"  ✗ Could not import {module_name}: {e}")
            suite_results.append({
                "name": suite_name,
                "tests": 0,
                "failures": 0,
                "errors": 1,
                "success": False,
                "error_msg": str(e)
            })
            total_errors += 1
        except Exception as e:
            print(f"  ✗ Error running {suite_name}: {e}")
            suite_results.append({
                "name": suite_name,
                "tests": 0,
                "failures": 0,
                "errors": 1,
                "success": False,
                "error_msg": str(e)
            })
            total_errors += 1
    
    elapsed_time = time.time() - start_time
    
    # Print summary
    print("\n\n" + "="*70)
    print("  TEST RESULTS SUMMARY")
    print("="*70 + "\n")
    
    for result in suite_results:
        status = "✓ PASS" if result["success"] else "✗ FAIL"
        print(f"  {status}  {result['name']}")
        print(f"         Tests: {result['tests']}, Failures: {result['failures']}, Errors: {result['errors']}")
        if "error_msg" in result:
            print(f"         Error: {result['error_msg']}")
        print()
    
    print("-"*70)
    print(f"\n  Total Tests:    {total_tests}")
    print(f"  Total Failures: {total_failures}")
    print(f"  Total Errors:   {total_errors}")
    print(f"  Success Rate:   {((total_tests - total_failures - total_errors) / max(total_tests, 1) * 100):.1f}%")
    print(f"  Time Elapsed:   {elapsed_time:.2f}s")
    print()
    
    if total_failures == 0 and total_errors == 0:
        print("  " + "🎉 ALL TESTS PASSED! 🎉")
    else:
        print("  " + "⚠️  SOME TESTS FAILED")
    
    print("\n" + "="*70)
    print(f"  Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    return 1 if (total_failures > 0 or total_errors > 0) else 0


if __name__ == "__main__":
    sys.exit(run_all_tests())

