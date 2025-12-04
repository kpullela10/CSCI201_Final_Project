# Running Tests - Squirrel Spotter USC

## Prerequisites

- Python 3.7+
- Backend running at `http://localhost:8080`

## Setup

Install Python dependencies:

```bash
cd tests
pip install -r requirements.txt
```

## Run All Tests

The easiest way to run all tests:

```bash
# From project root
cd tests
python run_all_tests.py
```

This will run:
- ✅ Account Creation Tests (13 tests)
- ✅ Pin API Tests (18 tests)
- ✅ Leaderboard API Tests (16 tests)
- ✅ WebSocket Tests (6 tests)

## Run Individual Test Suites

### 1. Account Creation Tests

Tests signup, login, validation, and password hashing:

```bash
cd tests/account_creation_tests
python test_account_creation.py
```

**What's tested:**
- Valid USC email signup
- Duplicate email/username rejection
- Non-USC email rejection
- Missing/empty field validation
- Login after signup
- Wrong password rejection
- Argon2 password hashing

### 2. Pin API Tests

Tests pin creation, retrieval, and rate limiting:

```bash
cd tests/pin_tests
python test_pins.py
```

**What's tested:**
- Create pin with valid data (form-data)
- Create pin without description
- Missing coordinate validation
- Invalid coordinate validation (out of range)
- Unauthorized pin creation
- Rate limiting (5 pins per 30 minutes)
- Get weekly pins (public)
- Get my pins (authenticated)
- Get pin by ID
- Get nonexistent pin (404)
- Image upload with pin

### 3. Leaderboard API Tests

Tests leaderboard retrieval, pagination, and sorting:

```bash
cd tests/leaderboard_tests
python test_leaderboard_api.py
```

**What's tested:**
- Weekly leaderboard
- All-time leaderboard
- Invalid type parameter
- Pagination (default, custom page size)
- Page navigation
- Invalid page/pageSize values
- Sorting verification
- New user appears on leaderboard
- Pin count increments
- User pins endpoint
- Case-insensitive type parameter

### 4. WebSocket Tests

Tests real-time pin broadcasting:

```bash
cd tests/websocket_tests
python test_websocket.py
```

**What's tested:**
- Connect without token
- Connect with valid token
- Connect with invalid token
- Receive pin broadcast
- Multiple clients receive broadcast
- Reconnection handling

## Test Structure

```
tests/
├── run_all_tests.py              # Master test runner
├── requirements.txt              # Python dependencies
├── RUN_TESTS.md                  # This file
│
├── account_creation_tests/
│   ├── __init__.py
│   ├── test_account_creation.py  # 13 auth tests
│   ├── run_tests.py              # Individual runner
│   └── config.py                 # Configuration
│
├── pin_tests/
│   ├── __init__.py
│   ├── test_pins.py              # 18 pin tests
│   └── config.py                 # Configuration
│
├── leaderboard_tests/
│   ├── __init__.py
│   ├── test_leaderboard_api.py   # 16 leaderboard tests
│   └── *.sql                     # SQL test files (legacy)
│
└── websocket_tests/
    ├── __init__.py
    └── test_websocket.py         # 6 WebSocket tests
```

## Expected Output

### All Tests Passing

```
======================================================================
  SQUIRREL SPOTTER USC - COMPREHENSIVE TEST SUITE
======================================================================
  Started at: 2024-12-04 10:00:00
  Backend URL: http://localhost:8080
======================================================================

Checking backend status... ✓ OK

----------------------------------------------------------------------
  Running: Account Creation Tests
----------------------------------------------------------------------

test_01_valid_account_creation ... ok
test_02_duplicate_email ... ok
...

----------------------------------------------------------------------
  Running: Pin API Tests
----------------------------------------------------------------------

test_01_create_pin_successfully ... ok
test_02_create_pin_without_description ... ok
...

======================================================================
  TEST RESULTS SUMMARY
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
  Time Elapsed:   15.42s

  🎉 ALL TESTS PASSED! 🎉

======================================================================
```

## Troubleshooting

### Backend Not Running

```
ERROR: Backend is not running!

Please start the backend first:
  cd backend
  mvn spring-boot:run
```

### WebSocket Tests Failing

Make sure `websocket-client` is installed:

```bash
pip install websocket-client
```

### Connection Refused

- Verify backend is running on port 8080
- Check if another service is using the port

### Rate Limit Tests Failing

If you've already created many pins, the rate limit test might fail.
Wait 30 minutes or use a fresh database.

### Database Issues

- Verify MySQL is running
- Check database credentials in `application.properties`
- Ensure schema is initialized

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Run All Tests
  run: |
    pip install -r tests/requirements.txt
    python tests/run_all_tests.py
```

## Test Coverage Summary

| Area | Tests | Coverage |
|------|-------|----------|
| Authentication | 13 | Signup, login, validation, security |
| Pins | 18 | CRUD, rate limiting, images, validation |
| Leaderboard | 16 | Rankings, pagination, sorting |
| WebSocket | 6 | Connections, broadcasts, reconnection |
| **Total** | **53** | |

---

**Fight On! ✌️🐿️**
