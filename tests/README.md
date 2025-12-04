# Squirrel Spotter USC - Test Suite 🐿️

Comprehensive API and integration tests for the Squirrel Spotter backend.

## Quick Start

```bash
# 1. Start the backend (in one terminal)
cd backend
mvn spring-boot:run -Dspring-boot.run.profiles=dev

# 2. Run tests (in another terminal)
cd tests
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_all_tests.py
```

## Test Suites

| Suite | Tests | Description |
|-------|-------|-------------|
| **Account Creation** | 13 | Signup, login, validation, password hashing |
| **Pin API** | 18 | Pin CRUD, rate limiting, image upload |
| **Leaderboard API** | 16 | Rankings, pagination, sorting |
| **WebSocket** | 6 | Real-time connections and broadcasts |
| **Total** | **53** | |

## Prerequisites

- Python 3.7+
- Backend running at `http://localhost:8080`

## Installation

```bash
cd tests

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

### Run All Tests
```bash
python run_all_tests.py
```

### Run Individual Suites

```bash
# Account/Auth tests
cd account_creation_tests
python test_account_creation.py

# Pin tests
cd pin_tests
python test_pins.py

# Leaderboard tests
cd leaderboard_tests
python test_leaderboard_api.py

# WebSocket tests
cd websocket_tests
python test_websocket.py
```

## Test Details

### Account Creation Tests (`account_creation_tests/`)
- ✅ Valid USC email signup
- ✅ Duplicate email/username rejection
- ✅ Non-USC email rejection (@usc.edu required)
- ✅ Missing/empty field validation
- ✅ Login after signup
- ✅ Wrong password rejection
- ✅ Argon2 password hashing verification

### Pin API Tests (`pin_tests/`)
- ✅ Create pin with form-data
- ✅ Create pin without description (optional)
- ✅ Missing coordinate validation
- ✅ Invalid coordinate range (-90 to 90 lat, -180 to 180 lng)
- ✅ Unauthorized pin creation (401)
- ✅ Rate limiting (5 pins per 30 minutes)
- ✅ Get weekly pins (public)
- ✅ Get my pins (authenticated)
- ✅ Get pin by ID
- ✅ Get nonexistent pin (404)
- ✅ Image upload with pin

### Leaderboard API Tests (`leaderboard_tests/`)
- ✅ Weekly leaderboard retrieval
- ✅ All-time leaderboard retrieval
- ✅ Invalid type parameter validation
- ✅ Pagination (default page size: 20)
- ✅ Custom page size
- ✅ Page navigation
- ✅ Invalid page/pageSize values
- ✅ Sorting verification (descending order)
- ✅ New user appears on leaderboard after pin
- ✅ Pin count increments correctly
- ✅ User pins endpoint

### WebSocket Tests (`websocket_tests/`)
- ✅ Connect without token (public viewing)
- ✅ Connect with valid JWT token
- ✅ Connect with invalid token (still allowed)
- ✅ Receive pin broadcast on creation
- ✅ Multiple clients receive broadcast
- ✅ Reconnection handling

## Project Structure

```
tests/
├── README.md                     # This file
├── run_all_tests.py              # Master test runner
├── requirements.txt              # Python dependencies
├── RUN_TESTS.md                  # Detailed instructions
│
├── account_creation_tests/
│   ├── __init__.py
│   ├── config.py
│   ├── run_tests.py
│   └── test_account_creation.py
│
├── pin_tests/
│   ├── __init__.py
│   ├── config.py
│   └── test_pins.py
│
├── leaderboard_tests/
│   ├── __init__.py
│   ├── test_leaderboard_api.py
│   └── *.sql                     # SQL test files (legacy)
│
└── websocket_tests/
    ├── __init__.py
    └── test_websocket.py
```

## Expected Output

```
======================================================================
  SQUIRREL SPOTTER USC - COMPREHENSIVE TEST SUITE
======================================================================

  ✓ PASS  Account Creation Tests
         Tests: 13, Failures: 0, Errors: 0

  ✓ PASS  Pin API Tests
         Tests: 18, Failures: 0, Errors: 0

  ✓ PASS  Leaderboard API Tests
         Tests: 16, Failures: 0, Errors: 0

  ✓ PASS  WebSocket Tests
         Tests: 6, Failures: 0, Errors: 0

----------------------------------------------------------------------

  Total Tests:    53
  Total Failures: 0
  Total Errors:   0
  Success Rate:   100.0%

  🎉 ALL TESTS PASSED! 🎉

======================================================================
```

## Troubleshooting

### Backend Not Running
```
ERROR: Backend is not running!
```
**Solution:** Start the backend with:
```bash
cd backend
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

### Missing JWT_SECRET Error
```
Could not resolve placeholder 'JWT_SECRET'
```
**Solution:** Use the dev profile which has defaults:
```bash
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

### WebSocket Tests Failing
**Solution:** Install websocket-client:
```bash
pip install websocket-client
```

### Rate Limit Tests Failing
If you've created many pins recently, wait 30 minutes or use a fresh test user.

## Adding New Tests

1. Create a new test file in the appropriate directory
2. Follow the existing test patterns (unittest-based)
3. Import in `__init__.py` if needed
4. Add to `run_all_tests.py` if it's a new suite

## CI/CD Integration

```yaml
# GitHub Actions example
- name: Run Tests
  run: |
    cd tests
    pip install -r requirements.txt
    python run_all_tests.py
```

---

**Fight On! ✌️🐿️**

