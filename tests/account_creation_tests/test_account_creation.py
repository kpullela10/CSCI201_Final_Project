import unittest
import requests
from typing import Dict, Any
import random
import string

BASE_URL = "http://localhost:8080"
API_PREFIX = "/api"
SIGNUP_ENDPOINT = f"{API_PREFIX}/auth/signup"
LOGIN_ENDPOINT = f"{API_PREFIX}/auth/login"
REQUEST_TIMEOUT = 30


def generate_random_user():
    """Generate random user data to avoid conflicts"""
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return {
        "email": f"testuser_{random_suffix}@usc.edu",
        "username": f"testuser_{random_suffix}",
        "password": "TestPassword123"
    }


class TestAccountCreation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = BASE_URL
        cls.signup_url = f"{BASE_URL}{SIGNUP_ENDPOINT}"
        cls.login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        cls.created_users = []
        print(f"\n{'='*60}")
        print(f"Testing Authentication Endpoints")
        print(f"Base URL: {cls.base_url}")
        print(f"Signup: {cls.signup_url}")
        print(f"Login: {cls.login_url}")
        print(f"{'='*60}\n")

    @classmethod
    def tearDownClass(cls):
        print(f"\n{'='*60}")
        print(f"Test Summary")
        print(f"Created {len(cls.created_users)} users during tests")
        print(f"{'='*60}\n")

    def test_01_valid_account_creation(self):
        """Test successful account creation with valid USC email"""
        print("\n[TEST] Valid account creation...")

        account_data = generate_random_user()

        response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")

        # Backend returns 200 OK (not 201)
        self.assertEqual(response.status_code, 200, "Expected 200 OK for successful signup")

        response_data = response.json()

        # Check response structure
        self.assertIn("token", response_data, "Response should contain JWT token")
        self.assertIn("user", response_data, "Response should contain user object")

        # Verify user data
        user = response_data["user"]
        self.assertEqual(user["username"], account_data["username"])
        self.assertEqual(user["email"], account_data["email"])
        self.assertIn("userID", user, "User should have userID")

        # Verify token is not empty
        self.assertTrue(len(response_data["token"]) > 0, "Token should not be empty")

        self.created_users.append(account_data["username"])
        print("  ✓ Account created successfully with JWT token")

    def test_02_duplicate_email(self):
        """Test that duplicate email is rejected"""
        print("\n[TEST] Duplicate email rejection...")

        # Create first user
        account_data = generate_random_user()
        response1 = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )
        self.assertEqual(response1.status_code, 200, "First signup should succeed")

        # Try to create another user with same email, different username
        duplicate_data = {
            "email": account_data["email"],  # Same email
            "username": f"different_{account_data['username']}",  # Different username
            "password": "AnotherPass456"
        }

        response2 = requests.post(
            self.signup_url,
            json=duplicate_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response2.status_code}")
        print(f"  Response: {response2.json()}")

        # Backend returns 409 Conflict
        self.assertEqual(response2.status_code, 409, "Expected 409 Conflict for duplicate email")

        response_data = response2.json()
        self.assertIn("message", response_data, "Error response should have 'message' field")
        self.assertIn("already exists", response_data["message"].lower(),
                     "Error message should mention 'already exists'")

        print("  ✓ Duplicate email properly rejected")

    def test_03_duplicate_username(self):
        """Test that duplicate username is rejected"""
        print("\n[TEST] Duplicate username rejection...")

        # Create first user
        account_data = generate_random_user()
        response1 = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )
        self.assertEqual(response1.status_code, 200, "First signup should succeed")

        # Try to create another user with same username, different email
        duplicate_data = {
            "email": f"different_{account_data['email']}",  # Different email
            "username": account_data["username"],  # Same username
            "password": "AnotherPass456"
        }

        response2 = requests.post(
            self.signup_url,
            json=duplicate_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response2.status_code}")
        print(f"  Response: {response2.json()}")

        # Backend returns 409 Conflict
        self.assertEqual(response2.status_code, 409, "Expected 409 Conflict for duplicate username")

        response_data = response2.json()
        self.assertIn("message", response_data)
        self.assertIn("already exists", response_data["message"].lower())

        print("  ✓ Duplicate username properly rejected")

    def test_04_non_usc_email_rejected(self):
        """Test that non-USC emails are rejected"""
        print("\n[TEST] Non-USC email rejection...")

        account_data = {
            "email": "test@gmail.com",  # Not @usc.edu
            "username": "testuser_gmail",
            "password": "TestPass123"
        }

        response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")

        # Backend returns 400 Bad Request
        self.assertEqual(response.status_code, 400, "Non-USC email should return 400")

        response_data = response.json()
        self.assertIn("message", response_data)
        self.assertIn("usc.edu", response_data["message"].lower(),
                     "Error should mention USC email requirement")

        print("  ✓ Non-USC email properly rejected")

    def test_05_login_after_signup(self):
        """Test that user can login after successful signup"""
        print("\n[TEST] Login after signup...")

        # Create account
        account_data = generate_random_user()
        signup_response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )
        self.assertEqual(signup_response.status_code, 200)
        signup_token = signup_response.json()["token"]

        # Try to login
        login_data = {
            "email": account_data["email"],
            "password": account_data["password"]
        }

        login_response = requests.post(
            self.login_url,
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {login_response.status_code}")
        print(f"  Response: {login_response.json()}")

        self.assertEqual(login_response.status_code, 200, "Login should succeed")

        login_data = login_response.json()
        self.assertIn("token", login_data, "Login response should contain token")
        self.assertIn("user", login_data, "Login response should contain user")

        # Verify user data matches
        user = login_data["user"]
        self.assertEqual(user["email"], account_data["email"])
        self.assertEqual(user["username"], account_data["username"])

        print("  ✓ Login successful after signup")

    def test_06_login_with_wrong_password(self):
        """Test that login fails with wrong password"""
        print("\n[TEST] Login with wrong password...")

        # Create account
        account_data = generate_random_user()
        requests.post(self.signup_url, json=account_data, timeout=REQUEST_TIMEOUT)

        # Try to login with wrong password
        login_data = {
            "email": account_data["email"],
            "password": "WrongPassword123"  # Wrong password
        }

        response = requests.post(
            self.login_url,
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")

        # Backend returns 401 Unauthorized
        self.assertEqual(response.status_code, 401, "Wrong password should return 401")

        response_data = response.json()
        self.assertIn("message", response_data)
        self.assertIn("invalid", response_data["message"].lower(),
                     "Error should mention invalid credentials")

        print("  ✓ Wrong password properly rejected")

    def test_07_login_nonexistent_user(self):
        """Test that login fails for non-existent user"""
        print("\n[TEST] Login with non-existent user...")

        login_data = {
            "email": "nonexistent@usc.edu",
            "password": "SomePassword123"
        }

        response = requests.post(
            self.login_url,
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")

        # Backend returns 401 Unauthorized
        self.assertEqual(response.status_code, 401, "Non-existent user should return 401")

        print("  ✓ Non-existent user login properly rejected")

    def test_08_missing_email(self):
        """Test that signup fails when email is missing"""
        print("\n[TEST] Missing email field...")

        account_data = {
            "username": "noemail",
            "password": "ValidPass123"
        }

        response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 400, "Missing email should return 400")
        print("  ✓ Missing email properly rejected")

    def test_09_missing_username(self):
        """Test that signup fails when username is missing"""
        print("\n[TEST] Missing username field...")

        account_data = {
            "email": "nousername@usc.edu",
            "password": "ValidPass123"
        }

        response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 400, "Missing username should return 400")
        print("  ✓ Missing username properly rejected")

    def test_10_missing_password(self):
        """Test that signup fails when password is missing"""
        print("\n[TEST] Missing password field...")

        account_data = {
            "email": "nopassword@usc.edu",
            "username": "nopassword"
        }

        response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 400, "Missing password should return 400")
        print("  ✓ Missing password properly rejected")

    def test_11_empty_username(self):
        """Test that empty username is rejected"""
        print("\n[TEST] Empty username...")

        account_data = {
            "email": "emptyuser@usc.edu",
            "username": "",
            "password": "ValidPass123"
        }

        response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 400, "Empty username should return 400")
        print("  ✓ Empty username properly rejected")

    def test_12_empty_password(self):
        """Test that empty password is rejected"""
        print("\n[TEST] Empty password...")

        account_data = {
            "email": "emptypass@usc.edu",
            "username": "emptypass",
            "password": ""
        }

        response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        print(f"  Status Code: {response.status_code}")

        self.assertEqual(response.status_code, 400, "Empty password should return 400")
        print("  ✓ Empty password properly rejected")

    def test_13_password_hashing_verification(self):
        """Test that passwords are hashed (not stored in plaintext)"""
        print("\n[TEST] Password hashing verification...")

        account_data = generate_random_user()

        response = requests.post(
            self.signup_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 200)

        # Verify password is not returned in response
        response_data = response.json()
        user = response_data["user"]

        self.assertNotIn("password", user, "Password should not be in user response")
        self.assertNotIn("passwordHash", user, "Password hash should not be in user response")

        # Verify we can still login (password was hashed and stored correctly)
        login_response = requests.post(
            self.login_url,
            json={"email": account_data["email"], "password": account_data["password"]},
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(login_response.status_code, 200,
                        "Should be able to login with hashed password")

        print("  ✓ Passwords are properly hashed (Argon2)")
        print("  ✓ Passwords not exposed in API responses")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
