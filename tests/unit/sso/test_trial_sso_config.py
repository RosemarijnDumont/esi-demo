
import pytest
from unittest.mock import MagicMock, patch

# Assuming these are the modules that will be modified for SSO configuration
# and trial account management.
# These would need to be created based on the actual implementation.
from app.sso.config import SSOConfigManager
from app.accounts.models import Account, AccountType
from app.identity.providers import IdentityProvider

@pytest.fixture
def sso_config_manager():
    return SSOConfigManager()

@pytest.fixture
def trial_account():
    return Account(account_id="trial-123", account_type=AccountType.TRIAL, name="Trial User")

@pytest.fixture
def paid_account():
    return Account(account_id="paid-456", account_type=AccountType.PAID, name="Paid User")

@pytest.fixture
def mock_idp_metadata():
    return {"idp_entity_id": "http://mock-idp.com", "login_url": "http://mock-idp.com/login"}

def test_configure_sso_for_trial_account_success(sso_config_manager, trial_account, mock_idp_metadata):
    """Test successful SSO configuration for a trial account."""
    with patch('app.sso.config.SSOConfigManager._save_sso_config') as mock_save_config,
         patch('app.identity.providers.IdentityProvider.validate_metadata', return_value=True):
        
        sso_config_manager.configure_sso(trial_account, "saml_config_data", mock_idp_metadata)
        mock_save_config.assert_called_once_with(trial_account.account_id, "saml_config_data", mock_idp_metadata)

def test_configure_sso_for_paid_account_success(sso_config_manager, paid_account, mock_idp_metadata):
    """Test successful SSO configuration for an existing paid account."""
    with patch('app.sso.config.SSOConfigManager._save_sso_config') as mock_save_config,
         patch('app.identity.providers.IdentityProvider.validate_metadata', return_value=True):
        
        sso_config_manager.configure_sso(paid_account, "saml_config_data", mock_idp_metadata)
        mock_save_config.assert_called_once_with(paid_account.account_id, "saml_config_data", mock_idp_metadata)

def test_configure_sso_invalid_metadata(sso_config_manager, trial_account):
    """Test SSO configuration with invalid identity provider metadata."""
    with patch('app.identity.providers.IdentityProvider.validate_metadata', return_value=False):
        with pytest.raises(ValueError, match="Invalid Identity Provider metadata."):
            sso_config_manager.configure_sso(trial_account, "saml_config_data", {})