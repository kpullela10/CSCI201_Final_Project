"""
Comprehensive Leaderboard API Tests for Squirrel Spotter USC
Tests leaderboard retrieval, pagination, sorting, and edge cases
"""

import unittest
import requests
import random
import string
from typing import Dict, List

# Configuration
BASE_URL = "http://localhost:8080"
SIGNUP_ENDPOINT = "/api/auth/signup"
PINS_ENDPOINT = "/api/pins"
LEADERBOARD_ENDPOINT = "/api/leaderboard"
USER_PINS_ENDPOINT = "/api/users/{userID}/pins"
REQUEST_TIMEOUT = 30

# USC Campus Coordinates
USC_CENTER = {"lat": 34.0224, "lng": -118.2851}


def generate_random_suffix():
    """Generate random string for unique test data"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))


def create_test_user():
    """Create a new test user and return credentials and token"""
    suffix = generate_random_suffix()
    user_data = {
        "email": f"leadertest_{suffix}@usc.edu",
        "username": f"leadertest_{suffix}",
        "password": "TestPassword123"
    }
    
    response = requests.post(
        f"{BASE_URL}{SIGNUP_ENDPOINT}",
        json=user_data,
        timeout=REQUEST_TIMEOUT
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to create test user: {response.text}")
    
    data = response.json()
    return {
        "user": data["user"],
        "token": data["token"],
        "credentials": user_data
    }


def get_auth_headers(token: str) -> Dict[str, str]:
    """Get authorization headers with JWT token"""
    return {"Authorization": f"Bearer {token}"}


def create_pin_for_user(token: str, lat_offset: float = 0, lng_offset: float = 0) -> Dict:
    """Create a pin for a user and return the response"""
    headers = get_auth_headers(token)
    form_data = {
        "lat": str(USC_CENTER["lat"] + lat_offset),
        "lng": str(USC_CENTER["lng"] + lng_offset),
        "description": f"Leaderboard test pin"
    }
    
    response = requests.post(
        f"{BASE_URL}{PINS_ENDPOINT}",
        data=form_data,
        headers=headers,
        timeout=REQUEST_TIMEOUT
    )
    return response.json() if response.status_code == 201 else None


class TestLeaderboardBasic(unittest.TestCase):
    """Test suite for basic leaderboard functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        print(f"\n{'='*60}")
        print("Testing Leaderboard Basic Functionality")
        print(f"{'='*60}\n")

    def test_01_get_weekly_leaderboard(self):
        """Test retrieving weekly leaderboard (public endpoint)"""
        print("\n[TEST] Getting weekly leaderboard...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly"},
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check response structure
        self.assertIn("entries", data)
        self.assertIn("totalCount", data)
        self.assertIsInstance(data["entries"], list)
        self.assertIsInstance(data["totalCount"], int)
        
        if len(data["entries"]) > 0:
            entry = data["entries"][0]
            self.assertIn("userID", entry)
            self.assertIn("username", entry)
            self.assertIn("weeklyPins", entry)
            self.assertIn("totalPins", entry)
            print(f"  Found {len(data['entries'])} entries, total count: {data['totalCount']}")
        
        print("  ✓ Weekly leaderboard retrieved successfully")

    def test_02_get_alltime_leaderboard(self):
        """Test retrieving all-time leaderboard"""
        print("\n[TEST] Getting all-time leaderboard...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "all-time"},
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("entries", data)
        self.assertIn("totalCount", data)
        
        if len(data["entries"]) > 0:
            print(f"  Found {len(data['entries'])} entries, total count: {data['totalCount']}")
        
        print("  ✓ All-time leaderboard retrieved successfully")

    def test_03_invalid_leaderboard_type(self):
        """Test that invalid leaderboard type returns error"""
        print("\n[TEST] Testing invalid leaderboard type...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "invalid"},
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("message", data)
        
        print("  ✓ Invalid type properly rejected")

    def test_04_missing_type_parameter(self):
        """Test that missing type parameter returns error"""
        print("\n[TEST] Testing missing type parameter...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            # No type parameter
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        # Should return 400 Bad Request
        self.assertEqual(response.status_code, 400)
        
        print("  ✓ Missing type parameter properly handled")


class TestLeaderboardPagination(unittest.TestCase):
    """Test suite for leaderboard pagination"""

    def test_01_default_pagination(self):
        """Test default pagination values"""
        print("\n[TEST] Testing default pagination...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly"},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Default page size is 20
        self.assertLessEqual(len(data["entries"]), 20)
        
        print(f"  Entries returned: {len(data['entries'])} (max 20)")
        print("  ✓ Default pagination working")

    def test_02_custom_page_size(self):
        """Test custom page size"""
        print("\n[TEST] Testing custom page size...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly", "pageSize": 5},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Should return at most 5 entries
        self.assertLessEqual(len(data["entries"]), 5)
        
        print(f"  Entries returned: {len(data['entries'])} (max 5)")
        print("  ✓ Custom page size working")

    def test_03_page_navigation(self):
        """Test pagination across multiple pages"""
        print("\n[TEST] Testing page navigation...")
        
        # Get page 1
        response1 = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "all-time", "page": 1, "pageSize": 5},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response1.status_code, 200)
        data1 = response1.json()
        
        # Get page 2
        response2 = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "all-time", "page": 2, "pageSize": 5},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json()
        
        # If there are enough entries, pages should be different
        if data1["totalCount"] > 5:
            page1_ids = {e["userID"] for e in data1["entries"]}
            page2_ids = {e["userID"] for e in data2["entries"]}
            self.assertTrue(page1_ids.isdisjoint(page2_ids), 
                "Pages should have different entries")
            print("  Pages have different entries as expected")
        
        print("  ✓ Page navigation working")

    def test_04_invalid_page_number(self):
        """Test that page number < 1 returns error"""
        print("\n[TEST] Testing invalid page number (0)...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly", "page": 0},
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 400)
        
        print("  ✓ Invalid page number rejected")

    def test_05_invalid_page_size(self):
        """Test that page size > 100 returns error"""
        print("\n[TEST] Testing invalid page size (101)...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly", "pageSize": 101},
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 400)
        
        print("  ✓ Invalid page size rejected")

    def test_06_negative_page_size(self):
        """Test that negative page size returns error"""
        print("\n[TEST] Testing negative page size (-1)...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly", "pageSize": -1},
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 400)
        
        print("  ✓ Negative page size rejected")


