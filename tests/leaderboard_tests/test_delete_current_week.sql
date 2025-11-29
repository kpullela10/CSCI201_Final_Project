-- ============================================
-- USC Pin Mapping Application
-- File: 04_test_delete_current_week_pin.sql
-- Test: Valid Pin Deletion (This Week) - Decrement Both Counts
-- ============================================

USE usc_pin_test;

-- Setup: Create user with multiple pins created this week
INSERT INTO Users (email, password) VALUES ('deletetest@usc.edu', 'hashed_pass');
SET @delete_user_id = LAST_INSERT_ID();

-- Create pins (all created this week)
INSERT INTO Pins (UserID, lat, lng, description, created_at) VALUES 
    (@delete_user_id, 34.0224, -118.2851, 'Pin 1', NOW()),
    (@delete_user_id, 34.0225, -118.2852, 'Pin 2', NOW()),
    (@delete_user_id, 34.0226, -118.2853, 'Pin 3', NOW());

-- Initialize leaderboard
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) 
VALUES (@delete_user_id, 3, 3);

-- Query BEFORE deletion
SELECT 
    'BEFORE DELETION' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
WHERE UserID = @delete_user_id;

-- Expected Output:
-- test_phase      | UserID | total_pins | weekly_pins
-- BEFORE DELETION | 1      | 3          | 3

-- Get a pin ID to delete (created this week)
SET @pin_to_delete = (
    SELECT PinID 
    FROM Pins 
    WHERE UserID = @delete_user_id 
    LIMIT 1
);

-- Verify the pin is from this week
SELECT 
    PinID,
    created_at,
    CASE 
        WHEN created_at >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        THEN 'CURRENT WEEK PIN'
        ELSE 'OLD PIN'
    END AS pin_status
FROM Pins
WHERE PinID = @pin_to_delete;

-- Delete the pin
DELETE FROM Pins WHERE PinID = @pin_to_delete;

-- Update leaderboard (simulating application logic)
UPDATE Leaderboard 
SET total_pins = total_pins - 1,
    weekly_pins = weekly_pins - 1
WHERE UserID = @delete_user_id;

-- Query AFTER deletion
SELECT 
    'AFTER DELETION' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
WHERE UserID = @delete_user_id;

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
        THEN 'PASS: Both counts decremented by 1' 
        ELSE 'FAIL' 
    END AS test_result
FROM Leaderboard
WHERE UserID = @delete_user_id;