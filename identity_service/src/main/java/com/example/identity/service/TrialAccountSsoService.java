package com.example.identity.service;

import com.example.identity.model.TrialAccount;
import com.example.identity.repository.TrialAccountRepository;
import com.example.identity.sso.SAMLServiceProvider;
import com.example.identity.sso.SAMLConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.opensaml.saml2.metadata.provider.MetadataProviderException;
import org.opensaml.xml.parse.XMLParserException;

import java.util.Optional;

@Service
public class TrialAccountSsoService {

    @Autowired
    private TrialAccountRepository trialAccountRepository;

    @Autowired
    private SAMLServiceProvider samlServiceProvider;

    public void configureSamlForTrialAccount(Long accountId, SAMLConfig samlConfig) throws MetadataProviderException, XMLParserException {
        Optional<TrialAccount> optionalTrialAccount = trialAccountRepository.findById(accountId);
        if (optionalTrialAccount.isPresent()) {
            TrialAccount trialAccount = optionalTrialAccount.get();
            trialAccount.setSsoEnabled(true);
            trialAccount.setSamlConfig(samlConfig);
            trialAccountRepository.save(trialAccount);
            samlServiceProvider.registerServiceProvider(accountId.toString(), samlConfig);
        } else {
            throw new IllegalArgumentException("Trial account not found with ID: " + accountId);
        }
    }

    public Optional<SAMLConfig> getSamlConfigForTrialAccount(Long accountId) {
        return trialAccountRepository.findById(accountId)
                .filter(TrialAccount::isSsoEnabled)
                .map(TrialAccount::getSamlConfig);
    }

    public boolean isSsoEnabledForTrialAccount(Long accountId) {
        return trialAccountRepository.findById(accountId)
                .map(TrialAccount::isSsoEnabled)
                .orElse(false);
    }
}
