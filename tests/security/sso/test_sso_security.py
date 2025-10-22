
import pytest
from unittest.mock import MagicMock, patch

# Assuming relevant security components and SSO modules
from app.sso.auth import SSOAuthenticator
from app.accounts.models import Account, AccountType
from app.security.encryption import decrypt_saml_assertion

@pytest.fixture
def sso_authenticator():
    return SSOAuthenticator()

@pytest.fixture
def trial_account_with_sso():
    account = Account(account_id="trial-sso-sec-123", account_type=AccountType.TRIAL, name="Trial SSO Security User")
    account.sso_enabled = True
    account.sso_config = {"idp_entity_id": "http://mock-idp.com", "login_url": "http://mock-idp.com/login"}
    return account

def test_saml_response_signature_validation(sso_authenticator, trial_account_with_sso):
    """Security test: Ensure SAML responses are properly validated for signature."""
    # Simulate a SAML response with an invalid signature
    malicious_saml_response = "<saml:Response InvalidSignature='true'></saml:Response>"
    
    with patch('app.sso.auth.SAMLIdentityProvider.validate_saml_signature', return_value=False):
        with pytest.raises(SecurityError, match="Invalid SAML response signature."):
            sso_authenticator.authenticate_sso(trial_account_with_sso, malicious_saml_response)

def test_saml_response_replay_attack_prevention(sso_authenticator, trial_account_with_sso):
    """Security test: Ensure SAML responses cannot be replayed."""
    # Simulate a valid SAML response that has already been processed
    replayed_saml_response = "<saml:Response ID='_replayed_id'></saml:Response>"

    with patch('app.sso.auth.SAMLIdentityProvider.validate_saml_signature', return_value=True),
         patch('app.sso.auth.SAMLIdentityProvider.is_saml_response_replayed', return_value=True):
        with pytest.raises(SecurityError, match="Replayed SAML response detected."):
            sso_authenticator.authenticate_sso(trial_account_with_sso, replayed_saml_response)

def test_saml_encryption_decryption(sso_authenticator, trial_account_with_sso):
    """Security test: Verify SAML assertions are encrypted and decrypted correctly."""
    encrypted_assertion = "encrypted_assertion_data"
    decrypted_assertion_content = {"email": "secure@trial.com"}

    # Mock the decryption process
    with patch('app.security.encryption.decrypt_saml_assertion', return_value=decrypted_assertion_content),
         patch('app.sso.auth.SAMLIdentityProvider.authenticate', return_value=decrypted_assertion_content),
         patch('app.sso.auth.UserManagementService.get_or_create_user', return_value=MagicMock()):
        
        # In a real scenario, the IdP would return an encrypted assertion, and our system would decrypt it.
        # This test focuses on the decryption logic.
        sso_authenticator.authenticate_sso(trial_account_with_sso, encrypted_assertion)
        decrypt_saml_assertion.assert_called_once_with(encrypted_assertion)

# Define a custom SecurityError if not already defined in the application
class SecurityError(Exception):
    pass
