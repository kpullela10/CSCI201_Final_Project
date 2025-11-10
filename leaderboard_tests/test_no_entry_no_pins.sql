-- ============================================
-- USC Pin Mapping Application
-- File: 14_test_no_entry_without_pins.sql
-- Test: New User Account with No Pins, No Leaderboard Entry
-- ============================================

USE usc_pin_test;

-- Setup: Create new user account
INSERT INTO Users (email, password) VALUES ('justregistered@usc.edu', 'hashed_pass');
SET @just_registered = LAST_INSERT_ID();

-- Verify user exists in Users table
SELECT 
    UserID,
    email,
    'User registered successfully' AS status
FROM Users
WHERE UserID = @just_registered;

-- Verify NO leaderboard entry exists
SELECT 
    COUNT(*) AS leaderboard_entries,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS: No leaderboard entry for user without pins'
        ELSE 'FAIL: Leaderboard entry should not exist'
    END AS test_result
FROM Leaderboard
WHERE UserID = @just_registered;

-- Expected Output:
-- leaderboard_entries | test_result
-- 0                   | PASS: No leaderboard entry for user without pins

-- Verify no pins exist for this user
SELECT 
    COUNT(*) AS pin_count,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS: No pins for new user'
        ELSE 'FAIL'
    END AS pin_verification
FROM Pins
WHERE UserID = @just_registered;

-- Comprehensive validation
SELECT 
    u.UserID,
    u.email,
    COALESCE(l.total_pins, 0) AS total_pins,
    COALESCE(l.weekly_pins, 0) AS weekly_pins,
    COUNT(p.PinID) AS actual_pin_count,
    CASE 
        WHEN l.UserID IS NULL AND COUNT(p.PinID) = 0 
        THEN 'PASS: User exists but no leaderboard entry and no pins'
        ELSE 'FAIL'
    END AS overall_test_result
FROM Users u
LEFT JOIN Leaderboard l ON u.UserID = l.UserID
LEFT JOIN Pins p ON u.UserID = p.UserID
WHERE u.UserID = @just_registered
GROUP BY u.UserID, u.email, l.total_pins, l.weekly_pins, l.UserID;