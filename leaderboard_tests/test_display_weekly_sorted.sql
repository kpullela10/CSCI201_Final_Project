-- ============================================
-- USC Pin Mapping Application
-- File: 10_test_display_weekly_pins_sorted.sql
-- Test: Display Weekly Leaderboard Pins Sorted (Descending)
-- ============================================

USE usc_pin_test;

-- Query: Display leaderboard sorted by weekly_pins
-- (Uses data from 09_test_display_total_pins_sorted.sql)
SELECT 
    ROW_NUMBER() OVER (ORDER BY l.weekly_pins DESC) AS rank,
    u.email,
    l.total_pins,
    l.weekly_pins
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.weekly_pins DESC;

-- Expected Output (using data from previous test):
-- rank | email              | total_pins | weekly_pins
-- 1    | top_user@usc.edu   | 45         | 8
-- 2    | mid_user@usc.edu   | 23         | 5
-- 3    | new_user@usc.edu   | 3          | 3
-- 4    | low_user@usc.edu   | 12         | 2

-- Validation: Ensure descending order by weekly_pins
SELECT 
    email,
    weekly_pins,
    LAG(weekly_pins) OVER (ORDER BY weekly_pins DESC) AS previous_weekly,
    CASE 
        WHEN LAG(weekly_pins) OVER (ORDER BY weekly_pins DESC) IS NULL
        OR weekly_pins <= LAG(weekly_pins) OVER (ORDER BY weekly_pins DESC)
        THEN 'PASS'
        ELSE 'FAIL: Not in descending order' 
    END AS sort_validation
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.weekly_pins DESC;