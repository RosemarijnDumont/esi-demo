package com.clientonboarding.portal.controller;

import com.clientonboarding.portal.model.Application;
import com.clientonboarding.portal.service.ApplicationService;
import com.clientonboarding.portal.exception.ApplicationSubmissionException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import javax.validation.Valid;

@RestController
@RequestMapping("/api/applications")
public class ApplicationController {

    private static final Logger logger = LoggerFactory.getLogger(ApplicationController.class);

    @Autowired
    private ApplicationService applicationService;

    @PostMapping("/submit")
    public ResponseEntity<?> submitApplication(@Valid @RequestBody Application application) {
        logger.info("Received application submission request for client: {}", application.getClientId());
        try {
            Application submittedApplication = applicationService.submitApplication(application);
            return new ResponseEntity<>(submittedApplication, HttpStatus.CREATED);
        } catch (ApplicationSubmissionException e) {
            logger.error("Application submission failed: {}", e.getMessage(), e);
            return new ResponseEntity<>(e.getMessage(), HttpStatus.BAD_REQUEST); // 400 for client-side errors
        } catch (Exception e) {
            logger.error("An unexpected error occurred during application submission: {}", e.getMessage(), e);
            return new ResponseEntity<>("An internal server error occurred.", HttpStatus.INTERNAL_SERVER_ERROR); // 500 for unexpected errors
        }
    }
}
