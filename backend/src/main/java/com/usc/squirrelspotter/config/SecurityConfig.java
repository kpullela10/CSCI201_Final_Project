package com.usc.squirrelspotter.config;

import com.usc.squirrelspotter.security.JwtAuthenticationFilter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private JwtAuthenticationFilter jwtAuthenticationFilter;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                // Disable CSRF (not needed for stateless JWT authentication)
                .csrf(csrf -> csrf.disable())

                // Configure CORS (will use CorsConfig)
                .cors(cors -> {})

                // Set session management to stateless
                .sessionManagement(session ->
                        session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))

                // Configure authorization rules
                .authorizeHttpRequests(auth -> auth
                        // Public endpoints (no authentication required)
                        .requestMatchers("/api/auth/**").permitAll()
                        .requestMatchers("/api/pins/weekly").permitAll()  // Public: view weekly pins
                        .requestMatchers("/api/pins/{pinID}").permitAll()  // Public: view pin details
                        .requestMatchers("/api/leaderboard").permitAll()  // Public: view leaderboard
                        .requestMatchers("/api/users/{userID}/pins").permitAll()  // Public: view user pins
                        .requestMatchers("/ws/**").permitAll()  // Public: WebSocket (Pin/Maps team)

                        // Protected endpoints (authentication required)
                        .requestMatchers("/api/pins/my").authenticated()  // Protected: get my pins
                        .requestMatchers("/api/pins").authenticated()  // Protected: create pin

                        // All other requests require authentication
                        .anyRequest().authenticated()
                )

                // Add JWT filter before Spring Security's authentication filter
                .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
