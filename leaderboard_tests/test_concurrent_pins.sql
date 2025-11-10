-- ============================================
-- USC Pin Mapping Application
-- File: 06_test_concurrent_pin_submissions.sql
-- Test: Concurrent Pin Submissions - No Cross Contamination (ACID)
-- ============================================

USE usc_pin_test;

-- Setup: Create two users
INSERT INTO Users (email, password) VALUES 
    ('concurrent1@usc.edu', 'hashed_pass1'),
    ('concurrent2@usc.edu', 'hashed_pass2');

SET @user1_id = (SELECT UserID FROM Users WHERE email = 'concurrent1@usc.edu');
SET @user2_id = (SELECT UserID FROM Users WHERE email = 'concurrent2@usc.edu');

-- Initialize with existing pins
INSERT INTO Pins (UserID, lat, lng, description) VALUES 
    (@user1_id, 34.0224, -118.2851, 'User1 initial'),
    (@user2_id, 34.0225, -118.2852, 'User2 initial');

INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) VALUES 
    (@user1_id, 1, 1),
    (@user2_id, 1, 1);

-- Query BEFORE concurrent operations
SELECT 
    'BEFORE CONCURRENT OPS' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
WHERE UserID IN (@user1_id, @user2_id)
ORDER BY UserID;

-- Expected Output:
-- test_phase            | UserID | total_pins | weekly_pins
-- BEFORE CONCURRENT OPS | 1      | 1          | 1
-- BEFORE CONCURRENT OPS | 2      | 1          | 1

-- Simulate concurrent pin creation
-- Transaction 1: User 1 creates pin
START TRANSACTION;
INSERT INTO Pins (UserID, lat, lng, description) 
VALUES (@user1_id, 34.0227, -118.2854, 'User1 concurrent pin');
UPDATE Leaderboard 
SET total_pins = total_pins + 1, weekly_pins = weekly_pins + 1 
WHERE UserID = @user1_id;
COMMIT;

-- Transaction 2: User 2 creates pin (immediately after)
START TRANSACTION;
INSERT INTO Pins (UserID, lat, lng, description) 
VALUES (@user2_id, 34.0228, -118.2855, 'User2 concurrent pin');
UPDATE Leaderboard 
SET total_pins = total_pins + 1, weekly_pins = weekly_pins + 1 
WHERE UserID = @user2_id;
COMMIT;

-- Query AFTER concurrent operations
SELECT 
    'AFTER CONCURRENT OPS' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
WHERE UserID IN (@user1_id, @user2_id)
ORDER BY UserID;

-- Expected Output:
-- test_phase           | UserID | total_pins | weekly_pins
-- AFTER CONCURRENT OPS | 1      | 2          | 2
-- AFTER CONCURRENT OPS | 2      | 2          | 2

-- Validation: Check for cross-contamination
SELECT 
    l.UserID,
    u.email,
    l.total_pins,
    l.weekly_pins,
    COUNT(p.PinID) AS actual_pins,
    CASE 
        WHEN l.total_pins = COUNT(p.PinID) AND l.total_pins = 2
        THEN 'PASS: No cross-contamination' 
        ELSE 'FAIL: Cross-contamination detected' 
    END AS test_result
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
JOIN Pins p ON l.UserID = p.UserID
WHERE l.UserID IN (@user1_id, @user2_id)
GROUP BY l.UserID, u.email, l.total_pins, l.weekly_pins;