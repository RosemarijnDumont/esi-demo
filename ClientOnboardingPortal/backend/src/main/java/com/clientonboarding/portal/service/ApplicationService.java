package com.clientonboarding.portal.service;

import com.clientonboarding.portal.model.Application;
import com.clientonboarding.portal.repository.ApplicationRepository;
import com.clientonboarding.portal.exception.ApplicationSubmissionException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import java.util.Set;

@Service
public class ApplicationService {

    private static final Logger logger = LoggerFactory.getLogger(ApplicationService.class);

    @Autowired
    private ApplicationRepository applicationRepository;

    private final Validator validator = Validation.buildDefaultValidatorFactory().getValidator();

    @Transactional
    public Application submitApplication(Application application) throws ApplicationSubmissionException {
        logger.info("Attempting to submit application for client: {}", application.getClientId());

        // 1. Server-side input validation
        Set<ConstraintViolation<Application>> violations = validator.validate(application);
        if (!violations.isEmpty()) {
            StringBuilder sb = new StringBuilder();
            for (ConstraintViolation<Application> violation : violations) {
                sb.append(violation.getPropertyPath()).append(" ").append(violation.getMessage()).append(". ");
            }
            logger.error("Application validation failed for client {}: {}", application.getClientId(), sb.toString());
            throw new ApplicationSubmissionException("Validation failed: " + sb.toString());
        }

        try {
            // 2. Placeholder for ID verification callback processing (if asynchronous)
            // Assuming ID verification status is updated prior to this submission or checked synchronously here.
            // For this fix, we assume ID verification status is part of the 'application' object or confirmed.
            if (application.getIdVerificationStatus() == null || !"VERIFIED".equals(application.getIdVerificationStatus())) {
                logger.error("ID verification not completed or failed for client {}. Status: {}", 
                             application.getClientId(), application.getIdVerificationStatus());
                throw new ApplicationSubmissionException("ID verification required or failed.");
            }
            
            // 3. Robust form processing and database transaction handling
            // If there's any specific complex logic, it would go here.
            // We ensure all database operations within this method are part of a single transaction.
            Application savedApplication = applicationRepository.save(application);
            logger.info("Application submitted successfully for client: {}", application.getClientId());
            return savedApplication;
        } catch (Exception e) {
            logger.error("Error submitting application for client {}: {}", application.getClientId(), e.getMessage(), e);
            // Re-throwing a custom exception provides a more controlled error message to the frontend
            throw new ApplicationSubmissionException("Failed to submit application due to an internal error.", e);
        }
    }
}
