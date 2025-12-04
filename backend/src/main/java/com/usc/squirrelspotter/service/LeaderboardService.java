package com.usc.squirrelspotter.service;

import com.usc.squirrelspotter.dto.LeaderboardEntryResponse;
import com.usc.squirrelspotter.dto.LeaderboardResponse;
import com.usc.squirrelspotter.dto.PinResponse;
import com.usc.squirrelspotter.exception.BadRequestException;
import com.usc.squirrelspotter.model.Pin;
import com.usc.squirrelspotter.model.User;
import com.usc.squirrelspotter.repository.PinRepository;
import com.usc.squirrelspotter.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service for Leaderboard business logic
 */
@Service
public class LeaderboardService {

    @Autowired
    private PinRepository pinRepository;

    @Autowired
    private UserRepository userRepository;

    /**
     * Get leaderboard entries with pagination
     * @param type "weekly" or "all-time"
     * @param page Page number (1-indexed)
     * @param pageSize Number of entries per page
     * @return Leaderboard response with entries and total count
     */
    public LeaderboardResponse getLeaderboard(String type, int page, int pageSize) {
        // Validate inputs
        if (page < 1) {
            throw new BadRequestException("Page must be greater than 0");
        }
        if (pageSize < 1 || pageSize > 100) {
            throw new BadRequestException("Page size must be between 1 and 100");
        }

        // Calculate week start (7 days ago)
        LocalDateTime weekStart = LocalDateTime.now().minusDays(7);

        // Create pageable (Spring uses 0-indexed pages internally)
        Pageable pageable = PageRequest.of(page - 1, pageSize);

        // Fetch leaderboard based on type
        List<Object[]> results;
        Long totalCount;

        if ("weekly".equalsIgnoreCase(type)) {
            results = pinRepository.findWeeklyLeaderboard(weekStart, pageable);
            totalCount = pinRepository.countWeeklyLeaderboardUsers(weekStart);
        } else if ("all-time".equalsIgnoreCase(type)) {
            results = pinRepository.findAllTimeLeaderboard(weekStart, pageable);
            totalCount = pinRepository.countAllTimeLeaderboardUsers();
        } else {
            throw new BadRequestException("Invalid type. Must be 'weekly' or 'all-time'");
        }

        // Convert Object[] results to DTOs
        List<LeaderboardEntryResponse> entries = results.stream()
                .map(row -> new LeaderboardEntryResponse(
                        (Integer) row[0],  // userID
                        (String) row[1],   // username
                        (Long) row[3],     // totalPins
                        (Long) row[2]      // weeklyPins
                ))
                .collect(Collectors.toList());

        return new LeaderboardResponse(entries, totalCount);
    }

    /**
     * Get all pins created by a specific user
     * @param userID User ID
     * @return List of user's pins
     */
    public List<PinResponse> getUserPins(Integer userID) {
        // Verify user exists
        User user = userRepository.findById(userID)
                .orElseThrow(() -> new BadRequestException("User not found"));

        // Fetch user's pins
        List<Pin> pins = pinRepository.findByUserIDOrderByCreatedAtDesc(userID);

        // Convert to responses
        return pins.stream()
                .map(pin -> new PinResponse(
                        pin.getPinID(),
                        pin.getUserID(),
                        pin.getLat(),
                        pin.getLng(),
                        pin.getDescription(),
                        pin.getImageUrl(),
                        pin.getCreatedAt(),
                        user.getUsername()
                ))
                .collect(Collectors.toList());
    }
}