class TestLeaderboardSorting(unittest.TestCase):
    """Test suite for leaderboard sorting"""

    def test_01_weekly_sorted_by_weekly_pins(self):
        """Test that weekly leaderboard is sorted by weekly pin count (descending)"""
        print("\n[TEST] Testing weekly leaderboard sorting...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly", "pageSize": 50},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        entries = data["entries"]
        if len(entries) > 1:
            # Check descending order by weeklyPins
            for i in range(len(entries) - 1):
                self.assertGreaterEqual(
                    entries[i]["weeklyPins"], 
                    entries[i+1]["weeklyPins"],
                    "Weekly leaderboard should be sorted by weeklyPins descending"
                )
            print(f"  Verified {len(entries)} entries are properly sorted")
        
        print("  ✓ Weekly leaderboard properly sorted")

    def test_02_alltime_sorted_by_total_pins(self):
        """Test that all-time leaderboard is sorted by total pin count (descending)"""
        print("\n[TEST] Testing all-time leaderboard sorting...")
        
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "all-time", "pageSize": 50},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        entries = data["entries"]
        if len(entries) > 1:
            # Check descending order by totalPins
            for i in range(len(entries) - 1):
                self.assertGreaterEqual(
                    entries[i]["totalPins"], 
                    entries[i+1]["totalPins"],
                    "All-time leaderboard should be sorted by totalPins descending"
                )
            print(f"  Verified {len(entries)} entries are properly sorted")
        
        print("  ✓ All-time leaderboard properly sorted")


