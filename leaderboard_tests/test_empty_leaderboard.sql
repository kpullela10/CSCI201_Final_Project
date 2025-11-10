-- ============================================
-- USC Pin Mapping Application
-- File: 07_test_empty_leaderboard_one_entry.sql
-- Test: Empty Leaderboard, Add One Pin, Verify One Entry
-- ============================================

USE usc_pin_test;

-- Ensure clean state
DELETE FROM Pins;
DELETE FROM Leaderboard;
DELETE FROM Users;

-- Verify leaderboard is empty
SELECT 
    COUNT(*) AS leaderboard_count,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS: Leaderboard empty'
        ELSE 'FAIL'
    END AS test_result
FROM Leaderboard;

-- Register first user
INSERT INTO Users (email, password) VALUES ('firstuser@usc.edu', 'hashed_pass');
SET @first_user = LAST_INSERT_ID();

-- Verify no leaderboard entry yet
SELECT 
    COUNT(*) AS entries_before,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS: No leaderboard entry before pin'
        ELSE 'FAIL'
    END AS test_result
FROM Leaderboard 
WHERE UserID = @first_user;

-- Add first pin
INSERT INTO Pins (UserID, lat, lng, description) 
VALUES (@first_user, 34.0224, -118.2851, 'First pin ever');

-- Create leaderboard entry
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) 
VALUES (@first_user, 1, 1);

-- Query leaderboard
SELECT 
    l.UserID,
    u.email,
    l.total_pins,
    l.weekly_pins
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID;

-- Expected Output:
-- UserID | email              | total_pins | weekly_pins
-- 1      | firstuser@usc.edu  | 1          | 1

-- Validation
SELECT 
    COUNT(*) AS total_entries,
    CASE 
        WHEN COUNT(*) = 1 THEN 'PASS: Exactly one entry' 
        ELSE 'FAIL' 
    END AS test_result
FROM Leaderboard;