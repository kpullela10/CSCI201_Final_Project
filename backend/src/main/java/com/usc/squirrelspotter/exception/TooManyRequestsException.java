package com.usc.squirrelspotter.exception;

/**
 * Exception for rate limiting (HTTP 429)
 */
public class TooManyRequestsException extends RuntimeException {
    public TooManyRequestsException(String message) {
        super(message);
    }
}

