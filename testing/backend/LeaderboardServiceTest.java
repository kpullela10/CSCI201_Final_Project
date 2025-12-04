package com.usc.squirrelspotter.service;

import com.usc.squirrelspotter.dto.LeaderboardEntryResponse;
import com.usc.squirrelspotter.dto.LeaderboardResponse;
import com.usc.squirrelspotter.dto.PinResponse;
import com.usc.squirrelspotter.exception.BadRequestException;
import com.usc.squirrelspotter.model.Pin;
import com.usc.squirrelspotter.model.User;
import com.usc.squirrelspotter.repository.PinRepository;
import com.usc.squirrelspotter.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Pageable;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for LeaderboardService
 * Tests leaderboard retrieval and user pin queries
 */
@ExtendWith(MockitoExtension.class)
class LeaderboardServiceTest {

    @Mock
    private PinRepository pinRepository;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private LeaderboardService leaderboardService;

    private User mockUser1;
    private User mockUser2;
    private Pin mockPin;

    @BeforeEach
    void setUp() {
        mockUser1 = new User("user1", "user1@usc.edu", "hash1");
        mockUser1.setUserID(1);

        mockUser2 = new User("user2", "user2@usc.edu", "hash2");
        mockUser2.setUserID(2);

        mockPin = new Pin(1, new BigDecimal("34.0224"), new BigDecimal("-118.2851"), 
            "Test pin", null);
        mockPin.setPinID(1);
        mockPin.setCreatedAt(LocalDateTime.now());
    }

    // ========== Get Leaderboard Tests - Weekly ==========

    @Test
    void testGetLeaderboard_Weekly_Success() {
        // Arrange
        List<Object[]> mockResults = Arrays.asList(
            new Object[]{1, "user1", 5L, 10L},  // userID, username, weeklyPins, totalPins
            new Object[]{2, "user2", 3L, 8L}
        );
        
        when(pinRepository.findWeeklyLeaderboard(any(LocalDateTime.class), any(Pageable.class)))
            .thenReturn(mockResults);
        when(pinRepository.countWeeklyLeaderboardUsers(any(LocalDateTime.class)))
            .thenReturn(2L);

        // Act
        LeaderboardResponse response = leaderboardService.getLeaderboard("weekly", 1, 10);

        // Assert
        assertNotNull(response);
        assertEquals(2, response.getEntries().size());
        assertEquals(2L, response.getTotalCount());
        
        LeaderboardEntryResponse firstEntry = response.getEntries().get(0);
        assertEquals(1, firstEntry.getUserID());
        assertEquals("user1", firstEntry.getUsername());
        assertEquals(10L, firstEntry.getTotalPins());
        assertEquals(5L, firstEntry.getWeeklyPins());

        verify(pinRepository, times(1)).findWeeklyLeaderboard(any(LocalDateTime.class), any(Pageable.class));
        verify(pinRepository, times(1)).countWeeklyLeaderboardUsers(any(LocalDateTime.class));
    }

    @Test
    void testGetLeaderboard_Weekly_EmptyResults() {
        // Arrange
        when(pinRepository.findWeeklyLeaderboard(any(LocalDateTime.class), any(Pageable.class)))
            .thenReturn(Arrays.asList());
        when(pinRepository.countWeeklyLeaderboardUsers(any(LocalDateTime.class)))
            .thenReturn(0L);

        // Act
        LeaderboardResponse response = leaderboardService.getLeaderboard("weekly", 1, 10);

        // Assert
        assertNotNull(response);
        assertTrue(response.getEntries().isEmpty());
        assertEquals(0L, response.getTotalCount());
    }

    @Test
    void testGetLeaderboard_Weekly_Pagination() {
        // Arrange
        List<Object[]> mockResults = Arrays.asList(
            new Object[]{3, "user3", 2L, 7L}
        );
        
        when(pinRepository.findWeeklyLeaderboard(any(LocalDateTime.class), any(Pageable.class)))
            .thenReturn(mockResults);
        when(pinRepository.countWeeklyLeaderboardUsers(any(LocalDateTime.class)))
            .thenReturn(15L);

        // Act
        LeaderboardResponse response = leaderboardService.getLeaderboard("weekly", 2, 5);

        // Assert
        assertNotNull(response);
        assertEquals(1, response.getEntries().size());
        assertEquals(15L, response.getTotalCount());
        
        // Verify pagination - page 2 with size 5 means offset of 5 (Spring uses 0-indexed pages)
        verify(pinRepository, times(1)).findWeeklyLeaderboard(
            any(LocalDateTime.class), 
            argThat(pageable -> pageable.getPageNumber() == 1 && pageable.getPageSize() == 5)
        );
    }

