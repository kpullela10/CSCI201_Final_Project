package com.usc.squirrelspotter.service;

import com.usc.squirrelspotter.controller.PinWebSocketHandler;
import com.usc.squirrelspotter.dto.PinResponse;
import com.usc.squirrelspotter.exception.BadRequestException;
import com.usc.squirrelspotter.exception.TooManyRequestsException;
import com.usc.squirrelspotter.model.Pin;
import com.usc.squirrelspotter.model.User;
import com.usc.squirrelspotter.repository.PinRepository;
import com.usc.squirrelspotter.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Service for Pin business logic
 */
@Service
public class PinService {

    @Autowired
    private PinRepository pinRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ImageStorageService imageStorageService;

    @Autowired
    private PinWebSocketHandler pinWebSocketHandler;

    // Rate limiting: 4-5 pins per 30 minutes
    private static final int MAX_PINS_PER_WINDOW = 5;
    private static final int RATE_LIMIT_WINDOW_MINUTES = 30;

    /**
     * Create a new pin with optional image upload or external image URL
     * @param userID Authenticated user ID
     * @param lat Latitude
     * @param lng Longitude
     * @param description Optional description
     * @param imageFile Optional image file (for file uploads)
     * @param imageUrl Optional external image URL (for default images)
     * @return Created pin response
     */
    public PinResponse createPin(Integer userID, BigDecimal lat, BigDecimal lng,
                                 String description, MultipartFile imageFile, String imageUrl) {
        // Validate input
        if (lat == null || lng == null) {
            throw new BadRequestException("Latitude and longitude are required");
        }

        // Validate coordinates
        if (lat.compareTo(new BigDecimal("-90")) < 0 || lat.compareTo(new BigDecimal("90")) > 0) {
            throw new BadRequestException("Latitude must be between -90 and 90");
        }
        if (lng.compareTo(new BigDecimal("-180")) < 0 || lng.compareTo(new BigDecimal("180")) > 0) {
            throw new BadRequestException("Longitude must be between -180 and 180");
        }

        // Check rate limiting
        checkRateLimit(userID);

        // Handle image: either file upload OR external URL
        String finalImageUrl = null;
        if (imageFile != null && !imageFile.isEmpty()) {
            // Save uploaded file
            try {
                finalImageUrl = imageStorageService.saveImage(imageFile);
            } catch (IOException e) {
                throw new BadRequestException("Failed to save image: " + e.getMessage());
            }
        } else if (imageUrl != null && !imageUrl.trim().isEmpty()) {
            // Use external URL directly (for default images)
            finalImageUrl = imageUrl.trim();
        }

        // Create and save pin
        Pin pin = new Pin(userID, lat, lng, description, finalImageUrl);
        pin = pinRepository.save(pin);

        // Get username for response
        User user = userRepository.findById(userID)
                .orElseThrow(() -> new BadRequestException("User not found"));

        PinResponse response = convertToResponse(pin, user.getUsername());

        // Broadcast new pin via WebSocket
        pinWebSocketHandler.broadcastPin(response);

        return response;
    }

    /**
     * Get pins from the current week (last 7 days)
     * @return List of pins from the last 7 days
     */
    public List<PinResponse> getWeeklyPins() {
        LocalDateTime weekAgo = LocalDateTime.now().minusDays(7);
        List<Pin> pins = pinRepository.findWeeklyPins(weekAgo);
        
        return pins.stream()
                .map(pin -> {
                    User user = userRepository.findById(pin.getUserID()).orElse(null);
                    return convertToResponse(pin, user != null ? user.getUsername() : null);
                })
                .collect(Collectors.toList());
    }

    /**
     * Get all pins created by the authenticated user
     * @param userID Authenticated user ID
     * @return List of user's pins
     */
    public List<PinResponse> getMyPins(Integer userID) {
        List<Pin> pins = pinRepository.findByUserIDOrderByCreatedAtDesc(userID);
        User user = userRepository.findById(userID)
                .orElseThrow(() -> new BadRequestException("User not found"));
        
        return pins.stream()
                .map(pin -> convertToResponse(pin, user.getUsername()))
                .collect(Collectors.toList());
    }

    /**
     * Get pin by ID
     * @param pinID Pin ID
     * @return Pin response
     */
    public PinResponse getPinById(Integer pinID) {
        Pin pin = pinRepository.findById(pinID)
                .orElseThrow(() -> new BadRequestException("Pin not found"));
        
        User user = userRepository.findById(pin.getUserID()).orElse(null);
        return convertToResponse(pin, user != null ? user.getUsername() : null);
    }

    /**
     * Check rate limiting for pin creation
     * @param userID User ID to check
     * @throws TooManyRequestsException if rate limit exceeded
     */
    private void checkRateLimit(Integer userID) {
        LocalDateTime windowStart = LocalDateTime.now().minusMinutes(RATE_LIMIT_WINDOW_MINUTES);
        Long pinCount = pinRepository.countPinsByUserIDAndCreatedAtAfter(userID, windowStart);
        
        if (pinCount >= MAX_PINS_PER_WINDOW) {
            throw new TooManyRequestsException(
                    "Rate limit exceeded. Maximum " + MAX_PINS_PER_WINDOW + 
                    " pins allowed per " + RATE_LIMIT_WINDOW_MINUTES + " minutes."
            );
        }
    }

    /**
     * Convert Pin entity to PinResponse DTO
     */
    private PinResponse convertToResponse(Pin pin, String username) {
        return new PinResponse(
                pin.getPinID(),
                pin.getUserID(),
                pin.getLat(),
                pin.getLng(),
                pin.getDescription(),
                pin.getImageUrl(),
                pin.getCreatedAt(),
                username
        );
    }
}

