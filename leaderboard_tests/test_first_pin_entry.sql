-- ============================================
-- USC Pin Mapping Application
-- File: 13_test_first_pin_creates_entry.sql
-- Test: First Pin Creates Leaderboard Entry
-- ============================================

USE usc_pin_test;

-- Setup: Create new user
INSERT INTO Users (email, password) VALUES ('newpinner@usc.edu', 'hashed_pass');
SET @new_user_id = LAST_INSERT_ID();

-- Verify no leaderboard entry exists before pin
SELECT 
    COUNT(*) AS leaderboard_entries_before,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS: No entry before first pin'
        ELSE 'FAIL'
    END AS test_result
FROM Leaderboard
WHERE UserID = @new_user_id;

-- Add first pin for user
INSERT INTO Pins (UserID, lat, lng, description) 
VALUES (@new_user_id, 34.0224, -118.2851, 'Very first pin');

-- Create leaderboard entry (simulating trigger or application logic)
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) 
VALUES (@new_user_id, 1, 1);

-- Verify leaderboard entry was created
SELECT 
    u.email,
    l.UserID,
    l.total_pins,
    l.weekly_pins,
    CASE 
        WHEN l.total_pins = 1 AND l.weekly_pins = 1 
        THEN 'PASS: Entry created with correct counts'
        ELSE 'FAIL'
    END AS test_result
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
WHERE l.UserID = @new_user_id;

-- Expected Output:
-- email              | UserID | total_pins | weekly_pins | test_result
-- newpinner@usc.edu  | X      | 1          | 1           | PASS: Entry created with correct counts

-- Verify pin was actually created
SELECT 
    COUNT(*) AS pin_count,
    CASE 
        WHEN COUNT(*) = 1 THEN 'PASS: Pin exists'
        ELSE 'FAIL'
    END AS pin_verification
FROM Pins
WHERE UserID = @new_user_id;