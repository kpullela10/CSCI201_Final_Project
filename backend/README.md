# Squirrel Spotter USC - Backend

Java/Spring Boot backend for the Squirrel Spotter USC web application.

## 🚀 Production Deployment

**Backend URL:** `https://csci201finalproject-production.up.railway.app`

The backend is fully deployed on Railway with:
- ✅ MySQL database on Railway
- ✅ JWT authentication
- ✅ WebSocket support for real-time updates
- ✅ Image upload and external URL support
- ✅ CORS configured for Vercel frontend

## ✅ Implemented Features

- **User Authentication**
  - Signup with USC email validation (`@usc.edu` required)
  - Login with email/password
  - JWT token generation and validation
  - Argon2 password hashing (secure)

- **Database**
  - MySQL database schema (Users, Pins tables)
  - JPA entities and repositories
  - Auto-generated schema initialization

- **Security**
  - Spring Security configuration
  - JWT-based authentication filter
  - CORS configuration for frontend integration
  - Public endpoints: `/api/auth/signup`, `/api/auth/login`

## ✅ Completed Features

### Pin/Maps Module
- ✅ `PinRepository` interface with JPA queries
- ✅ `PinService` with:
  - `createPin()` - Create new pin with image upload or external URL
  - `getWeeklyPins()` - Get pins from last 7 days
  - `getMyPins()` - Get authenticated user's pins
  - `getPinById()` - Get pin details
  - Rate limiting (4-5 pins per 30 minutes)
- ✅ `PinController` with REST endpoints
- ✅ WebSocket for real-time pin updates (`/ws/pins`)
- ✅ Image upload handling (multipart/form-data)
- ✅ External image URL support (for default images from Pexels/Unsplash)

### Leaderboard Module
- ✅ `LeaderboardService` with:
  - `getWeeklyLeaderboard()` - Top users by weekly pins
  - `getAllTimeLeaderboard()` - Top users by total pins
  - `getUserPins()` - Get all pins by a user
- ✅ `LeaderboardController` with REST endpoints
- ✅ Pagination support (20 entries per page)

## Prerequisites

- **Java 17** or higher
- **Maven** 3.6+
- **MySQL** 8.0+ (or Railway MySQL instance)
- **Git**

## Setup Instructions

### 1. Install MySQL Locally (or use Railway)

#### Option A: Local MySQL
```bash
# Install MySQL (macOS with Homebrew)
brew install mysql
brew services start mysql

# Create database
mysql -u root -p
CREATE DATABASE squirrel_spotter;
EXIT;
```

