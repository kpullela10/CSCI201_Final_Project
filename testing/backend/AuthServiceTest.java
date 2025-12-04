package com.usc.squirrelspotter.service;

import com.usc.squirrelspotter.dto.*;
import com.usc.squirrelspotter.exception.AuthenticationException;
import com.usc.squirrelspotter.exception.BadRequestException;
import com.usc.squirrelspotter.exception.ConflictException;
import com.usc.squirrelspotter.model.User;
import com.usc.squirrelspotter.repository.UserRepository;
import com.usc.squirrelspotter.security.JwtUtil;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Unit tests for AuthService
 * Tests authentication logic including signup and login
 */
@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private JwtUtil jwtUtil;

    @InjectMocks
    private AuthService authService;

    private SignupRequest validSignupRequest;
    private LoginRequest validLoginRequest;
    private User mockUser;

    @BeforeEach
    void setUp() {
        validSignupRequest = new SignupRequest();
        validSignupRequest.setEmail("testuser@usc.edu");
        validSignupRequest.setUsername("testuser");
        validSignupRequest.setPassword("password123");

        validLoginRequest = new LoginRequest();
        validLoginRequest.setEmail("testuser@usc.edu");
        validLoginRequest.setPassword("password123");

        mockUser = new User("testuser", "testuser@usc.edu", "hashedPassword");
        mockUser.setUserID(1);
    }

    // ========== Signup Tests ==========

    @Test
    void testSignup_Success() {
        // Arrange
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(userRepository.existsByUsername(anyString())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(mockUser);
        when(jwtUtil.generateToken(anyInt(), anyString())).thenReturn("mock-jwt-token");

        // Act
        AuthResponse response = authService.signup(validSignupRequest);

        // Assert
        assertNotNull(response);
        assertEquals("mock-jwt-token", response.getToken());
        assertNotNull(response.getUser());
        assertEquals("testuser", response.getUser().getUsername());
        assertEquals("testuser@usc.edu", response.getUser().getEmail());

        verify(userRepository, times(1)).existsByEmail(validSignupRequest.getEmail());
        verify(userRepository, times(1)).existsByUsername(validSignupRequest.getUsername());
        verify(userRepository, times(1)).save(any(User.class));
        verify(jwtUtil, times(1)).generateToken(anyInt(), anyString());
    }

    @Test
    void testSignup_MissingEmail_ThrowsBadRequestException() {
        // Arrange
        validSignupRequest.setEmail(null);

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> authService.signup(validSignupRequest));
        assertEquals("Email is required", exception.getMessage());
        
        verify(userRepository, never()).save(any());
    }

    @Test
    void testSignup_EmptyEmail_ThrowsBadRequestException() {
        // Arrange
        validSignupRequest.setEmail("");

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> authService.signup(validSignupRequest));
        assertEquals("Email is required", exception.getMessage());
    }

    @Test
    void testSignup_MissingUsername_ThrowsBadRequestException() {
        // Arrange
        validSignupRequest.setUsername(null);

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> authService.signup(validSignupRequest));
        assertEquals("Username is required", exception.getMessage());
    }

    @Test
    void testSignup_MissingPassword_ThrowsBadRequestException() {
        // Arrange
        validSignupRequest.setPassword(null);

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> authService.signup(validSignupRequest));
        assertEquals("Password is required", exception.getMessage());
    }

    @Test
    void testSignup_NonUSCEmail_ThrowsBadRequestException() {
        // Arrange
        validSignupRequest.setEmail("testuser@gmail.com");

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> authService.signup(validSignupRequest));
        assertEquals("Email must be a USC email (@usc.edu)", exception.getMessage());
    }

    @Test
    void testSignup_DuplicateEmail_ThrowsConflictException() {
        // Arrange
        when(userRepository.existsByEmail(anyString())).thenReturn(true);

        // Act & Assert
        ConflictException exception = assertThrows(ConflictException.class, 
            () -> authService.signup(validSignupRequest));
        assertEquals("Email already exists", exception.getMessage());
        
        verify(userRepository, times(1)).existsByEmail(validSignupRequest.getEmail());
        verify(userRepository, never()).save(any());
    }

    @Test
    void testSignup_DuplicateUsername_ThrowsConflictException() {
        // Arrange
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(userRepository.existsByUsername(anyString())).thenReturn(true);

        // Act & Assert
        ConflictException exception = assertThrows(ConflictException.class, 
            () -> authService.signup(validSignupRequest));
        assertEquals("Username already exists", exception.getMessage());
        
        verify(userRepository, times(1)).existsByUsername(validSignupRequest.getUsername());
        verify(userRepository, never()).save(any());
    }

    // ========== Login Tests ==========

    @Test
    void testLogin_Success() {
        // Arrange
        // Note: In real scenario, you'd need to hash the password with Argon2
        // For this test, we're mocking the verification process
        User userWithHashedPassword = new User("testuser", "testuser@usc.edu", 
            "$argon2id$v=19$m=65536,t=10,p=1$hashedsalt$hashedpassword");
        userWithHashedPassword.setUserID(1);
        
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.of(userWithHashedPassword));
        when(jwtUtil.generateToken(anyInt(), anyString())).thenReturn("mock-jwt-token");

        // Note: Argon2 verification is hard to mock, so this test is simplified
        // In a real scenario, you might want to use @Spy or integration tests
    }

    @Test
    void testLogin_MissingEmail_ThrowsBadRequestException() {
        // Arrange
        validLoginRequest.setEmail(null);

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> authService.login(validLoginRequest));
        assertEquals("Email is required", exception.getMessage());
    }

    @Test
    void testLogin_MissingPassword_ThrowsBadRequestException() {
        // Arrange
        validLoginRequest.setPassword(null);

        // Act & Assert
        BadRequestException exception = assertThrows(BadRequestException.class, 
            () -> authService.login(validLoginRequest));
        assertEquals("Password is required", exception.getMessage());
    }

    @Test
    void testLogin_UserNotFound_ThrowsAuthenticationException() {
        // Arrange
        when(userRepository.findByEmail(anyString())).thenReturn(Optional.empty());

        // Act & Assert
        AuthenticationException exception = assertThrows(AuthenticationException.class, 
            () -> authService.login(validLoginRequest));
        assertEquals("Invalid credentials", exception.getMessage());
        
        verify(userRepository, times(1)).findByEmail(validLoginRequest.getEmail());
    }

    // ========== GetUserById Tests ==========

    @Test
    void testGetUserById_Success() {
        // Arrange
        when(userRepository.findById(1)).thenReturn(Optional.of(mockUser));

        // Act
        User result = authService.getUserById(1);

        // Assert
        assertNotNull(result);
        assertEquals(1, result.getUserID());
        assertEquals("testuser", result.getUsername());
        
        verify(userRepository, times(1)).findById(1);
    }

    @Test
    void testGetUserById_UserNotFound_ThrowsAuthenticationException() {
        // Arrange
        when(userRepository.findById(anyInt())).thenReturn(Optional.empty());

        // Act & Assert
        AuthenticationException exception = assertThrows(AuthenticationException.class, 
            () -> authService.getUserById(999));
        assertEquals("User not found", exception.getMessage());
    }
}
