package com.usc.squirrelspotter.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * DTO for Leaderboard entry response
 * Uses snake_case field names to match frontend TypeScript interface
 */
public class LeaderboardEntryResponse {
    @JsonProperty("userID")
    private Integer userID;

    private String username;

    @JsonProperty("total_pins")
    private Long totalPins;

    @JsonProperty("weekly_pins")
    private Long weeklyPins;

    // Constructors
    public LeaderboardEntryResponse() {}

    public LeaderboardEntryResponse(Integer userID, String username, Long totalPins, Long weeklyPins) {
        this.userID = userID;
        this.username = username;
        this.totalPins = totalPins;
        this.weeklyPins = weeklyPins;
    }

    // Getters and Setters
    public Integer getUserID() {
        return userID;
    }

    public void setUserID(Integer userID) {
        this.userID = userID;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public Long getTotalPins() {
        return totalPins;
    }

    public void setTotalPins(Long totalPins) {
        this.totalPins = totalPins;
    }

    public Long getWeeklyPins() {
        return weeklyPins;
    }

    public void setWeeklyPins(Long weeklyPins) {
        this.weeklyPins = weeklyPins;
    }
}
