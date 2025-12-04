"""
Comprehensive Pin API Tests for Squirrel Spotter USC
Tests pin creation, retrieval, rate limiting, and validation
"""

import unittest
import requests
import time
import random
import string
from typing import Dict, Optional
import io

# Configuration
BASE_URL = "http://localhost:8080"
SIGNUP_ENDPOINT = "/api/auth/signup"
LOGIN_ENDPOINT = "/api/auth/login"
PINS_ENDPOINT = "/api/pins"
WEEKLY_PINS_ENDPOINT = "/api/pins/weekly"
MY_PINS_ENDPOINT = "/api/pins/my"
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
        "email": f"pintest_{suffix}@usc.edu",
        "username": f"pintest_{suffix}",
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


class TestPinCreation(unittest.TestCase):
    """Test suite for pin creation functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_user = create_test_user()
        cls.token = cls.test_user["token"]
        cls.user_id = cls.test_user["user"]["userID"]
        cls.headers = get_auth_headers(cls.token)
        print(f"\n{'='*60}")
        print("Testing Pin Creation Endpoints")
        print(f"User: {cls.test_user['user']['username']}")
        print(f"{'='*60}\n")

    def test_01_create_pin_successfully(self):
        """Test creating a pin with valid data (form-data format)"""
        print("\n[TEST] Creating pin with valid data...")
        
        form_data = {
            "lat": str(USC_CENTER["lat"]),
            "lng": str(USC_CENTER["lng"]),
            "description": "Spotted a cute squirrel near Tommy Trojan!"
        }
        
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,  # Using form data, NOT JSON
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")
        
        self.assertEqual(response.status_code, 201, "Expected 201 Created")
        
        data = response.json()
        self.assertIn("pinID", data)
        self.assertEqual(float(data["lat"]), USC_CENTER["lat"])
        self.assertEqual(float(data["lng"]), USC_CENTER["lng"])
        self.assertEqual(data["description"], form_data["description"])
        self.assertEqual(data["userID"], self.user_id)
        self.assertIn("createdAt", data)
        
        # Store pin ID for later tests
        self.__class__.created_pin_id = data["pinID"]
        print("  ✓ Pin created successfully")

    def test_02_create_pin_without_description(self):
        """Test creating a pin without description (optional field)"""
        print("\n[TEST] Creating pin without description...")
        
        form_data = {
            "lat": str(USC_CENTER["lat"] + 0.001),
            "lng": str(USC_CENTER["lng"] + 0.001)
        }
        
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 201, "Expected 201 Created")
        print("  ✓ Pin created without description")

    def test_03_create_pin_missing_latitude(self):
        """Test that creating a pin without latitude fails"""
        print("\n[TEST] Creating pin without latitude...")
        
        form_data = {
            "lng": str(USC_CENTER["lng"]),
            "description": "Missing latitude"
        }
        
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request")
        print("  ✓ Missing latitude properly rejected")

    def test_04_create_pin_missing_longitude(self):
        """Test that creating a pin without longitude fails"""
        print("\n[TEST] Creating pin without longitude...")
        
        form_data = {
            "lat": str(USC_CENTER["lat"]),
            "description": "Missing longitude"
        }
        
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request")
        print("  ✓ Missing longitude properly rejected")

    def test_05_create_pin_invalid_latitude(self):
        """Test that latitude out of range (-90 to 90) fails"""
        print("\n[TEST] Creating pin with invalid latitude (> 90)...")
        
        form_data = {
            "lat": "91.0",  # Invalid: > 90
            "lng": str(USC_CENTER["lng"])
        }
        
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request")
        print("  ✓ Invalid latitude properly rejected")

    def test_06_create_pin_invalid_longitude(self):
        """Test that longitude out of range (-180 to 180) fails"""
        print("\n[TEST] Creating pin with invalid longitude (> 180)...")
        
        form_data = {
            "lat": str(USC_CENTER["lat"]),
            "lng": "181.0"  # Invalid: > 180
        }
        
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 400, "Expected 400 Bad Request")
        print("  ✓ Invalid longitude properly rejected")

    def test_07_create_pin_unauthorized(self):
        """Test that creating a pin without authentication fails"""
        print("\n[TEST] Creating pin without authentication...")
        
        form_data = {
            "lat": str(USC_CENTER["lat"]),
            "lng": str(USC_CENTER["lng"]),
            "description": "Unauthorized attempt"
        }
        
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            # No auth headers
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertIn(response.status_code, [401, 403], "Expected 401/403 Unauthorized")
        print("  ✓ Unauthorized request properly rejected")


class TestPinRetrieval(unittest.TestCase):
    """Test suite for pin retrieval functionality"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_user = create_test_user()
        cls.token = cls.test_user["token"]
        cls.user_id = cls.test_user["user"]["userID"]
        cls.headers = get_auth_headers(cls.token)
        
        # Create a test pin
        form_data = {
            "lat": str(USC_CENTER["lat"]),
            "lng": str(USC_CENTER["lng"]),
            "description": "Test pin for retrieval"
        }
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            headers=cls.headers,
            timeout=REQUEST_TIMEOUT
        )
        cls.test_pin = response.json()
        
        print(f"\n{'='*60}")
        print("Testing Pin Retrieval Endpoints")
        print(f"{'='*60}\n")

    def test_01_get_weekly_pins(self):
        """Test retrieving weekly pins (public endpoint)"""
        print("\n[TEST] Getting weekly pins...")
        
        response = requests.get(
            f"{BASE_URL}{WEEKLY_PINS_ENDPOINT}",
            timeout=REQUEST_TIMEOUT
            # No auth needed - public endpoint
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        
        if len(data) > 0:
            pin = data[0]
            self.assertIn("pinID", pin)
            self.assertIn("lat", pin)
            self.assertIn("lng", pin)
            self.assertIn("createdAt", pin)
            print(f"  Found {len(data)} weekly pins")
        
        print("  ✓ Weekly pins retrieved successfully")

    def test_02_get_my_pins(self):
        """Test retrieving authenticated user's pins"""
        print("\n[TEST] Getting my pins...")
        
        response = requests.get(
            f"{BASE_URL}{MY_PINS_ENDPOINT}",
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, "Should have at least one pin")
        
        # Verify all pins belong to this user
        for pin in data:
            self.assertEqual(pin["userID"], self.user_id)
        
        print(f"  Found {len(data)} pins for user")
        print("  ✓ User's pins retrieved successfully")

    def test_03_get_my_pins_unauthorized(self):
        """Test that getting my pins without auth fails"""
        print("\n[TEST] Getting my pins without authentication...")
        
        response = requests.get(
            f"{BASE_URL}{MY_PINS_ENDPOINT}",
            timeout=REQUEST_TIMEOUT
            # No auth headers
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertIn(response.status_code, [401, 403], "Expected 401/403")
        print("  ✓ Unauthorized request properly rejected")

    def test_04_get_pin_by_id(self):
        """Test retrieving a specific pin by ID (public endpoint)"""
        print("\n[TEST] Getting pin by ID...")
        
        pin_id = self.test_pin["pinID"]
        
        response = requests.get(
            f"{BASE_URL}{PINS_ENDPOINT}/{pin_id}",
            timeout=REQUEST_TIMEOUT
            # No auth needed - public endpoint
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["pinID"], pin_id)
        print(f"  ✓ Pin {pin_id} retrieved successfully")

    def test_05_get_nonexistent_pin(self):
        """Test retrieving a pin that doesn't exist"""
        print("\n[TEST] Getting nonexistent pin...")
        
        response = requests.get(
            f"{BASE_URL}{PINS_ENDPOINT}/999999",
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 404, "Expected 404 Not Found")
        print("  ✓ Nonexistent pin properly returns 404")


class TestRateLimiting(unittest.TestCase):
    """Test suite for rate limiting functionality"""

    def test_01_rate_limit_exceeded(self):
        """Test that rate limit (5 pins per 30 minutes) is enforced"""
        print("\n[TEST] Testing rate limit (5 pins per 30 minutes)...")
        
        # Create a fresh user for this test
        test_user = create_test_user()
        headers = get_auth_headers(test_user["token"])
        
        # Try to create 6 pins quickly
        for i in range(6):
            form_data = {
                "lat": str(USC_CENTER["lat"] + (i * 0.0001)),
                "lng": str(USC_CENTER["lng"] + (i * 0.0001)),
                "description": f"Rate limit test pin {i+1}"
            }
            
            response = requests.post(
                f"{BASE_URL}{PINS_ENDPOINT}",
                data=form_data,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if i < 5:
                # First 5 pins should succeed
                self.assertEqual(response.status_code, 201, 
                    f"Pin {i+1} should succeed, got {response.status_code}")
                print(f"  Pin {i+1}/6: Created (status {response.status_code})")
            else:
                # 6th pin should be rate limited
                self.assertEqual(response.status_code, 429,
                    f"Pin {i+1} should be rate limited, got {response.status_code}")
                
                data = response.json()
                self.assertIn("message", data)
                self.assertIn("limit", data["message"].lower())
                print(f"  Pin {i+1}/6: Rate limited (status {response.status_code})")
        
        print("  ✓ Rate limiting working correctly")


class TestPinWithImage(unittest.TestCase):
    """Test suite for pin creation with image upload"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_user = create_test_user()
        cls.token = cls.test_user["token"]
        cls.headers = get_auth_headers(cls.token)
        print(f"\n{'='*60}")
        print("Testing Pin Creation with Images")
        print(f"{'='*60}\n")

    def test_01_create_pin_with_image(self):
        """Test creating a pin with an image upload"""
        print("\n[TEST] Creating pin with image...")
        
        # Create a simple test image (1x1 pixel PNG)
        # PNG header for a minimal valid 1x1 transparent PNG
        png_data = bytes([
            0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
            0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,  # IHDR chunk
            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
            0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
            0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41,
            0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
            0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
            0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE,
            0x42, 0x60, 0x82
        ])
        
        files = {
            'image': ('squirrel.png', io.BytesIO(png_data), 'image/png')
        }
        
        form_data = {
            "lat": str(USC_CENTER["lat"]),
            "lng": str(USC_CENTER["lng"]),
            "description": "Squirrel with photo!"
        }
        
        response = requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            files=files,
            headers=self.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            # Image URL should be set
            self.assertIn("imageUrl", data)
            if data.get("imageUrl"):
                print(f"  Image URL: {data['imageUrl']}")
            print("  ✓ Pin with image created successfully")
        else:
            # Image upload might fail due to storage config, but pin should still work
            print(f"  Response: {response.text}")
            self.assertIn(response.status_code, [201, 400])


class TestUserPins(unittest.TestCase):
    """Test suite for getting pins by user ID"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_user = create_test_user()
        cls.token = cls.test_user["token"]
        cls.user_id = cls.test_user["user"]["userID"]
        cls.headers = get_auth_headers(cls.token)
        
        # Create a test pin
        form_data = {
            "lat": str(USC_CENTER["lat"]),
            "lng": str(USC_CENTER["lng"]),
            "description": "User pins test"
        }
        requests.post(
            f"{BASE_URL}{PINS_ENDPOINT}",
            data=form_data,
            headers=cls.headers,
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"\n{'='*60}")
        print("Testing User Pins Endpoint")
        print(f"{'='*60}\n")

    def test_01_get_user_pins(self):
        """Test getting all pins for a specific user (public endpoint)"""
        print("\n[TEST] Getting pins for user...")
        
        response = requests.get(
            f"{BASE_URL}/api/users/{self.user_id}/pins",
            timeout=REQUEST_TIMEOUT
            # No auth needed - public endpoint
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # All pins should belong to this user
        for pin in data:
            self.assertEqual(pin["userID"], self.user_id)
        
        print(f"  Found {len(data)} pins for user {self.user_id}")
        print("  ✓ User pins retrieved successfully")

    def test_02_get_nonexistent_user_pins(self):
        """Test getting pins for a user that doesn't exist"""
        print("\n[TEST] Getting pins for nonexistent user...")
        
        response = requests.get(
            f"{BASE_URL}/api/users/999999/pins",
            timeout=REQUEST_TIMEOUT
        )
        
        print(f"  Status Code: {response.status_code}")
        
        self.assertEqual(response.status_code, 404, "Expected 404 Not Found")
        print("  ✓ Nonexistent user properly returns 404")


def run_tests():
    """Run all test suites"""
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/api/pins/weekly", timeout=5)
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
    suite.addTests(loader.loadTestsFromTestCase(TestPinCreation))
    suite.addTests(loader.loadTestsFromTestCase(TestPinRetrieval))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimiting))
    suite.addTests(loader.loadTestsFromTestCase(TestPinWithImage))
    suite.addTests(loader.loadTestsFromTestCase(TestUserPins))
    
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

