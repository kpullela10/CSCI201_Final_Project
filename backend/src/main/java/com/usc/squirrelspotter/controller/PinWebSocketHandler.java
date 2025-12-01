package com.usc.squirrelspotter.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.usc.squirrelspotter.dto.PinResponse;
import com.usc.squirrelspotter.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.net.URI;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * Plain WebSocket handler for real-time pin updates
 */
@Component
public class PinWebSocketHandler extends TextWebSocketHandler {

    private final List<WebSocketSession> sessions = new CopyOnWriteArrayList<>();
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Autowired
    private JwtUtil jwtUtil;

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        // Extract token from query string
        URI uri = session.getUri();
        if (uri != null) {
            String query = uri.getQuery();
            if (query != null && query.contains("token=")) {
                String token = query.substring(query.indexOf("token=") + 6);
                // Remove any additional query parameters
                if (token.contains("&")) {
                    token = token.substring(0, token.indexOf("&"));
                }
                
                // Validate token (optional - allow connections without valid tokens for public viewing)
                // Store session regardless, but you could add user info to session attributes
                if (jwtUtil.validateToken(token) && !jwtUtil.isTokenExpired(token)) {
                    try {
                        Integer userID = jwtUtil.getUserIdFromToken(token);
                        session.getAttributes().put("userID", userID);
                    } catch (Exception e) {
                        // Token invalid, but allow connection for public viewing
                    }
                }
            }
        }
        
        sessions.add(session);
        System.out.println("WebSocket connection established. Session ID: " + session.getId() + ", Total connections: " + sessions.size());
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        sessions.remove(session);
        System.out.println("WebSocket connection closed. Session ID: " + session.getId() + ", Total connections: " + sessions.size());
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        // Handle incoming messages if needed
        // For now, we only broadcast from server, so this can be empty
    }

    /**
     * Broadcast a new pin to all connected clients
     */
    public void broadcastPin(PinResponse pin) {
        String message;
        try {
            message = objectMapper.writeValueAsString(pin);
        } catch (Exception e) {
            System.err.println("Failed to serialize pin: " + e.getMessage());
            return;
        }

        TextMessage textMessage = new TextMessage(message);
        for (WebSocketSession session : sessions) {
            try {
                if (session.isOpen()) {
                    session.sendMessage(textMessage);
                }
            } catch (IOException e) {
                System.err.println("Failed to send message to session " + session.getId() + ": " + e.getMessage());
            }
        }
    }

    /**
     * Broadcast multiple pins to all connected clients
     */
    public void broadcastPins(List<PinResponse> pins) {
        String message;
        try {
            message = objectMapper.writeValueAsString(pins);
        } catch (Exception e) {
            System.err.println("Failed to serialize pins: " + e.getMessage());
            return;
        }

        TextMessage textMessage = new TextMessage(message);
        for (WebSocketSession session : sessions) {
            try {
                if (session.isOpen()) {
                    session.sendMessage(textMessage);
                }
            } catch (IOException e) {
                System.err.println("Failed to send message to session " + session.getId() + ": " + e.getMessage());
            }
        }
    }
}