class TestLeaderboardWithNewUser(unittest.TestCase):
    """Test suite for leaderboard with newly created users"""

    def test_01_new_user_with_pin_appears_on_leaderboard(self):
        """Test that a new user with a pin appears on the leaderboard"""
        print("\n[TEST] Testing new user appears on leaderboard after creating pin...")
        
        # Create a new user
        test_user = create_test_user()
        user_id = test_user["user"]["userID"]
        username = test_user["user"]["username"]
        
        # Create a pin for this user
        pin = create_pin_for_user(test_user["token"])
        self.assertIsNotNone(pin, "Pin creation should succeed")
        
        # Check weekly leaderboard
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly", "pageSize": 100},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Find our user
        user_entry = None
        for entry in data["entries"]:
            if entry["userID"] == user_id:
                user_entry = entry
                break
        
        self.assertIsNotNone(user_entry, f"User {username} should appear on leaderboard")
        self.assertEqual(user_entry["weeklyPins"], 1)
        self.assertEqual(user_entry["totalPins"], 1)
        
        print(f"  User {username} found on leaderboard with 1 pin")
        print("  ✓ New user with pin appears on leaderboard")

    def test_02_user_pin_count_increments(self):
        """Test that creating more pins increments leaderboard count"""
        print("\n[TEST] Testing pin count increments on leaderboard...")
        
        # Create a new user
        test_user = create_test_user()
        user_id = test_user["user"]["userID"]
        
        # Create 3 pins
        for i in range(3):
            pin = create_pin_for_user(test_user["token"], lat_offset=i*0.001)
            self.assertIsNotNone(pin)
        
        # Check leaderboard
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly", "pageSize": 100},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Find our user
        user_entry = None
        for entry in data["entries"]:
            if entry["userID"] == user_id:
                user_entry = entry
                break
        
        self.assertIsNotNone(user_entry)
        self.assertEqual(user_entry["weeklyPins"], 3)
        self.assertEqual(user_entry["totalPins"], 3)
        
        print(f"  User has 3 pins on leaderboard as expected")
        print("  ✓ Pin count properly increments")


class TestUserPinsEndpoint(unittest.TestCase):
    """Test suite for /api/users/{userID}/pins endpoint"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_user = create_test_user()
        cls.user_id = cls.test_user["user"]["userID"]
        
        # Create some pins
        for i in range(2):
            create_pin_for_user(cls.test_user["token"], lat_offset=i*0.001)
        
        print(f"\n{'='*60}")
        print("Testing User Pins Endpoint")
        print(f"{'='*60}\n")

    def test_01_get_user_pins(self):
        """Test getting pins for a specific user"""
        print("\n[TEST] Getting pins for user...")
        
        response = requests.get(
            f"{BASE_URL}/api/users/{self.user_id}/pins",
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)
        
        # All pins should belong to this user
        for pin in data:
            self.assertEqual(pin["userID"], self.user_id)
        
        print(f"  Found {len(data)} pins for user {self.user_id}")
        print("  ✓ User pins retrieved successfully")

    def test_02_nonexistent_user(self):
        """Test getting pins for nonexistent user"""
        print("\n[TEST] Getting pins for nonexistent user...")
        
        response = requests.get(
            f"{BASE_URL}/api/users/999999/pins",
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 404)
        
        print("  ✓ Nonexistent user properly returns 404")


class TestLeaderboardCaseSensitivity(unittest.TestCase):
    """Test suite for type parameter case sensitivity"""

    def test_01_type_case_insensitive(self):
        """Test that type parameter is case-insensitive"""
        print("\n[TEST] Testing type parameter case sensitivity...")
        
        # Test "WEEKLY"
        response1 = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "WEEKLY"},
            timeout=REQUEST_TIMEOUT
        )
        
        # Test "Weekly"
        response2 = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "Weekly"},
            timeout=REQUEST_TIMEOUT
        )
        
        # Test "ALL-TIME"
        response3 = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "ALL-TIME"},
            timeout=REQUEST_TIMEOUT
        )
        
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)
        
        print("  WEEKLY: OK, Weekly: OK, ALL-TIME: OK")
        print("  ✓ Type parameter is case-insensitive")


def run_tests():
    """Run all test suites"""
    # Check if backend is running
    try:
        response = requests.get(
            f"{BASE_URL}{LEADERBOARD_ENDPOINT}",
            params={"type": "weekly"},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        print("\n" + "="*60)
        print("✗ ERROR: Backend is not running!")
        print("="*60)
        print("\nPlease start the backend first:")
        print("  cd backend")
        print("  mvn spring-boot:run")
        print("="*60 + "\n")
        return
    
    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestLeaderboardBasic))
    suite.addTests(loader.loadTestsFromTestCase(TestLeaderboardPagination))
    suite.addTests(loader.loadTestsFromTestCase(TestLeaderboardSorting))
    suite.addTests(loader.loadTestsFromTestCase(TestLeaderboardWithNewUser))
    suite.addTests(loader.loadTestsFromTestCase(TestUserPinsEndpoint))
    suite.addTests(loader.loadTestsFromTestCase(TestLeaderboardCaseSensitivity))
    
    # Run with verbosity
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
    print("="*60 + "\n")


if __name__ == "__main__":
    run_tests()

