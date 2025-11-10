-- ============================================
-- USC Pin Mapping Application - Test Setup
-- File: 00_setup_test_environment.sql
-- Purpose: Create test database and tables
-- ============================================

-- Create test database
CREATE DATABASE IF NOT EXISTS usc_pin_test;
USE usc_pin_test;

-- Create Users table
CREATE TABLE IF NOT EXISTS Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Pins table
CREATE TABLE IF NOT EXISTS Pins (
    PinID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    lat FLOAT NOT NULL,
    lng FLOAT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    image_url VARCHAR(200),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Create Leaderboard table
CREATE TABLE IF NOT EXISTS Leaderboard (
    UserID INT PRIMARY KEY,
    total_pins INT DEFAULT 0,
    weekly_pins INT DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX idx_pins_userid ON Pins(UserID);
CREATE INDEX idx_pins_created_at ON Pins(created_at);
CREATE INDEX idx_leaderboard_total ON Leaderboard(total_pins DESC);
CREATE INDEX idx_leaderboard_weekly ON Leaderboard(weekly_pins DESC);

-- Verify table creation
SELECT 'Tables created successfully' AS status;
SHOW TABLES;