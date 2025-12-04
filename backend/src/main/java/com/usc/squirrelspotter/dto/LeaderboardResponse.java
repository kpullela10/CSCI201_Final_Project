package com.usc.squirrelspotter.dto;

import java.util.List;

/**
 * DTO for Leaderboard response with pagination info
 */
public class LeaderboardResponse {
    private List<LeaderboardEntryResponse> entries;
    private Long totalCount;

    // Constructors
    public LeaderboardResponse() {}

    public LeaderboardResponse(List<LeaderboardEntryResponse> entries, Long totalCount) {
        this.entries = entries;
        this.totalCount = totalCount;
    }

    // Getters and Setters
    public List<LeaderboardEntryResponse> getEntries() {
        return entries;
    }

    public void setEntries(List<LeaderboardEntryResponse> entries) {
        this.entries = entries;
    }

    public Long getTotalCount() {
        return totalCount;
    }

    public void setTotalCount(Long totalCount) {
        this.totalCount = totalCount;
    }
}
