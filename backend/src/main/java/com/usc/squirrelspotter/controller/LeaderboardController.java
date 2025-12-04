package com.usc.squirrelspotter.controller;

import com.usc.squirrelspotter.dto.ErrorResponse;
import com.usc.squirrelspotter.dto.LeaderboardResponse;
import com.usc.squirrelspotter.dto.PinResponse;
import com.usc.squirrelspotter.exception.BadRequestException;
import com.usc.squirrelspotter.service.LeaderboardService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST controller for Leaderboard endpoints
 */
@RestController
@RequestMapping("/api")
public class LeaderboardController {

    @Autowired
    private LeaderboardService leaderboardService;

    /**
     * GET /api/leaderboard - Get leaderboard with pagination
     * Query parameters:
     *   - type: "weekly" or "all-time" (required)
     *   - page: page number, 1-indexed (default: 1)
     *   - pageSize: entries per page (default: 20, max: 100)
     */
    @GetMapping("/leaderboard")
    public ResponseEntity<?> getLeaderboard(
            @RequestParam(value = "type", required = true) String type,
            @RequestParam(value = "page", defaultValue = "1") int page,
            @RequestParam(value = "pageSize", defaultValue = "20") int pageSize) {
        try {
            LeaderboardResponse response = leaderboardService.getLeaderboard(type, page, pageSize);
            return ResponseEntity.ok(response);
        } catch (BadRequestException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(new ErrorResponse(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ErrorResponse("An error occurred while fetching the leaderboard"));
        }
    }

    /**
     * GET /api/users/{userID}/pins - Get all pins by a specific user
     * Public endpoint (no authentication required)
     */
    @GetMapping("/users/{userID}/pins")
    public ResponseEntity<?> getUserPins(@PathVariable Integer userID) {
        try {
            List<PinResponse> pins = leaderboardService.getUserPins(userID);
            return ResponseEntity.ok(pins);
        } catch (BadRequestException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(new ErrorResponse(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(new ErrorResponse("An error occurred while fetching user pins"));
        }
    }
}
