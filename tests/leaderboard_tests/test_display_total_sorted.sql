-- ============================================
-- USC Pin Mapping Application
-- File: 09_test_display_total_pins_sorted.sql
-- Test: Display Total Leaderboard Pins Sorted (Descending)
-- ============================================

USE usc_pin_test;

-- Setup: Create multiple users with varying pin counts
INSERT INTO Users (email, password) VALUES 
    ('top_user@usc.edu', 'pass1'),
    ('mid_user@usc.edu', 'pass2'),
    ('low_user@usc.edu', 'pass3'),
    ('new_user@usc.edu', 'pass4');

SET @top = (SELECT UserID FROM Users WHERE email = 'top_user@usc.edu');
SET @mid = (SELECT UserID FROM Users WHERE email = 'mid_user@usc.edu');
SET @low = (SELECT UserID FROM Users WHERE email = 'low_user@usc.edu');
SET @new = (SELECT UserID FROM Users WHERE email = 'new_user@usc.edu');

-- Create leaderboard entries with different total_pins
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) VALUES 
    (@top, 45, 8),
    (@mid, 23, 5),
    (@low, 12, 2),
    (@new, 3, 3);

-- Query: Display leaderboard sorted by total_pins
SELECT 
    ROW_NUMBER() OVER (ORDER BY l.total_pins DESC) AS rank,
    u.email,
    l.total_pins,
    l.weekly_pins
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.total_pins DESC;

-- Expected Output:
-- rank | email              | total_pins | weekly_pins
-- 1    | top_user@usc.edu   | 45         | 8
-- 2    | mid_user@usc.edu   | 23         | 5
-- 3    | low_user@usc.edu   | 12         | 2
-- 4    | new_user@usc.edu   | 3          | 3

-- Validation: Ensure descending order
SELECT 
    email,
    total_pins,
    LAG(total_pins) OVER (ORDER BY total_pins DESC) AS previous_total,
    CASE 
        WHEN LAG(total_pins) OVER (ORDER BY total_pins DESC) IS NULL
        OR total_pins <= LAG(total_pins) OVER (ORDER BY total_pins DESC)
        THEN 'PASS'
        ELSE 'FAIL: Not in descending order' 
    END AS sort_validation
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.total_pins DESC;