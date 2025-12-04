package com.usc.squirrelspotter.service;

import com.usc.squirrelspotter.controller.PinWebSocketHandler;
import com.usc.squirrelspotter.dto.PinResponse;
import com.usc.squirrelspotter.exception.BadRequestException;
import com.usc.squirrelspotter.exception.TooManyRequestsException;
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
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for PinService
 * Tests pin creation, retrieval, and rate limiting logic
 */
@ExtendWith(MockitoExtension.class)
class PinServiceTest {

    @Mock
    private PinRepository pinRepository;

    @Mock
    private UserRepository userRepository;

    @Mock
    private ImageStorageService imageStorageService;

    @Mock
    private PinWebSocketHandler pinWebSocketHandler;

    @InjectMocks
    private PinService pinService;

    private User mockUser;
    private Pin mockPin;
    private BigDecimal validLat;
    private BigDecimal validLng;

    @BeforeEach
    void setUp() {
        mockUser = new User("testuser", "testuser@usc.edu", "hashedPassword");
        mockUser.setUserID(1);

        validLat = new BigDecimal("34.0224");
        validLng = new BigDecimal("-118.2851");

        mockPin = new Pin(1, validLat, validLng, "Test description", null);
        mockPin.setPinID(1);
        mockPin.setCreatedAt(LocalDateTime.now());
    }

    // ========== Create Pin Tests ==========

    @Test
    void testCreatePin_Success_NoImage() {
        // Arrange
        when(pinRepository.countPinsByUserIDAndCreatedAtAfter(anyInt(), any(LocalDateTime.class)))
            .thenReturn(2L);
        when(pinRepository.save(any(Pin.class))).thenReturn(mockPin);
        when(userRepository.findById(anyInt())).thenReturn(Optional.of(mockUser));
        doNothing().when(pinWebSocketHandler).broadcastPin(any(PinResponse.class));

        // Act
        PinResponse response = pinService.createPin(1, validLat, validLng, "Test description", null);

        // Assert
        assertNotNull(response);
        assertEquals(1, response.getPinID());
        assertEquals("testuser", response.getUsername());
        assertEquals(validLat, response.getLat());
        assertEquals(validLng, response.getLng());

        verify(pinRepository, times(1)).save(any(Pin.class));
        verify(pinWebSocketHandler, times(1)).broadcastPin(any(PinResponse.class));
    }

    @Test
    void testCreatePin_Success_WithImage() throws IOException {
        // Arrange
        MultipartFile mockFile = mock(MultipartFile.class);
        when(mockFile.isEmpty()).thenReturn(false);
        when(imageStorageService.saveImage(mockFile)).thenReturn("/uploads/image.jpg");
        when(pinRepository.countPinsByUserIDAndCreatedAtAfter(anyInt(), any(LocalDateTime.class)))
            .thenReturn(2L);
        
        Pin pinWithImage = new Pin(1, validLat, validLng, "Test", "/uploads/image.jpg");
        pinWithImage.setPinID(1);
        pinWithImage.setCreatedAt(LocalDateTime.now());
        
        when(pinRepository.save(any(Pin.class))).thenReturn(pinWithImage);
        when(userRepository.findById(anyInt())).thenReturn(Optional.of(mockUser));
        doNothing().when(pinWebSocketHandler).broadcastPin(any(PinResponse.class));

        // Act
        PinResponse response = pinService.createPin(1, validLat, validLng, "Test", mockFile);

        // Assert
        assertNotNull(response);
        assertEquals("/uploads/image.jpg", response.getImageUrl());
        
        verify(imageStorageService, times(1)).saveImage(mockFile);
    }

    @Test
    void testCreatePin_MissingLatitude_ThrowsBadRequestException() {
        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.createPin(1, null, validLng, "Test", null));
        assertEquals("Latitude and longitude are required", exception.getMessage());
        