    // ========== Get Leaderboard Tests - All Time ==========

    @Test
    void testGetLeaderboard_AllTime_Success() {
        // Arrange
        List<Object[]> mockResults = Arrays.asList(
            new Object[]{1, "user1", 5L, 20L},
            new Object[]{2, "user2", 3L, 15L}
        );
        
        when(pinRepository.findAllTimeLeaderboard(any(LocalDateTime.class), any(Pageable.class)))
            .thenReturn(mockResults);
        when(pinRepository.countAllTimeLeaderboardUsers())
            .thenReturn(2L);

        // Act
        LeaderboardResponse response = leaderboardService.getLeaderboard("all-time", 1, 10);

        // Assert
        assertNotNull(response);
        assertEquals(2, response.getEntries().size());
        assertEquals(2L, response.getTotalCount());
        
        LeaderboardEntryResponse firstEntry = response.getEntries().get(0);
        assertEquals(20L, firstEntry.getTotalPins());

        verify(pinRepository, times(1)).findAllTimeLeaderboard(any(LocalDateTime.class), any(Pageable.class));
        verify(pinRepository, times(1)).countAllTimeLeaderboardUsers();
    }

    @Test
    void testGetLeaderboard_AllTime_EmptyResults() {
        // Arrange
        when(pinRepository.findAllTimeLeaderboard(any(LocalDateTime.class), any(Pageable.class)))
            .thenReturn(Arrays.asList());
        when(pinRepository.countAllTimeLeaderboardUsers())
            .thenReturn(0L);

        // Act
        LeaderboardResponse response = leaderboardService.getLeaderboard("all-time", 1, 10);

        // Assert
        assertNotNull(response);
        assertTrue(response.getEntries().isEmpty());
        assertEquals(0L, response.getTotalCount());
    }

    // ========== Get Leaderboard Validation Tests ==========

    @Test
    void testGetLeaderboard_InvalidType_ThrowsBadRequestException() {
        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> leaderboardService.getLeaderboard("invalid", 1, 10));
        assertEquals("Invalid type. Must be 'weekly' or 'all-time'", exception.getMessage());
        
