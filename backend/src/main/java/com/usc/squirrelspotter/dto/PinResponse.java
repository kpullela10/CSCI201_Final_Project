package com.usc.squirrelspotter.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * DTO for Pin response - includes username for display
 * Uses snake_case field names to match frontend TypeScript interface
 */
public class PinResponse {
    @JsonProperty("pinID")
    private Integer pinID;
    
    @JsonProperty("userID")
    private Integer userID;
    
    private BigDecimal lat;
    private BigDecimal lng;
    private String description;
    
    @JsonProperty("image_url")
    private String imageUrl;
    
    @JsonProperty("created_at")
    private String createdAt;
    
    private String username; // Optional: populated by backend for display

    private static final DateTimeFormatter ISO_FORMATTER = DateTimeFormatter.ISO_DATE_TIME;

    // Constructors
    public PinResponse() {}

    public PinResponse(Integer pinID, Integer userID, BigDecimal lat, BigDecimal lng,
                       String description, String imageUrl, LocalDateTime createdAt, String username) {
        this.pinID = pinID;
        this.userID = userID;
        this.lat = lat;
        this.lng = lng;
        this.description = description;
        this.imageUrl = imageUrl;
        this.createdAt = createdAt != null ? createdAt.format(ISO_FORMATTER) : null;
        this.username = username;
    }

    // Getters and Setters
    public Integer getPinID() {
        return pinID;
    }

    public void setPinID(Integer pinID) {
        this.pinID = pinID;
    }

    public Integer getUserID() {
        return userID;
    }

    public void setUserID(Integer userID) {
        this.userID = userID;
    }

    public BigDecimal getLat() {
        return lat;
    }

    public void setLat(BigDecimal lat) {
        this.lat = lat;
    }

    public BigDecimal getLng() {
        return lng;
    }

    public void setLng(BigDecimal lng) {
        this.lng = lng;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }
}

