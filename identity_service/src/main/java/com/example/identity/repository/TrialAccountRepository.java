package com.example.identity.repository;

import com.example.identity.model.TrialAccount;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TrialAccountRepository extends JpaRepository<TrialAccount, Long> {
}
