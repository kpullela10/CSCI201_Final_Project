# Backend Integration Guide - Squirrel Spotter USC

## Overview

This document outlines what the frontend team has implemented and what the backend team needs to build to complete the Squirrel Spotter USC web application.

**Frontend Status:** ✅ Complete and ready for integration  
**Backend Status:** ⚠️ Needs implementation

---

## Frontend Implementation Summary

### What We Built

1. **Complete React + TypeScript Frontend**
   - React 18 with TypeScript
   - React Router for navigation
   - Tailwind CSS for styling
   - Leaflet maps (OpenStreetMap tiles)
   - Real-time updates via WebSocket with polling fallback

2. **Pages & Features**
   - Landing page: Map view (accessible to all users)
   - Authentication: Login/Signup pages with USC email validation
   - Map page: Interactive map with pin dropping (authenticated users only)
   - Leaderboard: Weekly and all-time rankings with pagination
   - Pin management: Create pins with images, view pin details

3. **Key Features**
   - Token-based authentication (JWT expected)
   - Real-time pin updates via WebSocket
   - Image uploads (multipart/form-data)
   - Default image selection (6 pre-selected squirrel images)
   - Rate limiting error handling (HTTP 429)
   - Responsive design

---

## API Endpoints Required

### Base URL
- Default: `http://localhost:8080`
- Configurable via `VITE_API_BASE_URL` environment variable

### Authentication Endpoints

#### POST `/api/auth/signup`
**Request:**
```json
{
  "email": "user@usc.edu",
  "username": "username",
  "password": "password"
}
```

