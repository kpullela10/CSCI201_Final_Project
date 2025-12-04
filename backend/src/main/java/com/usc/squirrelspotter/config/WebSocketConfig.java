package com.usc.squirrelspotter.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

import com.usc.squirrelspotter.controller.PinWebSocketHandler;

/**
 * Plain WebSocket configuration (no STOMP)
 */
@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    private final PinWebSocketHandler pinWebSocketHandler;

    public WebSocketConfig(PinWebSocketHandler pinWebSocketHandler) {
        this.pinWebSocketHandler = pinWebSocketHandler;
    }

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        // Register plain WebSocket endpoint
        registry.addHandler(pinWebSocketHandler, "/ws/pins")
                .setAllowedOriginPatterns(
                    "http://localhost:5173",
                    "http://localhost:3000",
                    "https://*.vercel.app",
                    "https://*.railway.app"
                );
    }
}