        verify(pinRepository, never()).findWeeklyLeaderboard(any(), any());
        verify(pinRepository, never()).findAllTimeLeaderboard(any(), any());
    }

    @Test
    void testGetLeaderboard_PageZero_ThrowsBadRequestException() {
        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> leaderboardService.getLeaderboard("weekly", 0, 10));
        assertEquals("Page must be greater than 0", exception.getMessage());
    }

    @Test
    void testGetLeaderboard_NegativePage_ThrowsBadRequestException() {
        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> leaderboardService.getLeaderboard("weekly", -1, 10));
        assertEquals("Page must be greater than 0", exception.getMessage());
    }

    @Test
    void testGetLeaderboard_PageSizeZero_ThrowsBadRequestException() {
        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> leaderboardService.getLeaderboard("weekly", 1, 0));
        assertEquals("Page size must be between 1 and 100", exception.getMessage());
    }

    @Test
    void testGetLeaderboard_PageSizeTooLarge_ThrowsBadRequestException() {
        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> leaderboardService.getLeaderboard("weekly", 1, 101));
        assertEquals("Page size must be between 1 and 100", exception.getMessage());
    }

    @Test
    void testGetLeaderboard_MaxPageSize_Success() {
        // Arrange
        when(pinRepository.findWeeklyLeaderboard(any(LocalDateTime.class), any(Pageable.class)))
            .thenReturn(Arrays.asList());
        when(pinRepository.countWeeklyLeaderboardUsers(any(LocalDateTime.class)))
            .thenReturn(0L);

        // Act
        LeaderboardResponse response = leaderboardService.getLeaderboard("weekly", 1, 100);

        // Assert
        assertNotNull(response);
        verify(pinRepository, times(1)).findWeeklyLeaderboard(
            any(LocalDateTime.class),
            argThat(pageable -> pageable.getPageSize() == 100)
        );
    }

    @Test
    void testGetLeaderboard_CaseInsensitiveType_Weekly() {
        // Arrange
        when(pinRepository.findWeeklyLeaderboard(any(LocalDateTime.class), any(Pageable.class)))
            .thenReturn(Arrays.asList());
        when(pinRepository.countWeeklyLeaderboardUsers(any(LocalDateTime.class)))
            .thenReturn(0L);

        // Act
        LeaderboardResponse response = leaderboardService.getLeaderboard("WEEKLY", 1, 10);

        // Assert
        assertNotNull(response);
        verify(pinRepository, times(1)).findWeeklyLeaderboard(any(), any());
    }

    @Test
    void testGetLeaderboard_CaseInsensitiveType_AllTime() {
        // Arrange
        when(pinRepository.findAllTimeLeaderboard(any(LocalDateTime.class), any(Pageable.class)))
            .thenReturn(Arrays.asList());
        when(pinRepository.countAllTimeLeaderboardUsers())
            .thenReturn(0L);

        // Act
        LeaderboardResponse response = leaderboardService.getLeaderboard("ALL-TIME", 1, 10);

        // Assert
        assertNotNull(response);
        verify(pinRepository, times(1)).findAllTimeLeaderboard(any(), any());
    }

    // ========== Get User Pins Tests ==========

    @Test
    void testGetUserPins_Success() {
        // Arrange
        List<Pin> mockPins = Arrays.asList(mockPin);
        when(userRepository.findById(1)).thenReturn(Optional.of(mockUser1));
        when(pinRepository.findByUserIDOrderByCreatedAtDesc(1)).thenReturn(mockPins);

        // Act
        List<PinResponse> responses = leaderboardService.getUserPins(1);

        // Assert
        assertNotNull(responses);
        assertEquals(1, responses.size());
        
        PinResponse response = responses.get(0);
        assertEquals(1, response.getPinID());
        assertEquals(1, response.getUserID());
        assertEquals("user1", response.getUsername());

        verify(userRepository, times(1)).findById(1);
        verify(pinRepository, times(1)).findByUserIDOrderByCreatedAtDesc(1);
    }

    @Test
    void testGetUserPins_EmptyList() {
        // Arrange
        when(userRepository.findById(1)).thenReturn(Optional.of(mockUser1));
        when(pinRepository.findByUserIDOrderByCreatedAtDesc(1)).thenReturn(Arrays.asList());

        // Act
        List<PinResponse> responses = leaderboardService.getUserPins(1);

        // Assert
        assertNotNull(responses);
        assertTrue(responses.isEmpty());
    }

    @Test
    void testGetUserPins_UserNotFound_ThrowsBadRequestException() {
        // Arrange
        when(userRepository.findById(999)).thenReturn(Optional.empty());

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> leaderboardService.getUserPins(999));
        assertEquals("User not found", exception.getMessage());
        
        verify(pinRepository, never()).findByUserIDOrderByCreatedAtDesc(any());
    }

    @Test
    void testGetUserPins_MultiplePins() {
        // Arrange
        Pin pin1 = new Pin(1, new BigDecimal("34.0224"), new BigDecimal("-118.2851"), 
            "Pin 1", null);
        pin1.setPinID(1);
        pin1.setCreatedAt(LocalDateTime.now());

        Pin pin2 = new Pin(1, new BigDecimal("34.0225"), new BigDecimal("-118.2852"), 
            "Pin 2", "/uploads/image.jpg");
        pin2.setPinID(2);
        pin2.setCreatedAt(LocalDateTime.now().minusHours(1));

        List<Pin> mockPins = Arrays.asList(pin1, pin2);
        when(userRepository.findById(1)).thenReturn(Optional.of(mockUser1));
        when(pinRepository.findByUserIDOrderByCreatedAtDesc(1)).thenReturn(mockPins);

        // Act
        List<PinResponse> responses = leaderboardService.getUserPins(1);

        // Assert
        assertNotNull(responses);
        assertEquals(2, responses.size());
        assertEquals(1, responses.get(0).getPinID());
        assertEquals(2, responses.get(1).getPinID());
        assertEquals("/uploads/image.jpg", responses.get(1).getImageUrl());
    }
}
