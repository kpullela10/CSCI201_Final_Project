package com.usc.squirrelspotter.model;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Pin entity - Represents a squirrel sighting pin on the map
 *
 * TODO for Pin/Maps team:
 * - Create PinRepository interface
 * - Create PinService with business logic
 * - Create PinController with REST endpoints
 * - Implement image upload handling
 * - Implement rate limiting (4-5 pins per 30 minutes)
 * - Implement WebSocket for real-time updates
 */
@Entity
@Table(name = "pins")
public class Pin {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer pinID;

    @Column(nullable = false)
    private Integer userID;

    @Column(nullable = false, precision = 10, scale = 8)
    private BigDecimal lat;

    @Column(nullable = false, precision = 11, scale = 8)
    private BigDecimal lng;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(name = "image_url", length = 500)
    private String imageUrl;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    // Constructors
    public Pin() {}

    public Pin(Integer userID, BigDecimal lat, BigDecimal lng, String description, String imageUrl) {
        this.userID = userID;
        this.lat = lat;
        this.lng = lng;
        this.description = description;
        this.imageUrl = imageUrl;
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

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
