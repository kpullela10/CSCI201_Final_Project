# Squirrel Spotter USC

A full-stack web application for USC students to pin squirrel sightings on campus and compete on a leaderboard.

## 🚀 Live Demo

<div align="center">

### [👉 Try the Live Application Now 👈](https://csci-201-final-project-33qh-bww31dupo-csci201-group15-50a4b012.vercel.app)

</div>

The application is fully deployed and ready to use:
- ✅ **Frontend:** Deployed on Vercel
- ✅ **Backend:** Deployed on Railway (`https://csci201finalproject-production.up.railway.app`)
- ✅ **Database:** MySQL on Railway

**Getting Started:**
1. Click the demo link above (or use your Vercel URL)
2. Sign up with a `@usc.edu` email address
3. Start spotting squirrels on the USC campus map! 🐿️
4. Compete on the leaderboard

> **Note:** Make sure to update the demo link with your actual Vercel deployment URL after deploying the frontend.

## Project Overview

Squirrel Spotter USC allows USC students to:
- 📍 Drop pins on a map when they spot squirrels on campus
- 📸 Upload photos of squirrel sightings
- 🏆 Compete on weekly and all-time leaderboards
- 🔒 Authenticate with USC email addresses (@usc.edu)
- ⚡ See real-time updates when others spot squirrels

## Tech Stack

### Frontend
- **React 18** with TypeScript
- **React Router** for client-side routing
- **Tailwind CSS** for styling
- **Vite** as the build tool
- **Leaflet** with React-Leaflet for interactive maps (OpenStreetMap tiles)
- **WebSocket** for real-time pin updates

### Backend
- **Java 17** with Spring Boot 3.2
- **Spring Security** with JWT authentication
- **Spring Data JPA** with MySQL
- **Argon2** for secure password hashing
- **WebSocket** support for real-time features
- **Maven** for dependency management

### Database
- **MySQL 8.0+** (Railway MySQL for deployment)

### Deployment
- **Backend:** Railway
- **Frontend:** Vercel (recommended) or Netlify
- **Database:** Railway MySQL

## Features

### ✅ Implemented Features

#### Authentication
- User signup with USC email validation
- Secure login with JWT token generation
- Argon2 password hashing (industry-standard security)
- Protected routes requiring authentication

#### Map Interface
- Interactive Leaflet map centered on USC campus
- Real-time pin updates via WebSocket
- Filter pins: "All weekly pins" or "My pins only"
- Click map to drop new pins (authenticated users only)
- Click markers to view pin details

#### Pin Management
- Create pins with description and optional image upload
- Choose from default images (Pexels/Unsplash) or upload your own
- View pin details: image, description, username, timestamp, coordinates
- Rate limiting: 4-5 pins per 30 minutes per user
- External image URLs supported for default images

#### Leaderboard
- Weekly leaderboard (pins from last 7 days)
- All-time leaderboard (total pins)
- Pagination (20 entries per page)
- Click username to view user's pins
- Responsive table design

## Prerequisites

Before running this application, ensure you have:

