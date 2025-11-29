package com.usc.squirrelspotter.service;

import com.usc.squirrelspotter.dto.*;
import com.usc.squirrelspotter.exception.AuthenticationException;
import com.usc.squirrelspotter.exception.BadRequestException;
import com.usc.squirrelspotter.exception.ConflictException;
import com.usc.squirrelspotter.model.User;
import com.usc.squirrelspotter.repository.UserRepository;
import com.usc.squirrelspotter.security.JwtUtil;
import de.mkammerer.argon2.Argon2;
import de.mkammerer.argon2.Argon2Factory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JwtUtil jwtUtil;

    private final Argon2 argon2 = Argon2Factory.create();

    /**
     * Register a new user (signup)
     */
    public AuthResponse signup(SignupRequest request) {
        // Validate input
        if (request.getEmail() == null || request.getEmail().isEmpty()) {
            throw new BadRequestException("Email is required");
        }
        if (request.getUsername() == null || request.getUsername().isEmpty()) {
            throw new BadRequestException("Username is required");
        }
        if (request.getPassword() == null || request.getPassword().isEmpty()) {
            throw new BadRequestException("Password is required");
        }

        // Validate USC email
        if (!request.getEmail().contains("@usc.edu")) {
            throw new BadRequestException("Email must be a USC email (@usc.edu)");
        }

        // Check if email already exists
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new ConflictException("Email already exists");
        }

        // Check if username already exists
        if (userRepository.existsByUsername(request.getUsername())) {
            throw new ConflictException("Username already exists");
        }

        // Hash password using Argon2
        String passwordHash = argon2.hash(10, 65536, 1, request.getPassword().toCharArray());

        // Create new user
        User user = new User(request.getUsername(), request.getEmail(), passwordHash);
        user = userRepository.save(user);

        // Generate JWT token
        String token = jwtUtil.generateToken(user.getUserID(), user.getEmail());

        // Create response
        UserResponse userResponse = new UserResponse(
                user.getUserID(),
                user.getUsername(),
                user.getEmail()
        );

        return new AuthResponse(token, userResponse);
    }

    /**
     * Login an existing user
     */
    public AuthResponse login(LoginRequest request) {
        // Validate input
        if (request.getEmail() == null || request.getEmail().isEmpty()) {
            throw new BadRequestException("Email is required");
        }
        if (request.getPassword() == null || request.getPassword().isEmpty()) {
            throw new BadRequestException("Password is required");
        }

        // Find user by email
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new AuthenticationException("Invalid credentials"));

        // Verify password using Argon2
        boolean passwordMatches = argon2.verify(user.getPasswordHash(), request.getPassword().toCharArray());

        if (!passwordMatches) {
            throw new AuthenticationException("Invalid credentials");
        }

        // Generate JWT token
        String token = jwtUtil.generateToken(user.getUserID(), user.getEmail());

        // Create response
        UserResponse userResponse = new UserResponse(
                user.getUserID(),
                user.getUsername(),
                user.getEmail()
        );

        return new AuthResponse(token, userResponse);
    }

    /**
     * Get user by ID (for protected endpoints)
     */
    public User getUserById(Integer userID) {
        return userRepository.findById(userID)
                .orElseThrow(() -> new AuthenticationException("User not found"));
    }
}
