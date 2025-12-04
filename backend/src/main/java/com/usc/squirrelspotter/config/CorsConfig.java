package com.usc.squirrelspotter.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

@Configuration
public class CorsConfig {

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();

        // Allow frontend origins
        configuration.setAllowedOriginPatterns(Arrays.asList(
                "http://localhost:*",      // Localhost any port
                "http://127.0.0.1:*",      // Localhost IP any port
                "http://10.*.*.*:*",       // Local network 10.x.x.x
                "http://192.168.*.*:*",    // Local network 192.168.x.x
                "https://*.vercel.app",    // Vercel deployments
                "https://*.railway.app"    // Railway deployments
        ));

        // Allow standard HTTP methods
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"));

        // Allow common headers
        configuration.setAllowedHeaders(Arrays.asList(
                "Authorization",
                "Content-Type",
                "Accept",
                "Origin",
                "X-Requested-With"
        ));

        // Allow credentials (cookies, authorization headers)
        configuration.setAllowCredentials(true);

        // Expose Authorization header to frontend
        configuration.setExposedHeaders(Arrays.asList("Authorization"));

        // Cache preflight response for 1 hour
        configuration.setMaxAge(3600L);

        // Apply CORS configuration to all endpoints
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);

        return source;
    }
}
