package com.example.identity.sso;

import javax.persistence.Embeddable;
import javax.persistence.Column;

@Embeddable
public class SAMLConfig {

    @Column(columnDefinition = "TEXT")
    private String idpMetadataUrl;
    @Column(columnDefinition = "TEXT")
    private String entityId;
    @Column(columnDefinition = "TEXT")
    private String acsUrl;

    // Getters and setters

    public String getIdpMetadataUrl() {
        return idpMetadataUrl;
    }

    public void setIdpMetadataUrl(String idpMetadataUrl) {
        this.idpMetadataUrl = idpMetadataUrl;
    }

    public String getEntityId() {
        return entityId;
    }

    public void setEntityId(String entityId) {
        this.entityId = entityId;
    }

    public String getAcsUrl() {
        return acsUrl;
    }

    public void setAcsUrl(String acsUrl) {
        this.acsUrl = acsUrl;
    }
}
