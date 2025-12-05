package com.usc.squirrelspotter.controller;

import com.usc.squirrelspotter.dto.ErrorResponse;
import com.usc.squirrelspotter.dto.PinResponse;
import com.usc.squirrelspotter.exception.BadRequestException;
import com.usc.squirrelspotter.exception.TooManyRequestsException;
import com.usc.squirrelspotter.service.PinService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.math.BigDecimal;
import java.util.List;

/**
 * REST controller for Pin endpoints
 */
@RestController
@RequestMapping("/api/pins")
public class PinController {

    @Autowired
    private PinService pinService;

    /**
     * POST /api/pins - Create a new pin with optional image upload or external image URL
     * Requires authentication
     */
    @PostMapping
    public ResponseEntity<?> createPin(
            @RequestParam("lat") BigDecimal lat,
            @RequestParam("lng") BigDecimal lng,
            @RequestParam(value = "description", required = false) String description,
            @RequestParam(value = "image", required = false) MultipartFile imageFile,
            @RequestParam(value = "image_url", required = false) String imageUrl,
            Authentication authentication) {
        try {
            if (authentication == null || authentication.getPrincipal() == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ErrorResponse("Authentication required"));
            }
            Integer userID = (Integer) authentication.getPrincipal();
            PinResponse response = pinService.createPin(userID, lat, lng, description, imageFile, imageUrl);
            return ResponseEntity.status(HttpStatus.CREATED).body(response);
        } catch (BadRequestException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ErrorResponse(e.getMessage()));
        } catch (TooManyRequestsException e) {
            return ResponseEntity.status(HttpStatus.TOO_MANY_REQUESTS)
                    .body(new ErrorResponse(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ErrorResponse("An error occurred while creating the pin"));
        }
    }

    /**
     * GET /api/pins/weekly - Get pins from the last 7 days
     * Public endpoint (no authentication required)
     */
    @GetMapping("/weekly")
    public ResponseEntity<?> getWeeklyPins() {
        try {
            List<PinResponse> pins = pinService.getWeeklyPins();
            return ResponseEntity.ok(pins);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ErrorResponse("An error occurred while fetching weekly pins"));
        }
    }

    /**
     * GET /api/pins/my - Get authenticated user's pins
     * Requires authentication
     */
    @GetMapping("/my")
    public ResponseEntity<?> getMyPins(Authentication authentication) {
        try {
            if (authentication == null || authentication.getPrincipal() == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body(new ErrorResponse("Authentication required"));
            }
            Integer userID = (Integer) authentication.getPrincipal();
            List<PinResponse> pins = pinService.getMyPins(userID);
            return ResponseEntity.ok(pins);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ErrorResponse("An error occurred while fetching your pins"));
        }
    }

    /**
     * GET /api/pins/{pinID} - Get pin by ID
     * Public endpoint (no authentication required)
     */
    @GetMapping("/{pinID}")
    public ResponseEntity<?> getPinById(@PathVariable Integer pinID) {
        try {
            PinResponse pin = pinService.getPinById(pinID);
            return ResponseEntity.ok(pin);
        } catch (BadRequestException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(new ErrorResponse(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ErrorResponse("An error occurred while fetching the pin"));
        }
    }
}

