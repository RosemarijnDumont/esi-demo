package com.example.identity.controller;

import com.example.identity.service.TrialAccountSsoService;
import com.example.identity.sso.SAMLConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.opensaml.saml2.metadata.provider.MetadataProviderException;
import org.opensaml.xml.parse.XMLParserException;

import java.util.Optional;

@RestController
@RequestMapping("/api/trial-accounts/{accountId}/sso")
public class TrialAccountSsoController {

    @Autowired
    private TrialAccountSsoService trialAccountSsoService;

    @PostMapping
    public ResponseEntity<?> configureTrialAccountSso(@PathVariable Long accountId, @RequestBody SAMLConfig samlConfig) {
        try {
            trialAccountSsoService.configureSamlForTrialAccount(accountId, samlConfig);
            return ResponseEntity.ok().build();
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(e.getMessage());
        } catch (MetadataProviderException | XMLParserException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error configuring SAML: " + e.getMessage());
        }
    }

    @GetMapping
    public ResponseEntity<SAMLConfig> getTrialAccountSsoConfig(@PathVariable Long accountId) {
        Optional<SAMLConfig> samlConfig = trialAccountSsoService.getSamlConfigForTrialAccount(accountId);
        return samlConfig.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping("/enabled")
    public ResponseEntity<Boolean> isSsoEnabledForTrialAccount(@PathVariable Long accountId) {
        boolean isEnabled = trialAccountSsoService.isSsoEnabledForTrialAccount(accountId);
        return ResponseEntity.ok(isEnabled);
    }
}
