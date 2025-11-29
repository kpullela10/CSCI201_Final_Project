-- ============================================
-- USC Pin Mapping Application - Cleanup Script
-- File: 00_cleanup_test_data.sql
-- Purpose: Clean up test data before running tests
-- ============================================

USE usc_pin_test;

-- Clean up script (run before each test suite)
DELETE FROM Pins;
DELETE FROM Leaderboard;
DELETE FROM Users;

-- Reset auto-increment counters
ALTER TABLE Users AUTO_INCREMENT = 1;
ALTER TABLE Pins AUTO_INCREMENT = 1;

-- Verify cleanup
SELECT 
    (SELECT COUNT(*) FROM Users) AS users_count,
    (SELECT COUNT(*) FROM Pins) AS pins_count,
    (SELECT COUNT(*) FROM Leaderboard) AS leaderboard_count,
    'Cleanup complete' AS status;