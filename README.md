# Squirrel Spotter USC - Frontend

A React + TypeScript frontend application for the Squirrel Spotter USC web app. This is a frontend-only implementation that communicates with backend REST APIs and WebSocket endpoints.

## Tech Stack

- **React 18** with TypeScript
- **React Router** for routing
- **Tailwind CSS** for styling
- **Vite** as the build tool
- **Leaflet** with React-Leaflet for map functionality (OpenStreetMap tiles)

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   
   Create a `.env` file in the root directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8080
   ```
   
   Update `VITE_API_BASE_URL` if your backend runs on a different port/URL.

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173` (or the port Vite assigns).

## Project Structure

```
src/
├── api/              # API client functions
│   ├── auth.ts       # Authentication API calls
│   ├── pins.ts       # Pin-related API calls
│   └── leaderboard.ts # Leaderboard API calls
├── components/       # Reusable React components
│   ├── AuthForm.tsx
│   ├── LeaderboardTable.tsx
│   ├── MapView.tsx
│   ├── Navbar.tsx
│   ├── PinDetailsModal.tsx
│   ├── PinForm.tsx
│   └── Tabs.tsx
├── hooks/            # Custom React hooks
│   ├── useAuth.tsx   # Authentication state management
│   └── useWebSocketPins.ts # WebSocket connection for real-time updates
├── routes/           # Page components
│   ├── HomePage.tsx
│   ├── LoginPage.tsx
│   ├── SignupPage.tsx
│   ├── MapPage.tsx
│   └── LeaderboardPage.tsx
├── types/            # TypeScript type definitions
│   └── index.ts
├── App.tsx           # Main app component with routing
├── main.tsx          # Entry point
└── index.css         # Global styles with Tailwind
```

## Features

### Authentication
- Login and signup pages with USC email validation
- Token-based authentication stored in localStorage
- Protected routes (map page requires authentication)

### Map Interface
- Leaflet map integration centered on USC campus (using OpenStreetMap tiles)
- Real-time pin updates via WebSocket (with 30s polling fallback)
- Click to drop new pins (authenticated users only)
- Filter pins: "All weekly pins" or "My pins only"
- Click markers to view pin details

### Pin Management
- Create pins with description and optional image upload
- View pin details in modal (image, description, user, time, coordinates)
- Rate limiting error handling (shows user-friendly message on 429)

### Leaderboard
- Weekly and all-time leaderboard tabs
- Pagination (20 entries per page)
- Click username to view that user's pins
- Responsive table design

## API Endpoints Expected

The frontend expects the following backend endpoints:

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/signup` - Signup

### Pins
- `GET /api/pins/weekly` - Get weekly pins
- `GET /api/pins/my` - Get current user's pins
- `POST /api/pins` - Create a new pin (multipart/form-data)
- `GET /api/pins/:pinID` - Get pin by ID

### Leaderboard
- `GET /api/leaderboard?type=weekly|all-time&page=1&pageSize=20` - Get leaderboard
- `GET /api/users/:userID/pins` - Get pins by user

### WebSocket
- `ws://<API_BASE_URL>/ws/pins` - Real-time pin updates

## Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Notes

- This is a **frontend-only** implementation. No backend code is included.
- All authentication tokens are stored in localStorage.
- The app assumes the backend will handle password hashing, rate limiting, and all security measures.
- WebSocket connection automatically falls back to polling every 30 seconds if the connection fails.
- USC email validation requires `@usc.edu` in the email address.