        verify(pinRepository, never()).save(any());
    }

    @Test
    void testCreatePin_MissingLongitude_ThrowsBadRequestException() {
        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.createPin(1, validLat, null, "Test", null));
        assertEquals("Latitude and longitude are required", exception.getMessage());
    }

    @Test
    void testCreatePin_InvalidLatitude_TooHigh_ThrowsBadRequestException() {
        // Arrange
        BigDecimal invalidLat = new BigDecimal("91.0");

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.createPin(1, invalidLat, validLng, "Test", null));
        assertEquals("Latitude must be between -90 and 90", exception.getMessage());
    }

    @Test
    void testCreatePin_InvalidLatitude_TooLow_ThrowsBadRequestException() {
        // Arrange
        BigDecimal invalidLat = new BigDecimal("-91.0");

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.createPin(1, invalidLat, validLng, "Test", null));
        assertEquals("Latitude must be between -90 and 90", exception.getMessage());
    }

    @Test
    void testCreatePin_InvalidLongitude_TooHigh_ThrowsBadRequestException() {
        // Arrange
        BigDecimal invalidLng = new BigDecimal("181.0");

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.createPin(1, validLat, invalidLng, "Test", null));
        assertEquals("Longitude must be between -180 and 180", exception.getMessage());
    }

    @Test
    void testCreatePin_InvalidLongitude_TooLow_ThrowsBadRequestException() {
        // Arrange
        BigDecimal invalidLng = new BigDecimal("-181.0");

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.createPin(1, validLat, invalidLng, "Test", null));
        assertEquals("Longitude must be between -180 and 180", exception.getMessage());
    }

    @Test
    void testCreatePin_RateLimitExceeded_ThrowsTooManyRequestsException() {
        // Arrange - user already created 5 pins in the last 30 minutes
        when(pinRepository.countPinsByUserIDAndCreatedAtAfter(anyInt(), any(LocalDateTime.class)))
            .thenReturn(5L);

        // Act & Assert
        TooManyRequestsException exception = assertThrows(TooManyRequestsException.class, 
            () -> pinService.createPin(1, validLat, validLng, "Test", null));
        assertTrue(exception.getMessage().contains("Rate limit exceeded"));
        
        verify(pinRepository, never()).save(any());
    }

    @Test
    void testCreatePin_ImageUploadFails_ThrowsBadRequestException() throws IOException {
        // Arrange
        MultipartFile mockFile = mock(MultipartFile.class);
        when(mockFile.isEmpty()).thenReturn(false);
        when(imageStorageService.saveImage(mockFile)).thenThrow(new IOException("Disk full"));
        when(pinRepository.countPinsByUserIDAndCreatedAtAfter(anyInt(), any(LocalDateTime.class)))
            .thenReturn(2L);

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.createPin(1, validLat, validLng, "Test", mockFile));
        assertTrue(exception.getMessage().contains("Failed to save image"));
    }

    // ========== Get Weekly Pins Tests ==========

    @Test
    void testGetWeeklyPins_Success() {
        // Arrange
        List<Pin> mockPins = Arrays.asList(mockPin);
        when(pinRepository.findWeeklyPins(any(LocalDateTime.class))).thenReturn(mockPins);
        when(userRepository.findById(1)).thenReturn(Optional.of(mockUser));

        // Act
        List<PinResponse> responses = pinService.getWeeklyPins();

        // Assert
        assertNotNull(responses);
        assertEquals(1, responses.size());
        assertEquals("testuser", responses.get(0).getUsername());
        
        verify(pinRepository, times(1)).findWeeklyPins(any(LocalDateTime.class));
    }

    @Test
    void testGetWeeklyPins_EmptyList() {
        // Arrange
        when(pinRepository.findWeeklyPins(any(LocalDateTime.class))).thenReturn(Arrays.asList());

        // Act
        List<PinResponse> responses = pinService.getWeeklyPins();

        // Assert
        assertNotNull(responses);
        assertTrue(responses.isEmpty());
    }

    @Test
    void testGetWeeklyPins_UserNotFound_ReturnsNullUsername() {
        // Arrange
        List<Pin> mockPins = Arrays.asList(mockPin);
        when(pinRepository.findWeeklyPins(any(LocalDateTime.class))).thenReturn(mockPins);
        when(userRepository.findById(1)).thenReturn(Optional.empty());

        // Act
        List<PinResponse> responses = pinService.getWeeklyPins();

        // Assert
        assertNotNull(responses);
        assertEquals(1, responses.size());
        assertNull(responses.get(0).getUsername());
    }

    // ========== Get My Pins Tests ==========

    @Test
    void testGetMyPins_Success() {
        // Arrange
        List<Pin> mockPins = Arrays.asList(mockPin);
        when(pinRepository.findByUserIDOrderByCreatedAtDesc(1)).thenReturn(mockPins);
        when(userRepository.findById(1)).thenReturn(Optional.of(mockUser));

        // Act
        List<PinResponse> responses = pinService.getMyPins(1);

        // Assert
        assertNotNull(responses);
        assertEquals(1, responses.size());
        assertEquals("testuser", responses.get(0).getUsername());
        
        verify(pinRepository, times(1)).findByUserIDOrderByCreatedAtDesc(1);
    }

    @Test
    void testGetMyPins_UserNotFound_ThrowsBadRequestException() {
        // Arrange
        when(pinRepository.findByUserIDOrderByCreatedAtDesc(999)).thenReturn(Arrays.asList());
        when(userRepository.findById(999)).thenReturn(Optional.empty());

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.getMyPins(999));
        assertEquals("User not found", exception.getMessage());
    }

    // ========== Get Pin By ID Tests ==========

    @Test
    void testGetPinById_Success() {
        // Arrange
        when(pinRepository.findById(1)).thenReturn(Optional.of(mockPin));
        when(userRepository.findById(1)).thenReturn(Optional.of(mockUser));

        // Act
        PinResponse response = pinService.getPinById(1);

        // Assert
        assertNotNull(response);
        assertEquals(1, response.getPinID());
        assertEquals("testuser", response.getUsername());
        
        verify(pinRepository, times(1)).findById(1);
    }

    @Test
    void testGetPinById_PinNotFound_ThrowsBadRequestException() {
        // Arrange
        when(pinRepository.findById(999)).thenReturn(Optional.empty());

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> pinService.getPinById(999));
        assertEquals("Pin not found", exception.getMessage());
    }

    @Test
    void testGetPinById_UserNotFound_ReturnsNullUsername() {
        // Arrange
        when(pinRepository.findById(1)).thenReturn(Optional.of(mockPin));
        when(userRepository.findById(1)).thenReturn(Optional.empty());

        // Act
        PinResponse response = pinService.getPinById(1);

        // Assert
        assertNotNull(response);
        assertNull(response.getUsername());
    }
}
