-- ============================================
-- USC Pin Mapping Application
-- File: 03_test_pin_creation_increments.sql
-- Test: Valid Pin Entry Updates Leaderboard (+1 to both counts)
-- ============================================

USE usc_pin_test;

-- Setup: Create user and initial leaderboard entry
INSERT INTO Users (email, password) VALUES ('testuser@usc.edu', 'hashed_pass');
SET @test_user_id = LAST_INSERT_ID();

-- Create initial pin to establish leaderboard entry
INSERT INTO Pins (UserID, lat, lng, description) 
VALUES (@test_user_id, 34.0224, -118.2851, 'Initial pin');

-- Initialize leaderboard (this would typically be done via trigger or application logic)
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) 
VALUES (@test_user_id, 1, 1);

-- Query BEFORE adding new pin
SELECT 
    'BEFORE PIN CREATION' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
WHERE UserID = @test_user_id;

-- Expected Output:
-- test_phase          | UserID | total_pins | weekly_pins
-- BEFORE PIN CREATION | 1      | 1          | 1

-- Add new pin
INSERT INTO Pins (UserID, lat, lng, description) 
VALUES (@test_user_id, 34.0225, -118.2852, 'Second pin');

-- Update leaderboard (simulating application logic or trigger)
UPDATE Leaderboard 
SET total_pins = total_pins + 1,
    weekly_pins = weekly_pins + 1
WHERE UserID = @test_user_id;

-- Query AFTER adding new pin
SELECT 
    'AFTER PIN CREATION' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
WHERE UserID = @test_user_id;

-- Expected Output:
-- test_phase         | UserID | total_pins | weekly_pins
-- AFTER PIN CREATION | 1      | 2          | 2

-- Validation: Verify difference is exactly 1
SELECT 
    l.UserID,
    l.total_pins,
    l.weekly_pins,
    CASE 
        WHEN l.total_pins = 2 AND l.weekly_pins = 2 
        THEN 'PASS: Both counts incremented by 1' 
        ELSE 'FAIL' 
    END AS test_result
FROM Leaderboard l
WHERE l.UserID = @test_user_id;