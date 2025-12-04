# Backend Unit Tests

This directory contains comprehensive unit tests for the Squirrel Spotter backend services.

## Test Coverage

### AuthServiceTest
Tests authentication and authorization functionality:
- ✅ User signup with validation
- ✅ Email uniqueness checks
- ✅ Username uniqueness checks
- ✅ USC email validation (@usc.edu)
- ✅ Password requirements
- ✅ User login
- ✅ JWT token generation
- ✅ User retrieval by ID
- ✅ Error handling for invalid credentials

**Test Count**: 14 tests

### PinServiceTest
Tests pin creation, retrieval, and management:
- ✅ Pin creation with and without images
- ✅ Coordinate validation (latitude -90 to 90, longitude -180 to 180)
- ✅ Rate limiting (5 pins per 30 minutes)
- ✅ Image upload handling
- ✅ Weekly pins retrieval
- ✅ User's pins retrieval
- ✅ Pin retrieval by ID
- ✅ WebSocket broadcasting
- ✅ Error handling for invalid inputs

**Test Count**: 17 tests

### LeaderboardServiceTest
Tests leaderboard functionality:
- ✅ Weekly leaderboard retrieval
- ✅ All-time leaderboard retrieval
- ✅ Pagination (pages, page size)
- ✅ Empty results handling
- ✅ Invalid type validation
- ✅ User pins retrieval
- ✅ Case-insensitive type matching
- ✅ Boundary testing for pagination

**Test Count**: 15 tests

**Total Tests**: 46 unit tests

## Setup Instructions

### 1. Copy tests to your project
Copy these test files to your backend test directory:

```bash
cp AuthServiceTest.java backend/src/test/java/com/usc/squirrelspotter/service/
cp PinServiceTest.java backend/src/test/java/com/usc/squirrelspotter/service/
cp LeaderboardServiceTest.java backend/src/test/java/com/usc/squirrelspotter/service/
```

### 2. Verify Dependencies
Make sure your `pom.xml` includes these test dependencies (already present):

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>org.springframework.security</groupId>
    <artifactId>spring-security-test</artifactId>
    <scope>test</scope>
</dependency>
```

## Running the Tests

### Run all tests
```bash
cd backend
mvn test
```

### Run specific test class
```bash
mvn test -Dtest=AuthServiceTest
mvn test -Dtest=PinServiceTest
mvn test -Dtest=LeaderboardServiceTest
```

### Run specific test method
```bash
mvn test -Dtest=AuthServiceTest#testSignup_Success
mvn test -Dtest=PinServiceTest#testCreatePin_RateLimitExceeded_ThrowsTooManyRequestsException
```
