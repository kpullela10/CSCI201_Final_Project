-- ============================================
-- USC Pin Mapping Application
-- File: 12_test_leaderboard_pagination.sql
-- Test: Leaderboard Pagination (Display Top 50)
-- ============================================

USE usc_pin_test;

-- Setup: Create stored procedure to generate test users
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS create_test_users(IN num_users INT)
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= num_users DO
        INSERT INTO Users (email, password) 
        VALUES (CONCAT('paginationuser', i, '@usc.edu'), 'hashed_pass');
        
        INSERT INTO Leaderboard (UserID, total_pins, weekly_pins) 
        VALUES (LAST_INSERT_ID(), FLOOR(RAND() * 100), FLOOR(RAND() * 20));
        
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

-- Execute procedure to create 75 users
CALL create_test_users(75);

-- Query: Display top 50 users (Page 1)
SELECT 
    ROW_NUMBER() OVER (ORDER BY l.total_pins DESC) AS rank,
    u.email,
    l.total_pins,
    l.weekly_pins
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.total_pins DESC
LIMIT 50;

-- Query: Display next 25 users (Page 2)
SELECT 
    ROW_NUMBER() OVER (ORDER BY l.total_pins DESC) AS rank,
    u.email,
    l.total_pins,
    l.weekly_pins
FROM Leaderboard l
JOIN Users u ON l.UserID = u.UserID
ORDER BY l.total_pins DESC
LIMIT 50 OFFSET 50;

-- Validation: Check pagination logic
SELECT 
    'Page 1' AS page,
    COUNT(*) AS entries,
    CASE WHEN COUNT(*) = 50 THEN 'PASS' ELSE 'FAIL' END AS test_result
FROM (
    SELECT * FROM Leaderboard ORDER BY total_pins DESC LIMIT 50
) AS page1

UNION ALL

SELECT 
    'Page 2' AS page,
    COUNT(*) AS entries,
    CASE WHEN COUNT(*) = 25 THEN 'PASS' ELSE 'FAIL' END AS test_result
FROM (
    SELECT * FROM Leaderboard ORDER BY total_pins DESC LIMIT 50 OFFSET 50
) AS page2;

-- Verify total count
SELECT 
    COUNT(*) AS total_users,
    CASE 
        WHEN COUNT(*) >= 75 THEN 'PASS: Sufficient users for pagination test'
        ELSE 'FAIL'
    END AS test_result
FROM Leaderboard;

-- Clean up procedure
DROP PROCEDURE IF EXISTS create_test_users;