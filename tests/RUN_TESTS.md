# Running Backend Tests

## Prerequisites

- Python 3.7+
- `requests` library
- Backend running at `http://localhost:8080`

## Setup

Install Python dependencies:

```bash
pip install requests
```

Or using the requirements file:

```bash
cd tests
pip install -r requirements.txt
```

## Run Authentication Tests

### Step 1: Start the Backend

In one terminal:

```bash
cd backend
mvn spring-boot:run
```

Wait for: `Started SquirrelSpotterApplication`

### Step 2: Run Tests

In another terminal:

```bash
cd tests/account_creation_tests
python run_tests.py
```

Or run directly:

```bash
python test_account_creation.py
```

## What the Tests Verify

✅ **Account Creation:**
- Valid USC email signup
- Duplicate email/username rejection
- Non-USC email rejection
- Missing fields validation
- Empty fields validation

✅ **Login:**
- Successful login after signup
- Wrong password rejection
- Non-existent user rejection

✅ **Security:**
- Passwords are hashed with Argon2
- Passwords not exposed in API responses
- JWT tokens generated correctly

✅ **Database:**
- Users are stored in Railway MySQL
- Login works after signup (verifies hashing)

## Expected Output

```
============================================================
Testing Authentication Endpoints
Base URL: http://localhost:8080
Signup: http://localhost:8080/api/auth/signup
Login: http://localhost:8080/api/auth/login
============================================================

test_01_valid_account_creation ...
[TEST] Valid account creation...
  Status Code: 200
  Response: {'token': 'eyJ...', 'user': {...}}
  ✓ Account created successfully with JWT token
ok

test_02_duplicate_email ...
[TEST] Duplicate email rejection...
  Status Code: 409
  Response: {'message': 'Email already exists'}
  ✓ Duplicate email properly rejected
ok

... (13 tests total)

============================================================
TEST SUMMARY
============================================================
Tests run: 13
Successes: 13
Failures: 0
Errors: 0
============================================================
```

## Troubleshooting

### Backend Not Running

```
✗ ERROR: Backend is not running!

Please start the backend first:
  cd backend
  mvn spring-boot:run
```

**Solution:** Start the backend first!

### Connection Refused

```
requests.exceptions.ConnectionError: Connection refused
```

**Solution:** Verify backend is running on port 8080

### Tests Failing

Check backend logs for errors:
```bash
# Backend terminal should show SQL queries and requests
```

Common issues:
- Database connection failed (check Railway MySQL)
- Port 8080 already in use
- Maven dependencies not installed

## Test Structure

```
tests/
├── account_creation_tests/
│   ├── test_account_creation.py  # Main test suite
│   ├── run_tests.py              # Test runner with backend check
│   └── config.py                 # Configuration
├── pin_tests/                    # TODO: Pin/Maps team
├── leaderboard_tests/            # TODO: Leaderboard team
└── requirements.txt              # Python dependencies
```

## Running Individual Tests

Run a specific test:

```bash
python test_account_creation.py TestAccountCreation.test_01_valid_account_creation
```

Run tests matching a pattern:

```bash
python -m unittest test_account_creation.TestAccountCreation.test_*_login_*
```

## CI/CD Integration

These tests can be integrated into CI/CD:

```yaml
# Example GitHub Actions
- name: Run Authentication Tests
  run: |
    python tests/account_creation_tests/run_tests.py
```

## Next Steps

- **Pin/Maps Team:** Add tests in `tests/pin_tests/`
- **Leaderboard Team:** Add tests in `tests/leaderboard_tests/`

Good luck! 🐿️
