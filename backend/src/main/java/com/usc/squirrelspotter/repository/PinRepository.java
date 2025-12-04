package com.usc.squirrelspotter.repository;

import com.usc.squirrelspotter.model.Pin;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface PinRepository extends JpaRepository<Pin, Integer> {

    /**
     * Find all pins created by a specific user
     */
    List<Pin> findByUserIDOrderByCreatedAtDesc(Integer userID);

    /**
     * Find all pins created within the last 7 days
     */
    @Query("SELECT p FROM Pin p WHERE p.createdAt >= :startDate ORDER BY p.createdAt DESC")
    List<Pin> findWeeklyPins(@Param("startDate") LocalDateTime startDate);

    /**
     * Count pins created by a user within a time window (for rate limiting)
     */
    @Query("SELECT COUNT(p) FROM Pin p WHERE p.userID = :userID AND p.createdAt >= :startDate")
    Long countPinsByUserIDAndCreatedAtAfter(@Param("userID") Integer userID, @Param("startDate") LocalDateTime startDate);

    /**
     * Get weekly leaderboard - users with most pins in last 7 days
     * Returns Object[] containing: userID, username, weeklyPins, totalPins
     */
    @Query("SELECT p.userID, u.username, COUNT(CASE WHEN p.createdAt >= :weekStart THEN 1 END), COUNT(p) " +
           "FROM Pin p JOIN User u ON p.userID = u.userID " +
           "GROUP BY p.userID, u.username " +
           "HAVING COUNT(CASE WHEN p.createdAt >= :weekStart THEN 1 END) > 0 " +
           "ORDER BY COUNT(CASE WHEN p.createdAt >= :weekStart THEN 1 END) DESC")
    List<Object[]> findWeeklyLeaderboard(@Param("weekStart") LocalDateTime weekStart, Pageable pageable);

    /**
     * Get all-time leaderboard - users with most total pins
     * Returns Object[] containing: userID, username, weeklyPins, totalPins
     */
    @Query("SELECT p.userID, u.username, COUNT(CASE WHEN p.createdAt >= :weekStart THEN 1 END), COUNT(p) " +
           "FROM Pin p JOIN User u ON p.userID = u.userID " +
           "GROUP BY p.userID, u.username " +
           "ORDER BY COUNT(p) DESC")
    List<Object[]> findAllTimeLeaderboard(@Param("weekStart") LocalDateTime weekStart, Pageable pageable);

    /**
     * Count total users with pins for weekly leaderboard pagination
     */
    @Query("SELECT COUNT(DISTINCT p.userID) FROM Pin p WHERE p.createdAt >= :weekStart")
    Long countWeeklyLeaderboardUsers(@Param("weekStart") LocalDateTime weekStart);

    /**
     * Count total users with pins for all-time leaderboard pagination
     */
    @Query("SELECT COUNT(DISTINCT p.userID) FROM Pin p")
    Long countAllTimeLeaderboardUsers();
}

