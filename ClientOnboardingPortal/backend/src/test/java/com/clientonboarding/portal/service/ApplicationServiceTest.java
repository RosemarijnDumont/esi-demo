package com.clientonboarding.portal.service;

import com.clientonboarding.portal.model.Application;
import com.clientonboarding.portal.repository.ApplicationRepository;
import com.clientonboarding.portal.exception.ApplicationSubmissionException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;
import java.time.LocalDateTime;

public class ApplicationServiceTest {

    @Mock
    private ApplicationRepository applicationRepository;

    @InjectMocks
    private ApplicationService applicationService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void submitApplication_Success() throws ApplicationSubmissionException {
        Application application = new Application();
        application.setClientId("CL001");
        application.setFirstName("John");
        application.setLastName("Doe");
        application.setEmail("john.doe@example.com");
        application.setPhoneNumber("1234567890");
        application.setAddress("123 Main St");
        application.setIdVerificationStatus("VERIFIED");
        application.setSubmissionDate(LocalDateTime.now());

        when(applicationRepository.save(any(Application.class))).thenReturn(application);

        Application result = applicationService.submitApplication(application);

        assertNotNull(result);
        assertEquals("CL001", result.getClientId());
        verify(applicationRepository, times(1)).save(application);
    }

    @Test
    void submitApplication_ValidationFailure_BlankFirstName() {
        Application application = new Application();
        application.setClientId("CL002");
        application.setFirstName(""); // Invalid
        application.setLastName("Doe");
        application.setEmail("john.doe@example.com");
        application.setPhoneNumber("1234567890");
        application.setAddress("123 Main St");
        application.setIdVerificationStatus("VERIFIED");
        application.setSubmissionDate(LocalDateTime.now());

        Exception exception = assertThrows(ApplicationSubmissionException.class, () -> {
            applicationService.submitApplication(application);
        });

        assertTrue(exception.getMessage().contains("Validation failed"));
        assertTrue(exception.getMessage().contains("firstName cannot be empty"));
        verify(applicationRepository, never()).save(any(Application.class));
    }
    
    @Test
    void submitApplication_ValidationFailure_InvalidEmail() {
        Application application = new Application();
        application.setClientId("CL003");
        application.setFirstName("Jane");
        application.setLastName("Smith");
        application.setEmail("invalid-email"); // Invalid
        application.setPhoneNumber("1234567890");
        application.setAddress("456 Oak Ave");
        application.setIdVerificationStatus("VERIFIED");
        application.setSubmissionDate(LocalDateTime.now());

        Exception exception = assertThrows(ApplicationSubmissionException.class, () -> {
            applicationService.submitApplication(application);
        });

        assertTrue(exception.getMessage().contains("Validation failed"));
        assertTrue(exception.getMessage().contains("email should be valid"));
        verify(applicationRepository, never()).save(any(Application.class));
    }

    @Test
    void submitApplication_IdVerificationNotVerified() {
        Application application = new Application();
        application.setClientId("CL004");
        application.setFirstName("Peter");
        application.setLastName("Jones");
        application.setEmail("peter.jones@example.com");
        application.setPhoneNumber("1234567890");
        application.setAddress("789 Pine Rd");
        application.setIdVerificationStatus("PENDING"); // Not VERIFIED
        application.setSubmissionDate(LocalDateTime.now());

        Exception exception = assertThrows(ApplicationSubmissionException.class, () -> {
            applicationService.submitApplication(application);
        });

        assertTrue(exception.getMessage().contains("ID verification required or failed."));
        verify(applicationRepository, never()).save(any(Application.class));
    }

    @Test
    void submitApplication_RepositoryThrowsException() {
        Application application = new Application();
        application.setClientId("CL005");
        application.setFirstName("Alice");
        application.setLastName("Brown");
        application.setEmail("alice.brown@example.com");
        application.setPhoneNumber("1234567890");
        application.setAddress("101 Elm Dr");
        application.setIdVerificationStatus("VERIFIED");
        application.setSubmissionDate(LocalDateTime.now());

        when(applicationRepository.save(any(Application.class))).thenThrow(new RuntimeException("Database Error"));

        Exception exception = assertThrows(ApplicationSubmissionException.class, () -> {
            applicationService.submitApplication(application);
        });

        assertTrue(exception.getMessage().contains("Failed to submit application due to an internal error."));
        verify(applicationRepository, times(1)).save(application);
    }
}
