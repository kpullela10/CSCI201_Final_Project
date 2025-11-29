#!/usr/bin/env python3
"""
Test Runner for Account Creation Tests
Verifies authentication endpoints are working correctly
"""

import sys
import unittest
import requests
from test_account_creation import TestAccountCreation

def check_backend_running():
    """Check if backend is running before running tests"""
    print("Checking if backend is running at http://localhost:8080...")
    try:
        response = requests.get("http://localhost:8080", timeout=5)
        print("✓ Backend is running!\n")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Backend is not running!")
        print("\nPlease start the backend first:")
        print("  cd backend")
        print("  mvn spring-boot:run")
        print("\nThen run these tests again.\n")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}\n")
        return False

if __name__ == "__main__":
    # Check backend is running
    if not check_backend_running():
        sys.exit(1)

    # Run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestAccountCreation)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
