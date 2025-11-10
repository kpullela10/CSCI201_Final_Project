-- ============================================
-- USC Pin Mapping Application
-- File: 11_test_handle_tied_rankings.sql
-- Test: Handle Tied Leaderboard Ranking
-- ============================================

USE usc_pin_test;

-- Setup: Create users with identical pin counts
INSERT INTO Users (email, password) VALUES 
    ('tie1@usc.edu', 'pass1'),
    ('tie2@usc.edu', 'pass2'),
    ('tie3@usc.edu', 'pass3'),
    ('unique@usc.edu', 'pass4');

SET @tie1 = (SELECT UserID FROM Users WHERE email = 'tie1@usc.edu');
SET @tie2 = (SELECT UserID FROM Users WHERE email = 'tie2@usc.edu');
SET @tie3 = (SELECT UserID FROM Users WHERE email = 'tie3@usc.edu');
SET @unique = (SELECT UserID FROM Users WHERE email = 'unique@usc.edu');

-- Create tied entries
INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) VALUES 
    (@tie1, 20, 5),
    (@tie2, 20, 5),  -- Tied with tie1
    (@tie3, 20, 3),  -- Tied on total, different weekly
    (@unique, 25, 10);

-- Query with RANK (shows ties with same rank number)
SELECT 
    RANK() OVER (ORDER BY l.total_pins DESC) AS rank,
    u.email,
    l.total_pins,
    l.weekly_pins
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.total_pins DESC, u.email ASC;

-- Expected Output:
-- rank | email           | total_pins | weekly_pins
-- 1    | unique@usc.edu  | 25         | 10
-- 2    | tie1@usc.edu    | 20         | 5
-- 2    | tie2@usc.edu    | 20         | 5
-- 2    | tie3@usc.edu    | 20         | 3

-- Alternative: Use DENSE_RANK for consecutive rankings
SELECT 
    DENSE_RANK() OVER (ORDER BY l.total_pins DESC) AS rank,
    u.email,
    l.total_pins,
    l.weekly_pins
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.total_pins DESC, l.weekly_pins DESC, u.email ASC;

-- Validation: Identify ties
SELECT 
    total_pins,
    COUNT(*) AS users_with_this_count,
    GROUP_CONCAT(email ORDER BY email) AS tied_users,
    CASE 
        WHEN COUNT(*) > 1 THEN 'TIE DETECTED' 
        ELSE 'UNIQUE' 
    END AS tie_status
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
GROUP BY total_pins
ORDER BY total_pins DESC;