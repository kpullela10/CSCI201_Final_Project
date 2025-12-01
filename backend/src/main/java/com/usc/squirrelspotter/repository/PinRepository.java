package com.usc.squirrelspotter.repository;

import com.usc.squirrelspotter.model.Pin;
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
}

