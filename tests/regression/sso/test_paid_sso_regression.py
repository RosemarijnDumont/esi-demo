
import pytest
from unittest.mock import patch, MagicMock

# Assuming existing SSO modules for paid accounts
from app.sso.auth import SSOAuthenticator
from app.sso.config import SSOConfigManager
from app.accounts.models import Account, AccountType
from app.users.models import User

@pytest.fixture
def paid_account_existing_sso():
    account = Account(account_id="paid-existing-sso-789", account_type=AccountType.PAID, name="Existing Paid SSO User")
    account.sso_enabled = True
    account.sso_config = {"idp_entity_id": "http://existing-idp.com", "login_url": "http://existing-idp.com/login"}
    return account

@pytest.fixture
def sso_authenticator():
    return SSOAuthenticator()

@pytest.fixture
def sso_config_manager():
    return SSOConfigManager()

def test_paid_account_existing_sso_authentication_regression(sso_authenticator, paid_account_existing_sso):
    """Regression test: Ensure existing paid account SSO authentication still functions."""
    with patch('app.sso.auth.SAMLIdentityProvider.authenticate', return_value={"email": "existing@paid.com", "name": "Existing Paid User"}), \
         patch('app.sso.auth.UserManagementService.get_or_create_user', return_value=User(user_id="paid-user-789", email="existing@paid.com")):
        
        user = sso_authenticator.authenticate_sso(paid_account_existing_sso, "saml_response_data")
        assert user is not None
        assert user.email == "existing@paid.com"

def test_paid_account_existing_sso_config_update_regression(sso_config_manager, paid_account_existing_sso):
    """Regression test: Ensure existing paid account SSO configuration can still be updated."""
    new_idp_metadata = {"idp_entity_id": "http://new-existing-idp.com", "login_url": "http://new-existing-idp.com/login"}
    with patch('app.sso.config.SSOConfigManager._save_sso_config') as mock_save_config,
         patch('app.identity.providers.IdentityProvider.validate_metadata', return_value=True):
        
        sso_config_manager.configure_sso(paid_account_existing_sso, "new_saml_config_data", new_idp_metadata)
        mock_save_config.assert_called_once_with(paid_account_existing_sso.account_id, "new_saml_config_data", new_idp_metadata)
        # Optionally, verify the account's sso_config was updated if _save_sso_config modifies it in place

def test_paid_account_sso_disable_regression(sso_config_manager, paid_account_existing_sso):
    """Regression test: Ensure SSO can be disabled for an existing paid account."""
    with patch('app.sso.config.SSOConfigManager._disable_sso_config') as mock_disable_config:
        sso_config_manager.disable_sso(paid_account_existing_sso)
        mock_disable_config.assert_called_once_with(paid_account_existing_sso.account_id)
