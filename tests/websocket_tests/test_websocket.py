"""
WebSocket Tests for Squirrel Spotter USC
Tests real-time pin broadcasting via WebSocket
"""

import unittest
import requests
import json
import time
import random
import string
import threading
from typing import Dict, List, Optional
import websocket  # pip install websocket-client

# Configuration
BASE_URL = "http://localhost:8080"
WS_URL = "ws://localhost:8080/ws/pins"
SIGNUP_ENDPOINT = "/api/auth/signup"
PINS_ENDPOINT = "/api/pins"
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
        "email": f"wstest_{suffix}@usc.edu",
        "username": f"wstest_{suffix}",
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


class WebSocketClient:
    """Simple WebSocket client for testing"""
    
    def __init__(self, url: str, token: Optional[str] = None):
        self.url = f"{url}?token={token}" if token else url
        self.ws = None
        self.messages: List[Dict] = []
        self.connected = False
        self.error = None
        self._lock = threading.Lock()
        
    def on_message(self, ws, message):
        """Called when a message is received"""
        with self._lock:
            try:
                data = json.loads(message)
                self.messages.append(data)
                print(f"  [WS] Received: {data.get('pinID', 'unknown')} - {data.get('description', '')[:30]}")
            except json.JSONDecodeError:
                self.messages.append({"raw": message})
    
    def on_error(self, ws, error):
        """Called when an error occurs"""
        self.error = str(error)
        print(f"  [WS] Error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Called when connection closes"""
        self.connected = False
        print(f"  [WS] Connection closed")
    
    def on_open(self, ws):
        """Called when connection opens"""
        self.connected = True
        print(f"  [WS] Connection established")
    
    def connect(self):
        """Connect to WebSocket server"""
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        # Run in separate thread
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()
        
        # Wait for connection
        for _ in range(50):  # Wait up to 5 seconds
            if self.connected:
                return True
            time.sleep(0.1)
        
        return False
    
    def disconnect(self):
        """Disconnect from WebSocket server"""
        if self.ws:
            self.ws.close()
            time.sleep(0.5)  # Give time for clean disconnect
    
    def get_messages(self) -> List[Dict]:
        """Get received messages (thread-safe)"""
        with self._lock:
            return list(self.messages)
    
    def clear_messages(self):
        """Clear received messages"""
        with self._lock:
            self.messages.clear()


class TestWebSocketConnection(unittest.TestCase):
    """Test suite for WebSocket connection"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_user = create_test_user()
        cls.token = cls.test_user["token"]
        print(f"\n{'='*60}")
        print("Testing WebSocket Connections")
        print(f"{'='*60}\n")

    def test_01_connect_without_token(self):
        """Test WebSocket connection without authentication token"""
        print("\n[TEST] Connecting without token...")
        
        client = WebSocketClient(WS_URL)
        
        try:
            connected = client.connect()
            self.assertTrue(connected, "Should be able to connect without token")
            print("  ✓ Connected successfully without token")
        finally:
            client.disconnect()

    def test_02_connect_with_token(self):
        """Test WebSocket connection with valid authentication token"""
        print("\n[TEST] Connecting with valid token...")
        
        client = WebSocketClient(WS_URL, self.token)
        
        try:
            connected = client.connect()
            self.assertTrue(connected, "Should be able to connect with valid token")
            print("  ✓ Connected successfully with token")
        finally:
            client.disconnect()

    def test_03_connect_with_invalid_token(self):
        """Test WebSocket connection with invalid token (should still connect for public viewing)"""
        print("\n[TEST] Connecting with invalid token...")
        
        client = WebSocketClient(WS_URL, "invalid_token_here")
        
        try:
            connected = client.connect()
            # Based on the implementation, connection should still work
            # The token is validated but invalid tokens are allowed for public viewing
            self.assertTrue(connected, "Should connect even with invalid token (public viewing)")
            print("  ✓ Connected (token invalid but connection allowed)")
        finally:
            client.disconnect()


class TestWebSocketBroadcast(unittest.TestCase):
    """Test suite for WebSocket pin broadcasting"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_user = create_test_user()
        cls.token = cls.test_user["token"]
        cls.user_id = cls.test_user["user"]["userID"]
        cls.headers = get_auth_headers(cls.token)
        print(f"\n{'='*60}")
        print("Testing WebSocket Broadcasting")
        print(f"{'='*60}\n")

    def test_01_receive_pin_broadcast(self):
        """Test that creating a pin broadcasts to connected WebSocket clients"""
        print("\n[TEST] Testing pin broadcast to WebSocket clients...")
        
        # Connect WebSocket client
        client = WebSocketClient(WS_URL, self.token)
        
        try:
            connected = client.connect()
            self.assertTrue(connected, "WebSocket should connect")
            
            # Wait a moment for stable connection
            time.sleep(0.5)
            
            # Clear any existing messages
            client.clear_messages()
            
            # Create a new pin
            unique_desc = f"WebSocket test pin {generate_random_suffix()}"
            form_data = {
                "lat": str(USC_CENTER["lat"]),
                "lng": str(USC_CENTER["lng"]),
                "description": unique_desc
            }
            
            response = requests.post(
                f"{BASE_URL}{PINS_ENDPOINT}",
                data=form_data,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            
            self.assertEqual(response.status_code, 201)
            created_pin = response.json()
            print(f"  Created pin: {created_pin['pinID']}")
            
            # Wait for broadcast
            time.sleep(1)
            
            # Check received messages
            messages = client.get_messages()
            print(f"  Received {len(messages)} message(s)")
            
            # Find our pin in the messages
            found = False
            for msg in messages:
                if msg.get("pinID") == created_pin["pinID"]:
                    found = True
                    self.assertEqual(msg["description"], unique_desc)
                    self.assertEqual(msg["userID"], self.user_id)
                    break
            
            self.assertTrue(found, f"Should receive broadcast for pin {created_pin['pinID']}")
            print("  ✓ Pin broadcast received successfully")
            
        finally:
            client.disconnect()

    def test_02_multiple_clients_receive_broadcast(self):
        """Test that multiple connected clients all receive pin broadcasts"""
        print("\n[TEST] Testing broadcast to multiple clients...")
        
        # Connect multiple clients
        clients = []
        for i in range(3):
            client = WebSocketClient(WS_URL)
            connected = client.connect()
            self.assertTrue(connected, f"Client {i+1} should connect")
            clients.append(client)
        
        print(f"  Connected {len(clients)} clients")
        
        try:
            time.sleep(0.5)
            
            # Clear all messages
            for client in clients:
                client.clear_messages()
            
            # Create a pin
            unique_desc = f"Multi-client test {generate_random_suffix()}"
            form_data = {
                "lat": str(USC_CENTER["lat"]),
                "lng": str(USC_CENTER["lng"]),
                "description": unique_desc
            }
            
            response = requests.post(
                f"{BASE_URL}{PINS_ENDPOINT}",
                data=form_data,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            
            self.assertEqual(response.status_code, 201)
            created_pin = response.json()
            
            # Wait for broadcasts
            time.sleep(1)
            
            # Check each client received the message
            for i, client in enumerate(clients):
                messages = client.get_messages()
                found = any(msg.get("pinID") == created_pin["pinID"] for msg in messages)
                self.assertTrue(found, f"Client {i+1} should receive broadcast")
                print(f"  Client {i+1}: Received broadcast ✓")
            
            print("  ✓ All clients received broadcast")
            
        finally:
            for client in clients:
                client.disconnect()


class TestWebSocketReconnection(unittest.TestCase):
    """Test suite for WebSocket reconnection scenarios"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.test_user = create_test_user()
        cls.token = cls.test_user["token"]
        cls.headers = get_auth_headers(cls.token)
        print(f"\n{'='*60}")
        print("Testing WebSocket Reconnection")
        print(f"{'='*60}\n")

    def test_01_reconnect_receives_new_pins(self):
        """Test that reconnected client receives new pins"""
        print("\n[TEST] Testing reconnection and receiving new pins...")
        
        # First connection
        client = WebSocketClient(WS_URL, self.token)
        connected = client.connect()
        self.assertTrue(connected)
        
        # Disconnect
        client.disconnect()
        time.sleep(0.5)
        
        # Reconnect
        client = WebSocketClient(WS_URL, self.token)
        connected = client.connect()
        self.assertTrue(connected, "Should reconnect successfully")
        
        try:
            time.sleep(0.5)
            client.clear_messages()
            
            # Create a pin after reconnection
            form_data = {
                "lat": str(USC_CENTER["lat"]),
                "lng": str(USC_CENTER["lng"]),
                "description": f"Reconnection test {generate_random_suffix()}"
            }
            
            response = requests.post(
                f"{BASE_URL}{PINS_ENDPOINT}",
                data=form_data,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )
            
            self.assertEqual(response.status_code, 201)
            created_pin = response.json()
            
            # Wait for broadcast
            time.sleep(1)
            
            # Check received
            messages = client.get_messages()
            found = any(msg.get("pinID") == created_pin["pinID"] for msg in messages)
            self.assertTrue(found, "Reconnected client should receive new pins")
            
            print("  ✓ Reconnected client receives new pins")
            
        finally:
            client.disconnect()


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
    
    # Check if websocket-client is installed
    try:
        import websocket
    except ImportError:
        print("\n" + "="*60)
        print("✗ ERROR: websocket-client not installed!")
        print("="*60)
        print("\nPlease install it:")
        print("  pip install websocket-client")
        print("="*60 + "\n")
        return
    
    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWebSocketConnection))
    suite.addTests(loader.loadTestsFromTestCase(TestWebSocketBroadcast))
    suite.addTests(loader.loadTestsFromTestCase(TestWebSocketReconnection))
    
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

