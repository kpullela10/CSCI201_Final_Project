-- ============================================
-- USC Pin Mapping Application
-- File: 05_test_delete_old_pin.sql
-- Test: Delete Old Pin (Not This Week) - Only Total Decrements
-- ============================================

USE usc_pin_test;

-- Setup: Create user with pins from different weeks
INSERT INTO Users (email, password) VALUES ('oldpin@usc.edu', 'hashed_pass');
SET @old_pin_user_id = LAST_INSERT_ID();

-- Create an old pin (3 weeks ago) and current pins
INSERT INTO Pins (UserID, lat, lng, description, created_at) VALUES 
    (@old_pin_user_id, 34.0224, -118.2851, 'Old pin', DATE_SUB(NOW(), INTERVAL 21 DAY)),
    (@old_pin_user_id, 34.0225, -118.2852, 'Recent pin 1', NOW()),
    (@old_pin_user_id, 34.0226, -118.2853, 'Recent pin 2', NOW());

-- Initialize leaderboard (1 old pin + 2 current week pins = 3 total, 2 weekly)
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) 
VALUES (@old_pin_user_id, 3, 2);

-- Query BEFORE deletion
SELECT 
    'BEFORE DELETION' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
WHERE UserID = @old_pin_user_id;

-- Expected Output:
-- test_phase      | UserID | total_pins | weekly_pins
-- BEFORE DELETION | 1      | 3          | 2

-- Get the old pin ID (created more than 7 days ago)
SET @old_pin_id = (
    SELECT PinID 
    FROM Pins 
    WHERE UserID = @old_pin_user_id 
    AND created_at < DATE_SUB(NOW(), INTERVAL 7 DAY)
    LIMIT 1
);

-- Verify we're deleting an old pin
SELECT 
    PinID,
    created_at,
    DATEDIFF(NOW(), created_at) AS days_old,
    CASE 
        WHEN DATEDIFF(NOW(), created_at) > 7 
        THEN 'OLD PIN (>7 days)' 
        ELSE 'CURRENT WEEK PIN' 
    END AS pin_age
FROM Pins
WHERE PinID = @old_pin_id;

-- Delete the old pin
DELETE FROM Pins WHERE PinID = @old_pin_id;

-- Update leaderboard (only total_pins decrements for old pins)
UPDATE Leaderboard 
SET total_pins = total_pins - 1
    -- weekly_pins stays the same because pin was not from this week
WHERE UserID = @old_pin_user_id;

-- Query AFTER deletion
SELECT 
    'AFTER DELETION' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
WHERE UserID = @old_pin_user_id;

-- Expected Output:
-- test_phase     | UserID | total_pins | weekly_pins
-- AFTER DELETION | 1      | 2          | 2

-- Validation query
SELECT 
    UserID,
    total_pins,
    weekly_pins,
    CASE 
        WHEN total_pins = 2 AND weekly_pins = 2 
        THEN 'PASS: Only total_pins decremented' 
        ELSE 'FAIL' 
    END AS test_result
FROM Leaderboard
WHERE UserID = @old_pin_user_id;