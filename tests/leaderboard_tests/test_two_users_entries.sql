-- ============================================
-- USC Pin Mapping Application
-- File: 08_test_two_users_two_entries.sql
-- Test: Two Users, Two Entries
-- ============================================

USE usc_pin_test;

-- Prerequisite: Run 07_test_empty_leaderboard_one_entry.sql first
-- or ensure first user exists from previous test

-- Add second user
INSERT INTO Users (email, password) VALUES ('seconduser@usc.edu', 'hashed_pass');
SET @second_user = LAST_INSERT_ID();

-- Add pin for second user
INSERT INTO Pins (UserID, lat, lng, description) 
VALUES (@second_user, 34.0225, -118.2852, 'Second user pin');

-- Create leaderboard entry for second user
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) 
VALUES (@second_user, 1, 1);

-- Query entire leaderboard
SELECT 
    l.UserID,
    u.email,
    l.total_pins,
    l.weekly_pins
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.UserID;

-- Expected Output:
-- UserID | email               | total_pins | weekly_pins
-- 1      | firstuser@usc.edu   | 1          | 1
-- 2      | seconduser@usc.edu  | 1          | 1

-- Validation
SELECT 
    COUNT(*) AS total_entries,
    COUNT(DISTINCT UserID) AS unique_users,
    CASE 
        WHEN COUNT(*) = 2 AND COUNT(DISTINCT UserID) = 2 
        THEN 'PASS: Two distinct entries' 
        ELSE 'FAIL' 
    END AS test_result
FROM Leaderboard;