**Response (200 OK):**
```json
{
  "token": "jwt_token_string",
  "user": {
    "userID": 1,
    "username": "username",
    "email": "user@usc.edu"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (email format, missing fields, etc.)
- `409 Conflict`: Email or username already exists
- `500 Internal Server Error`: Server error

**Validation Requirements:**
- Email must contain `@usc.edu`
- Username: non-empty, unique
- Password: non-empty (frontend validates, backend should enforce minimum requirements)

---

#### POST `/api/auth/login`
**Request:**
```json
{
  "email": "user@usc.edu",
  "password": "password"
}
```

**Response (200 OK):**
```json
{
  "token": "jwt_token_string",
  "user": {
    "userID": 1,
    "username": "username",
    "email": "user@usc.edu"
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `400 Bad Request`: Missing fields
- `500 Internal Server Error`: Server error

---

### Pin Endpoints

#### GET `/api/pins/weekly`
**Description:** Get all pins created in the current week

**Headers:**
- `Authorization: Bearer <token>` (optional - for authenticated users)

**Response (200 OK):**
```json
[
  {
    "pinID": 1,
    "userID": 1,
    "lat": 34.0224,
    "lng": -118.2851,
    "description": "Spotted a gray squirrel near the library",
    "created_at": "2024-01-15T10:30:00Z",
    "image_url": "https://example.com/images/pin1.jpg",
    "username": "testuser"
  },
  ...
]
```

**Notes:**
- Should return pins from the current week (Monday-Sunday or last 7 days)
- Include `username` field for display purposes
- Should be accessible to unauthenticated users (for viewing map)

---

#### GET `/api/pins/my`
**Description:** Get current authenticated user's pins

**Headers:**
- `Authorization: Bearer <token>` (required)

**Response (200 OK):**
```json
[
  {
    "pinID": 1,
    "userID": 1,
    "lat": 34.0224,
    "lng": -118.2851,
    "description": "My pin",
    "created_at": "2024-01-15T10:30:00Z",
    "image_url": "https://example.com/images/pin1.jpg",
    "username": "testuser"
  },
  ...
]
```

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token

---

#### POST `/api/pins`
**Description:** Create a new pin

**Headers:**
- `Authorization: Bearer <token>` (required)
- `Content-Type: multipart/form-data` (automatically set by browser)

**Request Body (FormData):**
- `lat`: string (required) - Latitude
- `lng`: string (required) - Longitude
- `description`: string (optional) - Pin description
- `image`: File (optional) - Uploaded image file
- `image_url`: string (optional) - URL of default image (if user selected default image instead of uploading)

**Note:** Either `image` OR `image_url` will be sent, not both.

**Response (201 Created):**
```json
{
  "pinID": 1,
  "userID": 1,
  "lat": 34.0224,
  "lng": -118.2851,
  "description": "Spotted a gray squirrel",
  "created_at": "2024-01-15T10:30:00Z",
  "image_url": "https://example.com/images/pin1.jpg",
  "username": "testuser"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid input (missing lat/lng, invalid coordinates)
- `401 Unauthorized`: Missing or invalid token
- `429 Too Many Requests`: Rate limit exceeded (4-5 pins per 30 minutes)
- `413 Payload Too Large`: Image file too large
- `500 Internal Server Error`: Server error

**Rate Limiting:**
- Enforce limit: 4-5 pins per user per 30 minutes
- Return HTTP 429 with appropriate error message
- Frontend displays: "You've reached the pin limit (4–5 pins per 30 minutes). Try again later."

**Image Handling:**
- If `image` file is provided: Upload and store image, return URL in `image_url`
- If `image_url` is provided: Use the provided URL (default image selected by user)
- Recommended: Store images in cloud storage (S3, Cloudinary, etc.) or local file system
- Return full URL in `image_url` field

---

#### GET `/api/pins/:pinID`
**Description:** Get a specific pin by ID

**Headers:**
- `Authorization: Bearer <token>` (optional)

**Response (200 OK):**
```json
{
  "pinID": 1,
  "userID": 1,
  "lat": 34.0224,
  "lng": -118.2851,
  "description": "Spotted a gray squirrel",
  "created_at": "2024-01-15T10:30:00Z",
  "image_url": "https://example.com/images/pin1.jpg",
  "username": "testuser"
}
```

**Error Responses:**
- `404 Not Found`: Pin not found
- `500 Internal Server Error`: Server error

---

### Leaderboard Endpoints

#### GET `/api/leaderboard`
**Description:** Get leaderboard entries

**Query Parameters:**
- `type`: string (required) - Either `"weekly"` or `"all-time"`
- `page`: number (required) - Page number (1-indexed)
- `pageSize`: number (required) - Number of entries per page (typically 20)

**Example:** `/api/leaderboard?type=weekly&page=1&pageSize=20`

**Headers:**
- `Authorization: Bearer <token>` (optional)

**Response (200 OK):**
```json
{
  "entries": [
    {
      "userID": 1,
      "username": "testuser",
      "total_pins": 50,
      "weekly_pins": 12
    },
    ...
  ],
  "totalCount": 150
}
```

**Notes:**
- `weekly_pins`: Count of pins created in current week
- `total_pins`: Total count of all pins by user
- Entries should be sorted by `weekly_pins` (desc) for weekly, `total_pins` (desc) for all-time
- `totalCount`: Total number of users (for pagination)

---

#### GET `/api/users/:userID/pins`
**Description:** Get all pins by a specific user

**Headers:**
- `Authorization: Bearer <token>` (optional)

**Response (200 OK):**
```json
[
  {
    "pinID": 1,
    "userID": 1,
    "lat": 34.0224,
    "lng": -118.2851,
    "description": "Spotted a gray squirrel",
    "created_at": "2024-01-15T10:30:00Z",
    "image_url": "https://example.com/images/pin1.jpg",
    "username": "testuser"
  },
  ...
]
```

**Error Responses:**
- `404 Not Found`: User not found
- `500 Internal Server Error`: Server error

---

### WebSocket Endpoint

#### WebSocket `/ws/pins`
**Description:** Real-time pin updates

**Connection URL:**
- `ws://localhost:8080/ws/pins` (unauthenticated)
- `ws://localhost:8080/ws/pins?token=<jwt_token>` (authenticated)

**Message Format:**
- Send: No messages sent from client
- Receive: JSON messages with Pin objects or arrays of Pins

**Example Messages:**
```json
// Single pin update
{
  "pinID": 1,
  "userID": 1,
  "lat": 34.0224,
  "lng": -118.2851,
  "description": "New pin",
  "created_at": "2024-01-15T10:30:00Z",
  "image_url": "https://example.com/images/pin1.jpg",
  "username": "testuser"
}

// Or array of pins
[
  { "pinID": 1, ... },
  { "pinID": 2, ... }
]
```

**Behavior:**
- Broadcast new pins to all connected clients when a pin is created
- Frontend merges received pins into existing list (deduplicates by pinID)
- Frontend falls back to polling every 30 seconds if WebSocket fails

**Authentication:**
- Optional: Can accept token via query parameter
- Unauthenticated users should still receive pin updates (for viewing map)

---

## Data Models

### User
```typescript
interface User {
  userID: number;        // Primary key
  username: string;     // Unique, non-empty
  email: string;        // Unique, must contain @usc.edu
  // password: never returned in API responses
}
```

### Pin
```typescript
interface Pin {
  pinID: number;         // Primary key
  userID: number;        // Foreign key to User
  lat: number;           // Latitude (-90 to 90)
  lng: number;           // Longitude (-180 to 180)
  description?: string;  // Optional description
  created_at: string;   // ISO 8601 timestamp (e.g., "2024-01-15T10:30:00Z")
  image_url?: string;    // Full URL to image (optional)
  username?: string;     // Populated by backend for display (join with User table)
}
```

### LeaderboardEntry
```typescript
interface LeaderboardEntry {
  userID: number;        // Foreign key to User
  username: string;      // User's username
  total_pins: number;    // Total count of all pins
  weekly_pins: number;   // Count of pins in current week
}
```

---

## Authentication & Security

### JWT Token
- **Format:** Bearer token in `Authorization` header
- **Storage:** Frontend stores in `localStorage` (key: `authToken`)
- **Validation:** Backend should validate token on protected endpoints
- **Expiration:** Backend should handle token expiration (frontend will need to re-authenticate)

### Protected Endpoints
- `POST /api/pins` - Requires authentication
- `GET /api/pins/my` - Requires authentication
- All other endpoints should work without authentication (for viewing map)

### Password Security
- **Hashing:** Backend MUST hash passwords (never store plaintext)
- **Recommendation:** Use bcrypt, Argon2, or similar
- Frontend sends passwords in plaintext over HTTPS (backend responsibility to hash)

### CORS
- **Required:** Enable CORS for frontend origin
- **Recommended:** Allow `http://localhost:5173` (Vite dev server) and production domain
- **Headers:** Allow `Authorization`, `Content-Type`

---

## Error Handling

### Standard Error Response Format
```json
{
  "message": "Error description"
}
```

### HTTP Status Codes
- `200 OK`: Success
- `201 Created`: Resource created (pin creation)
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing/invalid authentication
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (duplicate email/username)
- `413 Payload Too Large`: File too large
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

---

## Rate Limiting

### Pin Creation
- **Limit:** 4-5 pins per user per 30 minutes
- **Response:** HTTP 429 with error message
- **Frontend Message:** "You've reached the pin limit (4–5 pins per 30 minutes). Try again later."

### Implementation Notes
- Track pin creation timestamps per user
- Reset counter after 30 minutes
- Consider using Redis or similar for distributed rate limiting

---

## Image Handling

### Image Upload
- **Format:** `multipart/form-data`
- **Field Name:** `image`
- **Accepted Types:** Any image format (jpg, png, gif, webp, etc.)
- **Size Limit:** Recommend 5-10MB max
- **Storage:** 
  - Option 1: Cloud storage (AWS S3, Cloudinary, etc.) - Recommended
  - Option 2: Local file system with URL serving
- **Return:** Full URL in `image_url` field

### Default Images
- Frontend provides 6 default squirrel images (Pixabay URLs)
- If user selects default image, frontend sends `image_url` field instead of `image` file
- Backend should accept and store the provided URL

---

## Database Schema Recommendations

### Users Table
```sql
CREATE TABLE users (
  userID INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Pins Table
```sql
CREATE TABLE pins (
  pinID INT PRIMARY KEY AUTO_INCREMENT,
  userID INT NOT NULL,
  lat DECIMAL(10, 8) NOT NULL,
  lng DECIMAL(11, 8) NOT NULL,
  description TEXT,
  image_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
  INDEX idx_created_at (created_at),
  INDEX idx_user_created (userID, created_at)
);
```

### Weekly Reset
- Consider a cron job or scheduled task to reset weekly pin counts
- Or calculate weekly pins dynamically based on `created_at` timestamp

---

## Testing Checklist

### Authentication
- [ ] Signup with valid USC email
- [ ] Signup with duplicate email (should fail)
- [ ] Login with valid credentials
- [ ] Login with invalid credentials (should fail)
- [ ] Token validation on protected endpoints

### Pins
- [ ] Create pin with image upload
- [ ] Create pin with default image URL
- [ ] Create pin without image
- [ ] Get weekly pins (unauthenticated)
- [ ] Get user's pins (authenticated)
- [ ] Rate limiting (4-5 pins per 30 min)
- [ ] Invalid coordinates handling

### Leaderboard
- [ ] Weekly leaderboard with pagination
- [ ] All-time leaderboard with pagination
- [ ] Get user pins by userID
- [ ] Sorting (by weekly_pins and total_pins)

### WebSocket
- [ ] Connect without authentication
- [ ] Connect with authentication
- [ ] Receive pin updates in real-time
- [ ] Handle connection failures gracefully

### Image Handling
- [ ] Accept image file uploads
- [ ] Accept image URLs (default images)
- [ ] Validate image file size
- [ ] Return proper image URLs

---

## Environment Variables

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8080
```

### Backend (Recommended)
```env
DATABASE_URL=...
JWT_SECRET=...
IMAGE_STORAGE_PATH=... (or cloud storage credentials)
CORS_ORIGIN=http://localhost:5173
```

---

## Integration Steps

1. **Set up backend server** on port 8080 (or update frontend `.env`)
2. **Implement authentication endpoints** (`/api/auth/login`, `/api/auth/signup`)
3. **Implement pin endpoints** (`/api/pins/*`)
4. **Implement leaderboard endpoints** (`/api/leaderboard`, `/api/users/:userID/pins`)
5. **Set up WebSocket server** (`/ws/pins`)
6. **Configure CORS** for frontend origin
7. **Set up image storage** (cloud or local)
8. **Implement rate limiting** for pin creation
9. **Test all endpoints** with frontend
10. **Deploy** both frontend and backend

---

## Frontend Contact & Support

If you have questions about the frontend implementation or need clarification on any API requirements, please refer to:
- `src/api/` - API client implementations
- `src/types/index.ts` - TypeScript type definitions
- `README.md` - Frontend documentation

---

## Notes

- Frontend is **production-ready** and fully functional
- All API calls include proper error handling
- WebSocket has automatic reconnection and polling fallback
- Frontend validates USC emails (`@usc.edu` required)
- Map is accessible to all users; pin creation requires authentication
- Default images are provided by frontend (Pixabay URLs)

**Good luck with the backend implementation! 🐿️**

