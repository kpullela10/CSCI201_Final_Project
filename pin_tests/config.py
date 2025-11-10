# test_config.py
"""
Configuration file for USC Squirrel Tracker API tests.
Modify these settings to match your environment and requirements.
"""

# Server Configuration
BASE_URL = "http://localhost:8080"
API_PREFIX = "/api"

# Test User Credentials
TEST_USER_EMAIL = "testuser@usc.edu"
TEST_USER_PASSWORD = "TestPass123"

# Business Rules
DAILY_PIN_LIMIT = 10
MAX_DESCRIPTION_LENGTH = 500

# API Endpoints
ENDPOINTS = {
    "login": f"{API_PREFIX}/auth/login",
    "current_user": f"{API_PREFIX}/users/me",
    "pins": f"{API_PREFIX}/pins",
    "user_pins": f"{API_PREFIX}/users/{{userId}}/pins",
    "pin_detail": f"{API_PREFIX}/pins/{{pinId}}"
}

# Test Data
USC_CAMPUS_CENTER = {
    "lat": 34.0224,
    "lng": -118.2851
}

# Timeout Settings (in seconds)
REQUEST_TIMEOUT = 30

# Authentication
AUTH_HEADER_PREFIX = "Bearer"  # Change to "Token" or other if needed
TOKEN_RESPONSE_KEY = "token"  # Key in login response containing the token

# Expected HTTP Status Codes
HTTP_STATUS = {
    "success": 200,
    "created": 201,
    "bad_request": 400,
    "unauthorized": 401,
    "not_found": 404,
    "conflict": 409,
    "too_many_requests": 429
}