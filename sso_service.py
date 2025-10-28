import logging
from typing import Optional

from core.models import Account, SamlConfig, User
from core.integrations.saml import SamlServiceProvider
from core.security import sign_jwt, verify_password
from core.db import db_session

logger = logging.getLogger(__name__)

class SSOService:
    def __init__(self):
        self.saml_sp = SamlServiceProvider()

    def enable_saml_for_trial(self, account_id: str, idp_metadata_xml: str) -> SamlConfig:
        """
        Enables SAML for a trial account by storing IdP metadata.

        Args:
            account_id: The ID of the trial account.
            idp_metadata_xml: The XML metadata of the Identity Provider.

        Returns:
            The created or updated SamlConfig object.

        Raises:
            ValueError: If the account is not a trial account or an error occurs during configuration.
        """
        with db_session() as session:
            account = session.query(Account).filter_by(id=account_id).first()
            if not account:
                raise ValueError(f"Account with ID {account_id} not found.")

            # Allow SAML for all accounts regardless of plan type (trial or paid)
            # The previous 'paid plan' check is removed.

            saml_config = session.query(SamlConfig).filter_by(account_id=account_id).first()
            if not saml_config:
                saml_config = SamlConfig(account_id=account_id)
                session.add(saml_config)

            saml_config.idp_metadata_xml = idp_metadata_xml
            saml_config.enabled = True
            session.commit()
            logger.info(f"SAML enabled for account {account_id}")
            return saml_config

    def authenticate_saml_response(self, account_id: str, saml_response: str) -> Optional[User]:
        """
        Authenticates a SAML response for a given account.

        Args:
            account_id: The ID of the account.
            saml_response: The SAML response received from the IdP.

        Returns:
            The authenticated User object if successful, otherwise None.
        """
        with db_session() as session:
            saml_config = session.query(SamlConfig).filter_by(account_id=account_id, enabled=True).first()
            if not saml_config or not saml_config.idp_metadata_xml:
                logger.warning(f"SAML not configured or enabled for account {account_id}")
                return None

            try:
                user_attributes = self.saml_sp.process_saml_response(
                    saml_response=saml_response,
                    idp_metadata_xml=saml_config.idp_metadata_xml
                )
                if user_attributes:
                    email = user_attributes.get("email")
                    if not email:
                        logger.error(f"SAML response for account {account_id} missing email attribute.")
                        return None

                    user = session.query(User).filter_by(email=email, account_id=account_id).first()
                    if not user:
                        # Provision user if they don't exist and account allows auto-provisioning
                        # For trial accounts, we might auto-provision by default or based on a setting
                        user = self._provision_user(session, account_id, email, user_attributes)
                        logger.info(f"User {email} provisioned for account {account_id} via SAML.")
                    else:
                        logger.info(f"User {email} authenticated for account {account_id} via SAML.")
                    return user
                else:
                    logger.warning(f"Invalid SAML response for account {account_id}")
            except Exception as e:
                logger.exception(f"Error processing SAML response for account {account_id}: {e}")
            return None

    def _provision_user(self, session, account_id: str, email: str, user_attributes: dict) -> User:
        """
        Provisions a new user in the system based on SAML attributes.
        """
        # TODO: Implement more sophisticated role/permission mapping based on SAML attributes
        # For now, assign a default role or based on some basic attribute mapping
        new_user = User(
            account_id=account_id,
            email=email,
            first_name=user_attributes.get("firstName"),
            last_name=user_attributes.get("lastName"),
            is_active=True,
            # Assign a default role for trial users or configure based on SAML attributes
            role="trial_user" # Example default role
        )
        session.add(new_user)
        session.commit()
        return new_user

    def get_saml_sp_metadata(self) -> str:
        """
        Returns the SAML Service Provider (SP) metadata XML.
        """
        return self.saml_sp.get_sp_metadata()