package com.usc.squirrelspotter.dto;

public class ErrorResponse {
    private String message;

    // Constructors
    public ErrorResponse() {}

    public ErrorResponse(String message) {
        this.message = message;
    }

    // Getters and Setters
    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
