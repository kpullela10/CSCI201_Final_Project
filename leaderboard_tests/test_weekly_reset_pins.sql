-- ============================================
-- USC Pin Mapping Application
-- File: 02_test_weekly_reset_no_data_loss.sql
-- Test: Weekly Reset Doesn't Affect Pins Table
-- ============================================

USE usc_pin_test;

-- Setup: Create user and pins
INSERT INTO Users (email, password) VALUES ('resettest@usc.edu', 'hashed_pass');
SET @user_id = LAST_INSERT_ID();

INSERT INTO Pins (UserID, lat, lng, description) VALUES 
    (@user_id, 34.0224, -118.2851, 'Pin 1'),
    (@user_id, 34.0225, -118.2852, 'Pin 2'),
    (@user_id, 34.0226, -118.2853, 'Pin 3');

INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) VALUES 
    (@user_id, 3, 3);

-- Count pins before reset
SELECT COUNT(*) AS pins_before_reset FROM Pins;

-- Execute weekly reset
UPDATE Leaderboard SET weekly_pins = 0;

-- Count pins after reset
SELECT COUNT(*) AS pins_after_reset FROM Pins;

-- Validation: Both counts should be identical
SELECT 
    (SELECT COUNT(*) FROM Pins) AS pins_count,
    (SELECT weekly_pins FROM Leaderboard WHERE UserID = @user_id) AS weekly_pins_after_reset,
    CASE 
        WHEN (SELECT COUNT(*) FROM Pins) = 3 
        AND (SELECT weekly_pins FROM Leaderboard WHERE UserID = @user_id) = 0
        THEN 'PASS: Pins table unchanged, weekly_pins reset'
        ELSE 'FAIL'
    END AS test_result;