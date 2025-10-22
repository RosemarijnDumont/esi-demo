
import pytest
from unittest.mock import MagicMock, patch

# Assuming these are the modules involved in the SSO authentication flow
from app.sso.auth import SSOAuthenticator
from app.accounts.models import Account, AccountType
from app.users.models import User

@pytest.fixture
def sso_authenticator():
    return SSOAuthenticator()

@pytest.fixture
def trial_account_with_sso():
    account = Account(account_id="trial-sso-123", account_type=AccountType.TRIAL, name="Trial SSO User")
    # Simulate SSO configuration being present
    account.sso_enabled = True
    account.sso_config = {"idp_entity_id": "http://mock-idp.com", "login_url": "http://mock-idp.com/login"}
    return account

@pytest.fixture
def paid_account_with_sso():
    account = Account(account_id="paid-sso-456", account_type=AccountType.PAID, name="Paid SSO User")
    # Simulate SSO configuration being present
    account.sso_enabled = True
    account.sso_config = {"idp_entity_id": "http://mock-idp.com", "login_url": "http://mock-idp.com/login"}
    return account

def test_trial_account_sso_authentication_success(sso_authenticator, trial_account_with_sso):
    """Test successful SSO authentication for a trial account."""
    with patch('app.sso.auth.SAMLIdentityProvider.authenticate', return_value={"email": "user@trial.com", "name": "Trial User"}), \
         patch('app.sso.auth.UserManagementService.get_or_create_user', return_value=User(user_id="trial-user-1", email="user@trial.com")):
        
        user = sso_authenticator.authenticate_sso(trial_account_with_sso, "saml_response_data")
        assert user is not None
        assert user.email == "user@trial.com"

def test_paid_account_sso_authentication_success(sso_authenticator, paid_account_with_sso):
    """Test successful SSO authentication for a paid account."""
    with patch('app.sso.auth.SAMLIdentityProvider.authenticate', return_value={"email": "user@paid.com", "name": "Paid User"}), \
         patch('app.sso.auth.UserManagementService.get_or_create_user', return_value=User(user_id="paid-user-1", email="user@paid.com")):
        
        user = sso_authenticator.authenticate_sso(paid_account_with_sso, "saml_response_data")
        assert user is not None
        assert user.email == "user@paid.com"

def test_sso_authentication_failure_invalid_response(sso_authenticator, trial_account_with_sso):
    """Test SSO authentication failure with an invalid SAML response."""
    with patch('app.sso.auth.SAMLIdentityProvider.authenticate', return_value=None):
        with pytest.raises(ValueError, match="SSO authentication failed."):
            sso_authenticator.authenticate_sso(trial_account_with_sso, "invalid_saml_response")

def test_sso_authentication_account_sso_disabled(sso_authenticator):
    """Test SSO authentication when SSO is not enabled for the account."""
    account = Account(account_id="no-sso-123", account_type=AccountType.TRIAL, name="No SSO User")
    account.sso_enabled = False

    with pytest.raises(PermissionError, match="SSO is not enabled for this account."):
        sso_authenticator.authenticate_sso(account, "saml_response")