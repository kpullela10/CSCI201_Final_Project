import unittest
import requests
from typing import Dict, Any

BASE_URL = "http://localhost:8080"
API_PREFIX = "/api"
REGISTER_ENDPOINT = f"{API_PREFIX}/auth/register"
LOGIN_ENDPOINT = f"{API_PREFIX}/auth/login"
USER_ENDPOINT = f"{API_PREFIX}/users"
REQUEST_TIMEOUT = 30


class TestAccountCreation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.base_url = BASE_URL
        cls.register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"
        cls.login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        cls.user_url = f"{BASE_URL}{USER_ENDPOINT}"
        cls.created_users = []

    @classmethod
    def tearDownClass(cls):
        pass

    def test_valid_account_creation(self):
        account_data = {
            "email": "validuser@usc.edu",
            "username": "validuser123",
            "password": "ValidPass123"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertIn("message", response_data)
        self.assertEqual(response_data["message"], "Account Successfully Created")

        self.created_users.append(account_data["username"])

    def test_duplicate_username(self):
        account_data = {
            "email": "firstuser@usc.edu",
            "username": "duplicatetest",
            "password": "TestPass123"
        }

        response1 = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )
        self.assertEqual(response1.status_code, 201)

        duplicate_data = {
            "email": "seconduser@usc.edu",
            "username": "duplicatetest",
            "password": "AnotherPass456"
        }

        response2 = requests.post(
            self.register_url,
            json=duplicate_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertIn(response2.status_code, [400, 409])
        response_data = response2.json()
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Username already exists.")

    def test_password_missing_letter(self):
        account_data = {
            "email": "test1@usc.edu",
            "username": "testuser1",
            "password": "12345678"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("error", response_data)
        self.assertIn("letter", response_data["error"].lower())

    def test_password_missing_number(self):
        account_data = {
            "email": "test2@usc.edu",
            "username": "testuser2",
            "password": "abcdefgh"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("error", response_data)
        self.assertIn("number", response_data["error"].lower())

    def test_password_too_short(self):
        account_data = {
            "email": "test3@usc.edu",
            "username": "testuser3",
            "password": "Pass12"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("error", response_data)
        self.assertIn("8", response_data["error"])

    def test_password_all_requirements_failed(self):
        account_data = {
            "email": "test4@usc.edu",
            "username": "testuser4",
            "password": "short"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertIn("error", response_data)

    def test_user_added_to_database(self):
        account_data = {
            "email": "dbtest@usc.edu",
            "username": "dbtestuser",
            "password": "DbTest123"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "Account Successfully Created")

        login_data = {
            "email": account_data["email"],
            "password": account_data["password"]
        }

        login_response = requests.post(
            self.login_url,
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn("token", login_response.json())

        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        user_response = requests.get(
            f"{self.user_url}/me",
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(user_response.status_code, 200)
        user_data = user_response.json()
        self.assertEqual(user_data["username"], account_data["username"])
        self.assertEqual(user_data["email"], account_data["email"])

    def test_missing_email(self):
        account_data = {
            "username": "noemail",
            "password": "ValidPass123"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_username(self):
        account_data = {
            "email": "nousername@usc.edu",
            "password": "ValidPass123"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_password(self):
        account_data = {
            "email": "nopassword@usc.edu",
            "username": "nopassword"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)

    def test_invalid_email_format(self):
        account_data = {
            "email": "invalidemail",
            "username": "testuser5",
            "password": "ValidPass123"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)

    def test_empty_username(self):
        account_data = {
            "email": "emptyuser@usc.edu",
            "username": "",
            "password": "ValidPass123"
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)

    def test_empty_password(self):
        account_data = {
            "email": "emptypass@usc.edu",
            "username": "emptypass",
            "password": ""
        }

        response = requests.post(
            self.register_url,
            json=account_data,
            timeout=REQUEST_TIMEOUT
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
