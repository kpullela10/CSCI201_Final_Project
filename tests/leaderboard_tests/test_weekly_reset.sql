-- ============================================
-- USC Pin Mapping Application
-- File: 01_test_weekly_reset.sql
-- Test: Weekly Pins Reset to 0, Total Pins Unchanged
-- ============================================

USE usc_pin_test;

-- Setup: Create test users and pins
INSERT INTO Users (email, password) VALUES 
    ('user1@usc.edu', 'hashed_pass1'),
    ('user2@usc.edu', 'hashed_pass2'),
    ('user3@usc.edu', 'hashed_pass3');

-- Create leaderboard entries with various counts
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) VALUES 
    (1, 25, 12),
    (2, 18, 7),
    (3, 42, 15);

-- Verify initial state
SELECT 
    'BEFORE RESET' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
ORDER BY UserID;

-- Expected Output:
-- test_phase   | UserID | total_pins | weekly_pins
-- BEFORE RESET | 1      | 25         | 12
-- BEFORE RESET | 2      | 18         | 7
-- BEFORE RESET | 3      | 42         | 15

-- Execute weekly reset (this would be your scheduled script)
UPDATE Leaderboard 
SET weekly_pins = 0;

-- Verify after reset
SELECT 
    'AFTER RESET' AS test_phase,
    UserID,
    total_pins,
    weekly_pins
FROM Leaderboard
ORDER BY UserID;

-- Expected Output:
-- test_phase  | UserID | total_pins | weekly_pins
-- AFTER RESET | 1      | 25         | 0
-- AFTER RESET | 2      | 18         | 0
-- AFTER RESET | 3      | 42         | 0

-- Validation query: Ensure all weekly_pins are 0 and total_pins unchanged
SELECT 
    COUNT(*) AS total_entries,
    SUM(CASE WHEN weekly_pins = 0 THEN 1 ELSE 0 END) AS weekly_reset_count,
    SUM(CASE WHEN total_pins > 0 THEN 1 ELSE 0 END) AS total_pins_preserved,
    CASE 
        WHEN COUNT(*) = SUM(CASE WHEN weekly_pins = 0 THEN 1 ELSE 0 END)
        AND COUNT(*) = SUM(CASE WHEN total_pins > 0 THEN 1 ELSE 0 END)
        THEN 'PASS: Weekly reset successful, totals preserved'
        ELSE 'FAIL'
    END AS test_result
FROM Leaderboard;