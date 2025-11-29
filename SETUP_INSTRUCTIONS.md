# Setup Instructions - Install Prerequisites

## You Need to Install These First!

Your system is currently **missing the required development tools** to run the Squirrel Spotter application. Follow these instructions to install everything you need.

## Current Status

✅ Python 3.13 - Installed
❌ Java 17+ - **NOT INSTALLED**
❌ Maven - **NOT INSTALLED**
❌ Node.js & npm - **NOT INSTALLED**

## Installation Guide for Windows

### 1. Install Java 17

#### Option A: Using Adoptium (Recommended)

1. Go to https://adoptium.net/
2. Click **Download** for Java 17 (LTS)
3. Select:
   - **Operating System:** Windows
   - **Architecture:** x64 (or ARM if you have ARM processor)
   - **Package Type:** JDK
4. Download the `.msi` installer
5. Run the installer
6. **IMPORTANT:** Check "Add to PATH" during installation
7. Click through the installer with default settings

#### Option B: Using Oracle JDK

1. Go to https://www.oracle.com/java/technologies/downloads/#java17
2. Download **Windows x64 Installer**
3. Run the installer
4. Follow default installation steps

#### Verify Java Installation

Open a **NEW** Command Prompt or PowerShell window and run:

```bash
java -version
```

Expected output:
```
openjdk version "17.0.9" 2023-10-17
OpenJDK Runtime Environment Temurin-17.0.9+9 (build 17.0.9+9)
```

If you see "command not found", you need to add Java to your PATH:

1. Search for "Environment Variables" in Windows Start menu
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Under "System variables", find "Path" and click "Edit"
5. Click "New" and add: `C:\Program Files\Java\jdk-17\bin` (adjust path if different)
6. Click OK on all dialogs
7. **Close and reopen** your terminal

### 2. Install Maven

#### Using Maven Installer

1. Go to https://maven.apache.org/download.cgi
2. Download **Binary zip archive** (apache-maven-3.x.x-bin.zip)
3. Extract the zip file to `C:\Program Files\Apache\Maven`
4. Add Maven to PATH:
   - Search for "Environment Variables" in Start menu
   - Click "Edit the system environment variables"
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\Program Files\Apache\Maven\bin`
   - Click OK on all dialogs

#### Using Chocolatey (Alternative)

If you have Chocolatey package manager:

```bash
choco install maven
```

#### Verify Maven Installation

Open a **NEW** terminal and run:

```bash
mvn -version
```

Expected output:
```
Apache Maven 3.9.5 (...)
Maven home: C:\Program Files\Apache\Maven
Java version: 17.0.9, vendor: Eclipse Adoptium
```

### 3. Install Node.js and npm

#### Using Official Installer (Recommended)

1. Go to https://nodejs.org/
2. Download **LTS version** (currently Node.js 20.x)
3. Run the `.msi` installer
4. **IMPORTANT:** Check the box "Automatically install necessary tools" during installation
5. Follow the installer with default settings
6. This will install both Node.js and npm

#### Verify Node.js Installation

Open a **NEW** terminal and run:

```bash
node --version
```

Expected output:
```
v20.10.0
```

#### Verify npm Installation

```bash
npm --version
```

Expected output:
```
10.2.5
```

### 4. Verify All Prerequisites

Once everything is installed, verify with:

```bash
java -version
mvn -version
node --version
npm --version
```

All four commands should work without errors.

## Installation Guide for macOS

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Java 17

```bash
brew install openjdk@17
```

Add Java to PATH by adding this to your `~/.zshrc` or `~/.bash_profile`:

```bash
export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"
```

Then reload:

```bash
source ~/.zshrc  # or source ~/.bash_profile
```

Verify:

```bash
java -version
```

### 3. Install Maven

```bash
brew install maven
```

Verify:

```bash
mvn -version
```

### 4. Install Node.js and npm

```bash
brew install node
```

Verify:

```bash
node --version
npm --version
```

## Installation Guide for Linux (Ubuntu/Debian)

### 1. Install Java 17

```bash
sudo apt update
sudo apt install openjdk-17-jdk
```

Verify:

```bash
java -version
```

### 2. Install Maven

```bash
sudo apt install maven
```

Verify:

```bash
mvn -version
```

### 3. Install Node.js and npm

```bash
# Using NodeSource repository for latest version
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

Verify:

```bash
node --version
npm --version
```

## After Installation - Run the Application

Once you have all prerequisites installed, follow these steps:

### 1. Start the Backend

```bash
# Open terminal in project directory
cd C:\Users\Ara\CSCI201_Final_Project\backend

# Build the project
mvn clean install

# Run the backend
mvn spring-boot:run
```

**Wait for:** `Started SquirrelSpotterApplication in X.XXX seconds`

The backend will be running on http://localhost:8080

### 2. Start the Frontend

Open a **NEW terminal** window:

```bash
# Navigate to frontend directory
cd C:\Users\Ara\CSCI201_Final_Project\frontend

# Install dependencies (first time only)
npm install

# Create environment file
copy .env.example .env

# Start the development server
npm run dev
```

The frontend will be running on http://localhost:5173

### 3. Test the Application

1. Open your browser to http://localhost:5173
2. Click "Sign Up" and create an account with @usc.edu email
3. Log in and start dropping pins!

### 4. Run Tests

Open a **THIRD terminal** window:

```bash
cd C:\Users\Ara\CSCI201_Final_Project\tests\account_creation_tests
python run_tests.py
```

All 13 tests should pass!

## Troubleshooting

### "command not found" errors

- **Solution:** Make sure you've added the tools to your PATH
- **Windows:** Edit Environment Variables as described above
- **Mac/Linux:** Add to `~/.zshrc` or `~/.bash_profile`
- **Important:** Close and reopen your terminal after changing PATH

### Java version conflict

If you have multiple Java versions:

**Windows:**
```bash
# Set JAVA_HOME
setx JAVA_HOME "C:\Program Files\Java\jdk-17"
```

**Mac/Linux:**
Add to `~/.zshrc`:
```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
```

### Maven can't find Java

Make sure `JAVA_HOME` environment variable is set:

**Windows:**
1. Environment Variables → System variables → New
2. Variable name: `JAVA_HOME`
3. Variable value: `C:\Program Files\Java\jdk-17` (your Java path)

**Mac/Linux:**
Add to `~/.zshrc`:
```bash
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home
```

### Port 8080 already in use

```bash
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8080 | xargs kill -9
```

## Need Help?

- Java installation: https://adoptium.net/installation/
- Maven installation: https://maven.apache.org/install.html
- Node.js installation: https://nodejs.org/en/download/package-manager/

---

**Once installed, see [README.md](README.md) for full application documentation!**
