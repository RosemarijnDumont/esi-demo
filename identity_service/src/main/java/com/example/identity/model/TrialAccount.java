package com.example.identity.model;

import com.example.identity.sso.SAMLConfig;
import javax.persistence.*;

@Entity
public class TrialAccount {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private boolean ssoEnabled;

    @Embedded
    private SAMLConfig samlConfig;

    // Getters and setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public boolean isSsoEnabled() {
        return ssoEnabled;
    }

    public void setSsoEnabled(boolean ssoEnabled) {
        this.ssoEnabled = ssoEnabled;
    }

    public SAMLConfig getSamlConfig() {
        return samlConfig;
    }

    public void setSamlConfig(SAMLConfig samlConfig) {
        this.samlConfig = samlConfig;
    }
}