#### Option B: Railway MySQL
- Create a MySQL instance on [Railway](https://railway.app/)
- Note the connection details (host, port, database, username, password)

### 2. Configure Database Connection

Edit `src/main/resources/application.properties`:

```properties
# For local MySQL
spring.datasource.url=jdbc:mysql://localhost:3306/squirrel_spotter?useSSL=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=your_password

# For Railway MySQL
spring.datasource.url=jdbc:mysql://RAILWAY_HOST:PORT/railway?useSSL=true
spring.datasource.username=RAILWAY_USERNAME
spring.datasource.password=RAILWAY_PASSWORD
```

**Important:** Change the `jwt.secret` to a long, random string (minimum 256 bits).

### 3. Build and Run

```bash
# Navigate to backend directory
cd backend

# Clean and build
mvn clean install

# Run the application
mvn spring-boot:run
```

The backend will start on **http://localhost:8080**

### 4. Initialize Database (Optional)

If using the SQL script manually:

```bash
mysql -u root -p squirrel_spotter < src/main/resources/schema.sql
```

Otherwise, Hibernate will auto-create tables based on JPA entities (`spring.jpa.hibernate.ddl-auto=update`).

## API Endpoints

### Authentication

#### POST `/api/auth/signup`
Register a new user.

**Request:**
```json
{
  "email": "user@usc.edu",
  "username": "testuser",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "userID": 1,
    "username": "testuser",
    "email": "user@usc.edu"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input (non-USC email, missing fields)
- `409 Conflict` - Email or username already exists

#### POST `/api/auth/login`
Login with existing account.

**Request:**
```json
{
  "email": "user@usc.edu",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "userID": 1,
    "username": "testuser",
    "email": "user@usc.edu"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Missing fields
- `401 Unauthorized` - Invalid credentials

### Pins

#### POST `/api/pins`
Create a new pin. Supports both file uploads and external image URLs.

**Request (with file upload):**
```
Content-Type: multipart/form-data
- latitude: double
- longitude: double
- description: string
- image: file (optional)
```

**Request (with external URL):**
```
Content-Type: application/json
{
  "latitude": 34.0224,
  "longitude": -118.2851,
  "description": "Saw a squirrel!",
  "image_url": "https://images.pexels.com/photos/..."
}
```

**Response (200 OK):**
```json
{
  "pinID": 1,
  "latitude": 34.0224,
  "longitude": -118.2851,
  "description": "Saw a squirrel!",
  "imageUrl": "https://images.pexels.com/photos/...",
  "userID": 1,
  "username": "testuser",
  "createdAt": "2025-12-05T02:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid input or rate limit exceeded
- `401 Unauthorized` - Missing or invalid JWT token

#### GET `/api/pins/weekly`
Get all pins from the last 7 days.

**Response (200 OK):**
```json
[
  {
    "pinID": 1,
    "latitude": 34.0224,
    "longitude": -118.2851,
    "description": "Saw a squirrel!",
    "imageUrl": "https://...",
    "userID": 1,
    "username": "testuser",
    "createdAt": "2025-12-05T02:00:00"
  }
]
```

#### GET `/api/pins/my`
Get current authenticated user's pins.

#### GET `/api/pins/:pinID`
Get pin details by ID.

### Leaderboard

#### GET `/api/leaderboard?type={weekly|all-time}&page={page}&pageSize={size}`
Get leaderboard with pagination.

**Query Parameters:**
- `type`: `weekly` or `all-time` (default: `weekly`)
- `page`: Page number (default: 1)
- `pageSize`: Entries per page (default: 20)

**Response (200 OK):**
```json
{
  "users": [
    {
      "userID": 1,
      "username": "testuser",
      "pinCount": 5
    }
  ],
  "currentPage": 1,
  "totalPages": 1,
  "totalUsers": 1
}
```

#### GET `/api/users/:userID/pins`
Get all pins by a specific user.

### WebSocket

#### `/ws/pins`
Real-time pin updates. Connect using WebSocket:
- Production: `wss://your-backend.railway.app/ws/pins`
- Local: `ws://localhost:8080/ws/pins`

The server broadcasts new pin creations to all connected clients.

### Protected Endpoints (Require JWT Token)

Include the token in the `Authorization` header:
```
Authorization: Bearer <your_jwt_token>
```

**Example with curl:**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/pins/my
```

## Testing with cURL

### Test Signup
```bash
curl -X POST http://localhost:8080/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@usc.edu",
    "username": "testuser",
    "password": "password123"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@usc.edu",
    "password": "password123"
  }'
```

### Test Invalid Email (Non-USC)
```bash
curl -X POST http://localhost:8080/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@gmail.com",
    "username": "testuser",
    "password": "password123"
  }'
```

Expected: `400 Bad Request` with error message "Email must be a USC email (@usc.edu)"

## Testing with Postman

1. **Install Postman** (https://www.postman.com/)
2. **Create a new POST request** to `http://localhost:8080/api/auth/signup`
3. **Set headers:** `Content-Type: application/json`
4. **Set body (raw JSON):**
   ```json
   {
     "email": "test@usc.edu",
     "username": "testuser",
     "password": "password123"
   }
   ```
5. **Send request** - you should get a JWT token in the response
6. **Test login** with the same credentials at `/api/auth/login`

## Project Structure

```
backend/
├── src/main/java/com/usc/squirrelspotter/
│   ├── SquirrelSpotterApplication.java  # Main application class
│   ├── config/
│   │   ├── SecurityConfig.java          # Spring Security configuration
│   │   └── CorsConfig.java              # CORS configuration
│   ├── model/
│   │   ├── User.java                    # User entity (JPA)
│   │   └── Pin.java                     # Pin entity (TODO: Pin team)
│   ├── repository/
│   │   └── UserRepository.java          # JPA repository for users
│   ├── service/
│   │   └── AuthService.java             # Authentication business logic
│   ├── controller/
│   │   └── AuthController.java          # REST endpoints for auth
│   ├── security/
│   │   ├── JwtUtil.java                 # JWT token utilities
│   │   └── JwtAuthenticationFilter.java # JWT filter for requests
│   ├── dto/                             # Data Transfer Objects
│   │   ├── SignupRequest.java
│   │   ├── LoginRequest.java
│   │   ├── AuthResponse.java
│   │   ├── UserResponse.java
│   │   └── ErrorResponse.java
│   └── exception/                       # Custom exceptions
│       ├── AuthenticationException.java
│       ├── BadRequestException.java
│       └── ConflictException.java
├── src/main/resources/
│   ├── application.properties           # Configuration
│   └── schema.sql                       # Database schema
├── uploads/                             # Image storage (for Pin team)
├── pom.xml                              # Maven dependencies
└── README.md                            # This file
```

