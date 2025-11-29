# Railway Deployment Guide

## MySQL Configuration

Your Railway MySQL instance details:
- **Public Host:** `trolley.proxy.rlwy.net`
- **Public Port:** `45740`
- **Private Host:** `mysql.railway.internal` (use when backend is also on Railway)

## Step 1: Get MySQL Credentials

1. Go to your Railway MySQL service dashboard
2. Click on **Variables** tab
3. Note these values:
   - `MYSQL_ROOT_PASSWORD` - Your MySQL password
   - `MYSQL_DATABASE` - Usually "railway"
   - Or use `MYSQLDATABASE`, `MYSQLUSER`, `MYSQLPASSWORD` if available

## Step 2: Test Locally with Railway MySQL

Update your **local** `application.properties` for testing:

```properties
# Connect to Railway MySQL from local machine
spring.datasource.url=jdbc:mysql://trolley.proxy.rlwy.net:45740/railway?useSSL=true&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=YOUR_MYSQL_ROOT_PASSWORD_FROM_RAILWAY
```

Replace `YOUR_MYSQL_ROOT_PASSWORD_FROM_RAILWAY` with the actual password from Railway Variables tab.

Then test locally:
```bash
cd backend
mvn clean install
mvn spring-boot:run
```

Try signup: `http://localhost:8080/api/auth/signup`

## Step 3: Deploy Backend to Railway

### Option A: Railway CLI (Recommended)

1. **Install Railway CLI:**
   ```bash
   # Mac/Linux
   bash <(curl -fsSL cli.new)

   # Or with npm
   npm i -g @railway/cli
   ```

2. **Login and link project:**
   ```bash
   railway login
   cd backend
   railway link
   ```

3. **Set environment variables in Railway:**
   ```bash
   # Use private networking (when both backend and MySQL are on Railway)
   railway variables set DATABASE_URL="jdbc:mysql://mysql.railway.internal:3306/railway?useSSL=false"
   railway variables set DATABASE_USERNAME="root"
   railway variables set DATABASE_PASSWORD="YOUR_MYSQL_ROOT_PASSWORD"
   railway variables set JWT_SECRET="your-very-long-random-secret-key-minimum-256-bits"
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

### Option B: GitHub Integration

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Add backend with authentication"
   git push
   ```

2. **Connect Railway to GitHub:**
   - In Railway dashboard, click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Spring Boot

3. **Set environment variables in Railway dashboard:**
   - Go to your backend service
   - Click **Variables** tab
   - Add these variables:

   **For production (private networking):**
   ```
   DATABASE_URL=jdbc:mysql://mysql.railway.internal:3306/railway?useSSL=false
   DATABASE_USERNAME=root
   DATABASE_PASSWORD=<from MySQL service variables>
   JWT_SECRET=<generate a long random string>
   ```

   **Alternative (public networking):**
   ```
   DATABASE_URL=jdbc:mysql://trolley.proxy.rlwy.net:45740/railway?useSSL=true
   DATABASE_USERNAME=root
   DATABASE_PASSWORD=<from MySQL service variables>
   JWT_SECRET=<generate a long random string>
   ```

## Step 4: Initialize Database Schema

### Option 1: Automatic (JPA will create tables)
The backend is configured with `spring.jpa.hibernate.ddl-auto=update`, so tables will be created automatically on first run.

### Option 2: Manual (Run SQL script)

Connect to Railway MySQL and run the schema:

```bash
# Using Railway CLI
railway connect mysql

# Then paste the contents of src/main/resources/schema.sql
```

Or use a MySQL client like MySQL Workbench:
- Host: `trolley.proxy.rlwy.net`
- Port: `45740`
- Username: `root`
- Password: (from Railway Variables)
- Database: `railway`

## Step 5: Test Deployed Backend

Once deployed, Railway will give you a URL like: `https://your-backend.up.railway.app`

Test signup:
```bash
curl -X POST https://your-backend.up.railway.app/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@usc.edu","username":"testuser","password":"password123"}'
```

## Step 6: Update Frontend

Update `frontend/.env`:
```env
VITE_API_BASE_URL=https://your-backend.up.railway.app
```

## Environment Variables Summary

**Required variables for Railway backend:**

| Variable | Example Value | Where to Get |
|----------|---------------|--------------|
| `DATABASE_URL` | `jdbc:mysql://mysql.railway.internal:3306/railway` | Use private host when on Railway |
| `DATABASE_USERNAME` | `root` | From MySQL service Variables tab |
| `DATABASE_PASSWORD` | `abc123xyz` | From MySQL service Variables tab (MYSQL_ROOT_PASSWORD) |
| `JWT_SECRET` | `a-very-long-random-string-minimum-256-bits` | Generate a secure random string |

**Optional:**
| Variable | Default | Purpose |
|----------|---------|---------|
| `IMAGE_STORAGE_PATH` | `./uploads/` | For Pin/Maps team (image storage) |

## Troubleshooting

### Connection Refused
If you see "Connection refused" errors:
- ✅ Check that MySQL service is running on Railway
- ✅ Verify `DATABASE_URL` uses correct host (private: `mysql.railway.internal` or public: `trolley.proxy.rlwy.net:45740`)
- ✅ Check username and password match Railway MySQL Variables

### Unknown Database 'railway'
If database doesn't exist:
```bash
railway connect mysql
CREATE DATABASE railway;
EXIT;
```

### SSL Errors
Try both:
- `useSSL=true` (for public networking)
- `useSSL=false` (for private networking)

### Tables Not Created
Check logs in Railway dashboard:
```bash
railway logs
```

If needed, manually run `schema.sql` in Railway MySQL.

## Railway Networking: Public vs Private

**Private Networking (Recommended when both on Railway):**
- URL: `mysql.railway.internal:3306`
- Faster, more secure
- Only works when backend is also deployed to Railway
- Use `useSSL=false`

**Public Networking (For local testing):**
- URL: `trolley.proxy.rlwy.net:45740`
- Accessible from anywhere (including your local machine)
- Use `useSSL=true`

## Next Steps

1. ✅ Deploy backend to Railway
2. ✅ Test authentication endpoints
3. ✅ Update frontend `.env` with Railway backend URL
4. 🚀 Deploy frontend to Vercel
5. 🎉 Full stack deployed!

## Helpful Railway Commands

```bash
# View logs
railway logs

# Connect to MySQL shell
railway connect mysql

# Open service in browser
railway open

# View environment variables
railway variables

# Set a variable
railway variables set KEY=value
```

Good luck! 🐿️
