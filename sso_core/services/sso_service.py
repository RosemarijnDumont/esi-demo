
import logging
from sso_core.models.saml_config import SAMLConfig
from sso_core.models.account import Account, AccountType
from sso_core.integrations.saml_integration import SAMLIntegration

logger = logging.getLogger(__name__)

class SSOService:

    @staticmethod
    def _authorize_sso_action(account_id):
        account = Account.get_by_id(account_id)
        if not account:
            raise ValueError(f"Account with ID {account_id} not found.")
        # Allow SSO configuration for both PAID and TRIAL accounts
        if account.account_type not in [AccountType.PAID, AccountType.TRIAL]:
            raise ValueError("SSO configuration is not available for this account type.")
        return account

    @staticmethod
    def create_saml_configuration(account_id, config_data):
        account = SSOService._authorize_sso_action(account_id)

        if SAMLConfig.get_by_account_id(account_id):
            raise ValueError("SAML configuration already exists for this account. Use update instead.")

        try:
            # Validate config_data and create a new SAMLConfig object
            sso_config = SAMLConfig(
                account_id=account_id,
                idp_entity_id=config_data.get('idp_entity_id'),
                idp_sso_url=config_data.get('idp_sso_url'),
                idp_x509_cert=config_data.get('idp_x509_cert'),
                sp_entity_id=config_data.get('sp_entity_id', SAMLIntegration.generate_sp_entity_id(account_id)),
                sp_acs_url=config_data.get('sp_acs_url', SAMLIntegration.generate_sp_acs_url(account_id)),
                # Add other necessary SAML configuration fields
            )
            sso_config.save()
            logger.info(f"SAML configuration created for account {account_id} (Type: {account.account_type.name})")
            return sso_config
        except Exception as e:
            logger.error(f"Error creating SAML configuration for account {account_id}: {e}")
            raise

    @staticmethod
    def get_saml_configuration(account_id):
        SSOService._authorize_sso_action(account_id)
        try:
            config = SAMLConfig.get_by_account_id(account_id)
            return config
        except Exception as e:
            logger.error(f"Error retrieving SAML configuration for account {account_id}: {e}")
            raise

    @staticmethod
    def update_saml_configuration(account_id, config_data):
        account = SSOService._authorize_sso_action(account_id)
        sso_config = SAMLConfig.get_by_account_id(account_id)

        if not sso_config:
            raise ValueError("No SAML configuration found for this account. Use create instead.")

        try:
            # Update fields based on config_data
            sso_config.idp_entity_id = config_data.get('idp_entity_id', sso_config.idp_entity_id)
            sso_config.idp_sso_url = config_data.get('idp_sso_url', sso_config.idp_sso_url)
            sso_config.idp_x509_cert = config_data.get('idp_x509_cert', sso_config.idp_x509_cert)
            # Update other necessary SAML configuration fields
            sso_config.save()
            logger.info(f"SAML configuration updated for account {account_id} (Type: {account.account_type.name})")
            return sso_config
        except Exception as e:
            logger.error(f"Error updating SAML configuration for account {account_id}: {e}")
            raise

    @staticmethod
    def delete_saml_configuration(account_id):
        account = SSOService._authorize_sso_action(account_id)
        sso_config = SAMLConfig.get_by_account_id(account_id)

        if not sso_config:
            raise ValueError("No SAML configuration found for this account.")
        try:
            sso_config.delete()
            logger.info(f"SAML configuration deleted for account {account_id} (Type: {account.account_type.name})")
        except Exception as e:
            logger.error(f"Error deleting SAML configuration for account {account_id}: {e}")
            raise

    @staticmethod
    def generate_saml_metadata(account_id):
        # This method would typically interact with the SAML integration library
        # to dynamically generate the SP metadata XML.
        config = SAMLConfig.get_by_account_id(account_id)
        if not config:
            raise ValueError("No SAML configuration found for this account to generate metadata.")
        try:
            metadata_xml = SAMLIntegration.generate_sp_metadata(config)
            return metadata_xml
        except Exception as e:
            logger.error(f"Error generating SAML metadata for account {account_id}: {e}")
            raise

    @staticmethod
    def process_saml_response(account_id, saml_response):
        # This method handles the incoming SAML response from the IdP
        config = SAMLConfig.get_by_account_id(account_id)
        if not config:
            raise ValueError("No SAML configuration found for this account.")
        try:
            user_attributes = SAMLIntegration.process_response(config, saml_response)
            # Here, you would typically find or create a user in your system
            # based on user_attributes and authenticate them.
            logger.info(f"SAML response processed for account {account_id}. User attributes: {user_attributes}")
            return user_attributes
        except Exception as e:
            logger.error(f"Error processing SAML response for account {account_id}: {e}")
            raise
