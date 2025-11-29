-- Squirrel Spotter USC - Database Schema
-- This script creates all the tables needed for the application

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS pins;
DROP TABLE IF EXISTS users;

-- ============================================================
-- Users Table
-- ============================================================
-- Stores user account information with Argon2 hashed passwords
CREATE TABLE IF NOT EXISTS users (
    userID INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_email (email),
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Pins Table
-- ============================================================
-- Stores squirrel pin locations with metadata
CREATE TABLE IF NOT EXISTS pins (
    pinID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT NOT NULL,
    lat DECIMAL(10, 8) NOT NULL,
    lng DECIMAL(11, 8) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
    INDEX idx_created_at (created_at),
    INDEX idx_user_created (userID, created_at),
    INDEX idx_user (userID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- Leaderboard View (Computed from Pins)
-- ============================================================
-- NOTE: This is computed dynamically. No separate table needed.
-- The Leaderboard team can use this query pattern:
--
-- Weekly leaderboard:
-- SELECT
--     u.userID,
--     u.username,
--     COUNT(p.pinID) as weekly_pins,
--     (SELECT COUNT(*) FROM pins WHERE userID = u.userID) as total_pins
-- FROM users u
-- LEFT JOIN pins p ON u.userID = p.userID
--     AND p.created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
-- GROUP BY u.userID, u.username
-- ORDER BY weekly_pins DESC;
--
-- All-time leaderboard:
-- SELECT
--     u.userID,
--     u.username,
--     COUNT(p.pinID) as total_pins
-- FROM users u
-- LEFT JOIN pins p ON u.userID = p.userID
-- GROUP BY u.userID, u.username
-- ORDER BY total_pins DESC;

-- ============================================================
-- Sample Data (Optional - for testing)
-- ============================================================
-- Uncomment to insert sample data

-- INSERT INTO users (username, email, password_hash) VALUES
-- ('testuser', 'testuser@usc.edu', '$argon2id$v=19$m=65536,t=10,p=1$...');  -- Replace with actual hash

-- INSERT INTO pins (userID, lat, lng, description, image_url) VALUES
-- (1, 34.0224, -118.2851, 'Spotted near Tommy Trojan', 'https://example.com/squirrel1.jpg'),
-- (1, 34.0212, -118.2879, 'Cute squirrel by Doheny Library', 'https://example.com/squirrel2.jpg');
