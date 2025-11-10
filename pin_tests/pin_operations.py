import pytest
import requests
import time
from typing import Dict, Any
from test_config import (
    BASE_URL, API_PREFIX, TEST_USER_EMAIL, TEST_USER_PASSWORD,
    DAILY_PIN_LIMIT, MAX_DESCRIPTION_LENGTH, ENDPOINTS,
    USC_CAMPUS_CENTER, REQUEST_TIMEOUT, AUTH_HEADER_PREFIX,
    TOKEN_RESPONSE_KEY, HTTP_STATUS
)

class TestPinCreationRetrieval:
    """Test suite for Pin Creation and Retrieval operations"""
    
    @pytest.fixture
    def auth_headers(self) -> Dict[str, str]:
        """
        Fixture to provide authentication headers.
        Adjust based on your authentication mechanism (JWT, session, etc.)
        """
        # Login and get auth token
        login_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        response = requests.post(
            f"{BASE_URL}{ENDPOINTS['login']}", 
            json=login_data,
            timeout=REQUEST_TIMEOUT
        )
        assert response.status_code == HTTP_STATUS["success"]
        
        token = response.json().get(TOKEN_RESPONSE_KEY)
        return {"Authorization": f"{AUTH_HEADER_PREFIX} {token}"}
    
    @pytest.fixture
    def test_user_id(self, auth_headers) -> int:
        """Fixture to get the current user's ID"""
        response = requests.get(
            f"{BASE_URL}{ENDPOINTS['current_user']}", 
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        assert response.status_code == HTTP_STATUS["success"]
        return response.json().get("userId")
    
    @pytest.fixture
    def valid_pin_data(self, test_user_id) -> Dict[str, Any]:
        """Fixture providing valid pin data"""
        return {
            "userId": test_user_id,
            "lat": USC_CAMPUS_CENTER["lat"],
            "lng": USC_CAMPUS_CENTER["lng"],
            "description": "Fluffy gray squirrel near Doheny Library",
            "image_url": "https://example.com/squirrel.jpg"
        }
    
    # Test: Successful Pin Creation
    def test_create_pin_successfully(self, auth_headers, valid_pin_data):
        """
        Test that a pin can be created successfully with valid data.
        Input: Required pin details (userId, lat, lng, description)
        Expected: Pin created and stored in database with 201 status
        """
        response = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=valid_pin_data,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        
        assert response.status_code == HTTP_STATUS["created"], \
            f"Expected {HTTP_STATUS['created']}, got {response.status_code}"
        response_data = response.json()
        
        # Verify response contains pin details
        assert "pinId" in response_data
        assert response_data["lat"] == valid_pin_data["lat"]
        assert response_data["lng"] == valid_pin_data["lng"]
        assert response_data["description"] == valid_pin_data["description"]
        
        # Verify pin exists in database by fetching it
        pin_id = response_data["pinId"]
        pin_detail_url = ENDPOINTS["pin_detail"].format(pinId=pin_id)
        get_response = requests.get(
            f"{BASE_URL}{pin_detail_url}",
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        assert get_response.status_code == HTTP_STATUS["success"]
    
    # Test: Get All Pins for a Specific User
    def test_get_all_pins_for_user(self, auth_headers, test_user_id, valid_pin_data):
        """
        Test retrieving all pins for a specific user.
        Input: userId
        Expected: Returns every pin from the userId successfully
        """
        # Create a pin first
        create_response = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=valid_pin_data,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        assert create_response.status_code == HTTP_STATUS["created"]
        created_pin_id = create_response.json()["pinId"]
        
        # Get all pins for the user
        user_pins_url = ENDPOINTS["user_pins"].format(userId=test_user_id)
        response = requests.get(
            f"{BASE_URL}{user_pins_url}",
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        
        assert response.status_code == HTTP_STATUS["success"]
        pins = response.json()
        assert isinstance(pins, list)
        
        # Verify the created pin is in the list
        pin_ids = [pin["pinId"] for pin in pins]
        assert created_pin_id in pin_ids
    
    # Test: Get Pin Details
    def test_get_pin_details(self, auth_headers, valid_pin_data):
        """
        Test retrieving details of a specific pin.
        Input: pinId
        Expected: Successfully returns the pin details
        """
        # Create a pin first
        create_response = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=valid_pin_data,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        assert create_response.status_code == HTTP_STATUS["created"]
        pin_id = create_response.json()["pinId"]
        
        # Get pin details
        pin_detail_url = ENDPOINTS["pin_detail"].format(pinId=pin_id)
        response = requests.get(
            f"{BASE_URL}{pin_detail_url}",
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        
        assert response.status_code == HTTP_STATUS["success"]
        pin_details = response.json()
        
        # Verify all expected fields are present
        assert pin_details["pinId"] == pin_id
        assert pin_details["lat"] == valid_pin_data["lat"]
        assert pin_details["lng"] == valid_pin_data["lng"]
        assert pin_details["description"] == valid_pin_data["description"]
        assert "created_at" in pin_details
    
    # Test: Duplicate Pins (if applicable)
    def test_duplicate_pins(self, auth_headers, valid_pin_data):
        """
        Test handling of duplicate pins.
        This test depends on your business logic for handling duplicates.
        """
        # Create first pin
        response1 = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=valid_pin_data,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        assert response1.status_code == HTTP_STATUS["created"]
        
        # Try to create duplicate pin (same location and user)
        response2 = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=valid_pin_data,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        
        # Adjust assertion based on your business logic:
        # Option 1: Duplicates are allowed
        # assert response2.status_code == HTTP_STATUS["created"]
        
        # Option 2: Duplicates are rejected
        # assert response2.status_code in [HTTP_STATUS["bad_request"], HTTP_STATUS["conflict"]]
        # assert "duplicate" in response2.json().get("message", "").lower()
        
        # For now, we'll just verify both create attempts complete
        assert response2.status_code in [
            HTTP_STATUS["created"], 
            HTTP_STATUS["bad_request"], 
            HTTP_STATUS["conflict"]
        ]
    
    # Test: Unauthorized Pin Creation
    def test_unauthorized_pin_creation(self, valid_pin_data):
        """
        Test that pin creation without authentication fails.
        Input: POST /api/pins without auth
        Expected Output: 401 Unauthorized
        """
        response = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=valid_pin_data,
            timeout=REQUEST_TIMEOUT
            # No auth headers provided
        )
        
        assert response.status_code == HTTP_STATUS["unauthorized"], \
            f"Expected {HTTP_STATUS['unauthorized']} Unauthorized, got {response.status_code}"
    
    # Test: Pin Creation Beyond Daily Limits
    def test_pin_creation_beyond_daily_limit(self, auth_headers, test_user_id):
        """
        Test that creating pins beyond daily limit is rejected.
        Input: Create pins from the same userId beyond limit
        Expected Output: Error message indicating limit exceeded
        """
        created_pins = []
        for i in range(DAILY_PIN_LIMIT + 1):
            pin_data = {
                "userId": test_user_id,
                "lat": USC_CAMPUS_CENTER["lat"] + (i * 0.0001),  # Slight variation
                "lng": USC_CAMPUS_CENTER["lng"] + (i * 0.0001),
                "description": f"Test pin {i}"
            }
            
            response = requests.post(
                f"{BASE_URL}{ENDPOINTS['pins']}",
                json=pin_data,
                headers=auth_headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if i < DAILY_PIN_LIMIT:
                # Should succeed for pins within limit
                assert response.status_code == HTTP_STATUS["created"]
                created_pins.append(response.json()["pinId"])
            else:
                # Should fail for pin exceeding limit
                assert response.status_code in [
                    HTTP_STATUS["bad_request"], 
                    HTTP_STATUS["too_many_requests"]
                ], f"Expected {HTTP_STATUS['bad_request']}/{HTTP_STATUS['too_many_requests']} for pin beyond limit, got {response.status_code}"
                
                error_message = response.json().get("message", "").lower()
                assert "limit" in error_message or "exceeded" in error_message, \
                    f"Expected error about limit, got: {response.json()}"
    
    # Test: Pin Creation with Missing Coordinates
    def test_pin_creation_missing_coordinates(self, auth_headers, test_user_id):
        """
        Test that pin creation fails when coordinates are missing.
        Input: POST with description but no lat/lng
        Expected Output: 400 Bad Request
        """
        # Missing latitude
        pin_data_no_lat = {
            "userId": test_user_id,
            "lng": USC_CAMPUS_CENTER["lng"],
            "description": "Pin without latitude"
        }
        
        response1 = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=pin_data_no_lat,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        assert response1.status_code == HTTP_STATUS["bad_request"], \
            f"Expected {HTTP_STATUS['bad_request']} for missing latitude, got {response1.status_code}"
        
        # Missing longitude
        pin_data_no_lng = {
            "userId": test_user_id,
            "lat": USC_CAMPUS_CENTER["lat"],
            "description": "Pin without longitude"
        }
        
        response2 = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=pin_data_no_lng,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        assert response2.status_code == HTTP_STATUS["bad_request"], \
            f"Expected {HTTP_STATUS['bad_request']} for missing longitude, got {response2.status_code}"
        
        # Missing both coordinates
        pin_data_no_coords = {
            "userId": test_user_id,
            "description": "Pin without coordinates"
        }
        
        response3 = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=pin_data_no_coords,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        assert response3.status_code == HTTP_STATUS["bad_request"], \
            f"Expected {HTTP_STATUS['bad_request']} for missing coordinates, got {response3.status_code}"
    
    # Test: Pin Creation with Long Description
    def test_pin_creation_long_description(self, auth_headers, test_user_id):
        """
        Test handling of pin creation with description exceeding character limit.
        Input: Description length > allowed (500+ characters)
        Expected Output: 400 Bad Request OR truncated (depending on design)
        """
        # Generate a description longer than allowed limit
        long_description = "A" * (MAX_DESCRIPTION_LENGTH + 1)
        
        pin_data = {
            "userId": test_user_id,
            "lat": USC_CAMPUS_CENTER["lat"],
            "lng": USC_CAMPUS_CENTER["lng"],
            "description": long_description
        }
        
        response = requests.post(
            f"{BASE_URL}{ENDPOINTS['pins']}",
            json=pin_data,
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        
        # Option 1: System rejects long descriptions
        if response.status_code == HTTP_STATUS["bad_request"]:
            error_message = response.json().get("message", "").lower()
            assert "description" in error_message or "length" in error_message or "long" in error_message
        
        # Option 2: System truncates descriptions
        elif response.status_code == HTTP_STATUS["created"]:
            pin_id = response.json()["pinId"]
            pin_detail_url = ENDPOINTS["pin_detail"].format(pinId=pin_id)
            get_response = requests.get(
                f"{BASE_URL}{pin_detail_url}",
                headers=auth_headers,
                timeout=REQUEST_TIMEOUT
            )
            saved_description = get_response.json()["description"]
            assert len(saved_description) <= MAX_DESCRIPTION_LENGTH, \
                f"Description should be truncated to {MAX_DESCRIPTION_LENGTH} characters"
        
        else:
            pytest.fail(f"Unexpected status code: {response.status_code}")
    
    # Test: Get Nonexistent Pin
    def test_get_nonexistent_pin(self, auth_headers):
        """
        Test that requesting a nonexistent pin returns appropriate error.
        """
        nonexistent_pin_id = 999999
        pin_detail_url = ENDPOINTS["pin_detail"].format(pinId=nonexistent_pin_id)
        response = requests.get(
            f"{BASE_URL}{pin_detail_url}",
            headers=auth_headers,
            timeout=REQUEST_TIMEOUT
        )
        
        assert response.status_code == HTTP_STATUS["not_found"], \
            f"Expected {HTTP_STATUS['not_found']} for nonexistent pin, got {response.status_code}"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])