## Deployment to Railway

### 1. Create Railway Project
1. Go to [Railway](https://railway.app/)
2. Create a new project
3. Add a **MySQL database** service
4. Note the database connection details

### 2. Configure Environment Variables

In Railway dashboard, set these environment variables:

```
DATABASE_URL=jdbc:mysql://RAILWAY_MYSQL_HOST:PORT/railway?useSSL=true
DATABASE_USERNAME=root
DATABASE_PASSWORD=RAILWAY_MYSQL_PASSWORD
JWT_SECRET=your-very-long-secure-random-secret-key
```

### 3. Deploy Backend

```bash
# Railway CLI (recommended)
railway login
railway link
railway up

# Or connect GitHub repository
# Railway will auto-detect Spring Boot and deploy
```

### 4. Update Frontend Environment

Update `frontend/.env`:
```
VITE_API_BASE_URL=https://your-backend.railway.app
```

## Recent Updates

### Image Handling
- ✅ Added support for external image URLs via `image_url` parameter
- ✅ Default images from Pexels/Unsplash can be stored directly (no file upload needed)
- ✅ File uploads still supported for custom images
- ✅ External URLs stored directly in database, avoiding ephemeral filesystem issues on Railway

### WebSocket Configuration
- ✅ Secure WebSocket (`wss://`) automatically used for HTTPS backends
- ✅ Real-time pin updates working in production
- ✅ Frontend automatically detects and uses correct protocol

### Security Configuration
- ✅ `/uploads/**` path configured for static file access
- ✅ CORS configured for Vercel frontend deployment
- ✅ JWT authentication on all protected endpoints

## Security Notes

- **Passwords:** Hashed with Argon2 (industry-standard, secure)
- **JWT Tokens:** 24-hour expiration (configurable in `application.properties`)
- **CORS:** Configured to allow frontend origins (Vercel deployment)
- **Email Validation:** Only `@usc.edu` emails allowed for signup
- **Rate Limiting:** Pin creation limited to 4-5 pins per 30 minutes per user
- **Static Resources:** `/uploads/**` path configured for image access

## Troubleshooting

### MySQL Connection Error
```
com.mysql.cj.jdbc.exceptions.CommunicationsException: Communications link failure
```

**Solution:** Check MySQL is running and connection details in `application.properties` are correct.

### JWT Token Invalid
```
401 Unauthorized
```

**Solution:** Token may be expired or invalid. Re-login to get a new token.

### Port Already in Use
```
Port 8080 was already in use
```

**Solution:** Kill the process using port 8080 or change `server.port` in `application.properties`.

## Production Deployment Notes

### Railway Deployment
- Backend is deployed on Railway at `https://csci201finalproject-production.up.railway.app`
- MySQL database hosted on Railway (ephemeral filesystem)
- Environment variables configured in Railway dashboard

### Image Storage Considerations
- **Uploaded files:** Stored in `/uploads/` directory (ephemeral on Railway)
- **External URLs:** Recommended for production (default images from Pexels/Unsplash)
- **Future improvement:** Consider cloud storage (S3, Cloudinary) for persistent file uploads

### WebSocket in Production
- Frontend automatically uses `wss://` (secure WebSocket) for HTTPS backends
- WebSocket endpoint: `/ws/pins`
- Real-time updates working correctly in production environment

## Documentation

- Full API specification: `../BACKEND_INTEGRATION.md`
- Frontend documentation: `../frontend/README.md`
- Project documentation: `../README.md`

## Contact

For questions about the authentication module, refer to:
- `src/service/AuthService.java` - Core authentication logic
- `src/security/JwtUtil.java` - JWT token handling
- `src/config/SecurityConfig.java` - Security configuration

Good luck! 🐿️