### For Backend Development
- **Java 17 or higher** ([Download](https://adoptium.net/))
- **Maven 3.6+** ([Download](https://maven.apache.org/download.cgi))
- **MySQL 8.0+** (local) or Railway MySQL account

### For Frontend Development
- **Node.js 16+** ([Download](https://nodejs.org/))
- **npm** (comes with Node.js)

### Verification
Check if you have the prerequisites installed:

```bash
# Check Java
java -version

# Check Maven
mvn -version

# Check Node.js
node --version

# Check npm
npm --version
```

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd CSCI201_Final_Project
```

### 2. Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Configure database connection
# Edit src/main/resources/application.properties
# Update the database URL, username, and password

# Build the project
mvn clean install

# Run the backend server
mvn spring-boot:run
```

The backend will start on **http://localhost:8080**

See [backend/README.md](backend/README.md) for detailed backend setup instructions.

### 3. Set Up Frontend

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Edit .env and set VITE_API_BASE_URL=http://localhost:8080

# Run the development server
npm run dev
```

The frontend will start on **http://localhost:5173**

### 4. Test the Application

1. Open your browser to http://localhost:5173
2. Click "Sign Up" and create an account with a @usc.edu email
3. Log in with your credentials
4. Click on the map to drop a pin
5. View the leaderboard to see your rank
6. Try viewing other users' pins

## Project Structure

```
CSCI201_Final_Project/
├── backend/                      # Spring Boot backend
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/usc/squirrelspotter/
│   │   │   │   ├── SquirrelSpotterApplication.java
│   │   │   │   ├── config/       # Security & CORS configuration
│   │   │   │   ├── controller/   # REST API endpoints
│   │   │   │   ├── service/      # Business logic
│   │   │   │   ├── repository/   # Database access
│   │   │   │   ├── model/        # JPA entities
│   │   │   │   ├── security/     # JWT authentication
│   │   │   │   ├── dto/          # Data transfer objects
│   │   │   │   └── exception/    # Custom exceptions
│   │   │   └── resources/
│   │   │       ├── application.properties  # Configuration
│   │   │       └── schema.sql             # Database schema
│   │   └── test/                 # Unit tests
│   ├── pom.xml                   # Maven dependencies
│   └── README.md                 # Backend documentation
│
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── api/                  # API client functions
│   │   ├── components/           # React components
│   │   ├── hooks/                # Custom React hooks
│   │   ├── routes/               # Page components
│   │   ├── types/                # TypeScript types
│   │   ├── utils/                # Utility functions
│   │   ├── App.tsx               # Main app with routing
│   │   └── main.tsx              # Entry point
│   ├── package.json              # npm dependencies
│   └── vite.config.ts            # Vite configuration
│
├── tests/                        # Test suites
│   ├── account_creation_tests/   # Authentication tests
│   ├── leaderboard_tests/        # SQL test files
│   └── pin_tests/                # Pin operation tests
│
└── README.md                     # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user (requires @usc.edu email)
- `POST /api/auth/login` - Login and get JWT token

### Pins (Requires Authentication)
- `GET /api/pins/weekly` - Get pins from last 7 days
- `GET /api/pins/my` - Get current user's pins
- `POST /api/pins` - Create new pin (multipart/form-data or JSON with `image_url`)
  - Supports file uploads (saved to `/uploads/` directory)
  - Supports external image URLs (for default images from Pexels/Unsplash)
- `GET /api/pins/:pinID` - Get pin by ID

### Leaderboard
- `GET /api/leaderboard?type={weekly|all-time}&page={page}&pageSize={size}` - Get leaderboard
- `GET /api/users/:userID/pins` - Get pins by specific user

### WebSocket
- `wss://<API_BASE_URL>/ws/pins` - Real-time pin updates (secure WebSocket in production)
- Automatically uses `wss://` (secure) for HTTPS backends, `ws://` for local development

For detailed API documentation, see [backend/README.md](backend/README.md).

## Testing

### Backend Tests

Run authentication tests:

```bash
# Terminal 1: Start backend
cd backend
mvn spring-boot:run

# Terminal 2: Run tests
cd tests/account_creation_tests
python run_tests.py
```

### Manual Testing with cURL

```bash
# Test signup
curl -X POST http://localhost:8080/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@usc.edu","username":"testuser","password":"password123"}'

# Test login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@usc.edu","password":"password123"}'
```

## Deployment

### Deploy Backend to Railway

1. Create account at [Railway](https://railway.app/)
2. Create new project and add MySQL database
3. Note the database credentials
4. Deploy backend:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

5. Set environment variables in Railway dashboard:
   - `DATABASE_URL`
   - `DATABASE_USERNAME`
   - `DATABASE_PASSWORD`
   - `JWT_SECRET`

6. Note your backend URL: `https://your-backend.railway.app`

### Deploy Frontend to Vercel

1. Create account at [Vercel](https://vercel.com/)
2. Connect your GitHub repository
3. Set environment variable:
   - `VITE_API_BASE_URL=https://your-backend.railway.app`
4. Deploy!
5. Your app will be available at `https://your-app.vercel.app`

**Important:** Update the demo link at the top of this README with your Vercel URL!

See [backend/RAILWAY_SETUP.md](backend/RAILWAY_SETUP.md) for detailed deployment instructions.

## Environment Variables

### Backend (.env or Railway environment variables)

```env
DATABASE_URL=jdbc:mysql://host:port/database
DATABASE_USERNAME=root
DATABASE_PASSWORD=your_password
JWT_SECRET=your-256-bit-secret-key
IMAGE_STORAGE_PATH=./uploads/
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8080  # or your Railway URL
```

## Security Features

- **Password Security:** Argon2 hashing algorithm (OWASP recommended)
- **Authentication:** JWT tokens with 24-hour expiration
- **Email Validation:** Only @usc.edu emails allowed
- **CORS:** Configured to allow only trusted origins
- **Rate Limiting:** Pin creation limited to prevent spam
- **Input Validation:** Server-side validation on all endpoints

## Troubleshooting

### Backend won't start

**Error:** `Communications link failure` (MySQL)
- Verify MySQL is running
- Check database credentials in `application.properties`
- Ensure database exists

**Error:** `Port 8080 already in use`
- Kill the process: `lsof -ti:8080 | xargs kill -9` (Mac/Linux)
- Or change port in `application.properties`

### Frontend won't connect to backend

- Verify backend is running on the correct port
- Check `VITE_API_BASE_URL` in frontend `.env` file
- Check browser console for CORS errors
- Ensure CORS is configured in backend
- For production: Ensure WebSocket uses `wss://` (secure) protocol

### Image upload issues (403 Forbidden)

- **For uploaded files:** Railway's filesystem is ephemeral - files may be lost on redeploy
- **For default images:** External URLs (Pexels/Unsplash) are stored directly and work immediately
- **Solution:** Use default images for production, or implement cloud storage (S3, Cloudinary) for file uploads

### Authentication issues

- Clear localStorage and try logging in again
- Check JWT token expiration (24 hours by default)
- Verify email is @usc.edu format

### Database issues

- Verify schema is initialized: `mvn spring-boot:run` creates tables automatically
- Check MySQL logs for errors
- Ensure user has proper permissions

## Recent Updates

### Image Handling
- ✅ Added support for external image URLs (default images from Pexels/Unsplash)
- ✅ File uploads still supported for custom images
- ✅ External URLs stored directly in database (no file system dependency)

### WebSocket Configuration
- ✅ Automatic secure WebSocket (`wss://`) for production HTTPS backends
- ✅ Falls back to `ws://` for local development
- ✅ Real-time pin updates working in production

### Deployment
- ✅ Backend deployed on Railway with MySQL database
- ✅ Frontend deployed on Vercel with automatic builds
- ✅ Environment variables configured for production

## Development Workflow

1. **Start Backend:** `cd backend && mvn spring-boot:run`
2. **Start Frontend:** `cd frontend && npm run dev`
3. **Make Changes:** Edit code in respective directories
4. **Test Locally:** Access app at http://localhost:5173
5. **Run Tests:** Execute test suites in `tests/` directory
6. **Commit:** `git add . && git commit -m "description"`
7. **Deploy:** Push to Railway (backend) and Vercel (frontend)

## Contributing

This is a course project for CSCI 201 at USC. Contributions are welcome from team members.

### Development Guidelines
- Follow existing code structure and naming conventions
- Write clear commit messages
- Test your changes before committing
- Update documentation when adding features
- Keep sensitive data (passwords, secrets) in environment variables

## Documentation

- [Backend Documentation](backend/README.md) - Detailed backend setup and API docs
- [Railway Deployment Guide](backend/RAILWAY_SETUP.md) - How to deploy to Railway
- [Test Documentation](tests/RUN_TESTS.md) - How to run tests

## License

This project is for educational purposes as part of CSCI 201 coursework at USC.

## Contact

For questions or issues, please contact your team members or course instructor.

---

**Made with ❤️ by USC Students | Fight On! ✌️**
