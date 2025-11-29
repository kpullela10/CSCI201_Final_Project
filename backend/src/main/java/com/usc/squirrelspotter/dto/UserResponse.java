package com.usc.squirrelspotter.dto;

public class UserResponse {
    private Integer userID;
    private String username;
    private String email;

    // Constructors
    public UserResponse() {}

    public UserResponse(Integer userID, String username, String email) {
        this.userID = userID;
        this.username = username;
        this.email = email;
    }

    // Getters and Setters
    public Integer getUserID() {
        return userID;
    }

    public void setUserID(Integer userID) {
        this.userID = userID;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
