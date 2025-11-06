package com.clientonboarding.portal.repository;

import com.clientonboarding.portal.model.Application;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ApplicationRepository extends JpaRepository<Application, Long> {
    // Custom queries can be added here if needed
}
