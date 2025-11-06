package com.clientonboarding.portal.exception;

public class ApplicationSubmissionException extends Exception {
    public ApplicationSubmissionException(String message) {
        super(message);
    }

    public ApplicationSubmissionException(String message, Throwable cause) {
        super(message, cause);
    }
}
