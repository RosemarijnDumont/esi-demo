import logging
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings

logger = logging.getLogger(__name__)

class SamlServiceProvider:
    def __init__(self, sp_base_url: str = "http://localhost:5000"):
        """
        Initializes the SAML Service Provider with basic configurations.
        In a production environment, these settings would come from a configuration management system.
        """
        self.sp_base_url = sp_base_url
        self._settings = self._load_sp_settings()

    def _load_sp_settings(self) -> dict:
        """
        Loads the Service Provider's (our application's) SAML settings.
        These are static for our SP.
        """
        # These are example SP settings. In a real application, populate these
        # from environment variables or a secure configuration store.
        return {
            'strict': True,
            'debug': True,
            'sp': {
                'entityId': f'{self.sp_base_url}/sso/saml/metadata',
                'assertionConsumerService': {
                    'url': f'{self.sp_base_url}/sso/saml/acs',
                    'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST'
                },
                'singleLogoutService': {
                    # Optional: implement if supporting SAML SLO
                    'url': f'{self.sp_base_url}/sso/saml/sls',
                    'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect'
                },
                'NameIDFormat': 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress',
                'x509cert': 'MIIDBTCCAf2gAwIBAgIUW4/O2i5p9x2G7f4v8k/p0E9o6+wwDQYJKoZIhvcNAQELBQAwUDEqMCgGA1UEAxMhYWNtZS1jbG91ZC1zYW1sLXNlcnZpY2UucmFwaWQxLjAsBgNVBAsMJVdhbWJhc0NhY2hlLURlbW8tQWNjZXNzLUNlcnRpZmljZWQwHhcNMjMwMzE3MTI0NDQ0WhcNMzMwMzE3MTI0NDQ0WjBQMSowKAYDVQQDEyFhY21lLWNsb3VkLXNhbWwtc2VydmljZS5yYXBpZDEuMCwGA1UECwMlV2FtYmFzQ2FjaGUtRGVtby1BY2Nlc3MtQ2VydGlmaWNlZzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALqT3R6Yp/B7z6k0hJzK/C+5e8nQ9X4g7g4j8g7+9bM2k8Q43/5X/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8/J8=',
                'privateKey': '-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-256-CBC,2C712C573A141A8F6A3FE9A045330FBA

5+Qx0p+w+J7D8E7H8N6V5U/P3H9W6C7F1B3E0A9D2G6K4J/L3M9N8O7Q5R
9T7V5X1Z0Y8C6I4L2K/M7N5P4S2W0X8Z7A5B3D1F9G7J5H3I1K9L7M5N3P
1R9S7U5W3Y1A9C7E5G3I1K9M7O5Q3S1U9W7Y5A3C1E9G7I5K3M1O9Q7S5U
3W1Y9A7C5E3G1I9K7M5O3Q1S9U7W5Y3A1C9E7G5I3K1M9O7Q5S3U1W9Y7A
5C3E1G9I7K5M3O1Q9S7U5W5Z3A1C9E7G5I3K1M9O7Q5S3U1W9Y5A3C1E9G
7I5K3M1O9Q7S3U1W9Y7Z5A3C1E9G7I5K3M1O9Q7S3U1W9Y7A5C3E1G9I7K
5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q
9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W
9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C
3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I
7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O
1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U
1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A
5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G
9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M
3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S
7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y
7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E
1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K
5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q
9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W
9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C
3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I
7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O
1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U
1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1G9I7K5M3O1Q9S7U1W9Y7A
5C3E1G9I7K5M3O1Q9S7U1W9Y7A5C3E1A9D6F3H0J8L6N4P2R0T8V6X4Z2B
0D8F6H4J2L0N8P6R4T2V0X8Z7B5D3F1H9J7L5N3P1R9S7U5W3Y1A9C7E5G3
I1K9M7O5Q3S1U9W7Y5A3C1E9G7I5K3M1O9Q7S1U9W7Y5A3C1E9G7I5K3M
-----END RSA PRIVATE KEY-----'
            },
            'security': {
                'authnRequestsSigned': True,
                'wantAssertionsSigned': True,
                'wantAssertionsEncrypted': False, # For simplicity, can be enabled.
                'metadataCacheDuration': None
            }
        }

    def get_sp_metadata(self) -> str:
        """
        Generates and returns the Service Provider's (SP) metadata XML.
        This XML is given to the Identity Provider (IdP) for configuration.
        """
        saml_settings = OneLogin_Saml2_Settings(settings=self._settings, custom_base_path="/tmp")
        metadata = saml_settings.get_sp_metadata()
        errors = saml_settings.validate_metadata(metadata)
        if len(errors) > 0:
            logger.error(f"SAML SP Metadata validation errors: {', '.join(errors)}")
            raise Exception(f"Invalid SP metadata: {', '.join(errors)}")
        return metadata

    def process_saml_response(self, saml_response: str, idp_metadata_xml: str) -> Optional[dict]:
        """
        Processes a SAML response received from the IdP.
        """
        try:
            # Dynamically load IdP settings based on provided XML for the account
            idp_settings = self._get_idp_settings_from_xml(idp_metadata_xml)
            full_settings = self._settings.copy()
            full_settings.update({'idp': idp_settings})

            auth = OneLogin_Saml2_Auth(
                request_data={'https': 'on', 'post_data': {'SAMLResponse': saml_response}},
                old_settings=full_settings
            )
            auth.process_response()

            if auth.is_authenticated():
                attributes = auth.get_attributes()
                logger.info(f"User authenticated successfully via SAML. Attributes: {attributes}")
                return attributes
            else:
                errors = auth.get_errors()
                logger.warning(f"SAML authentication failed. Errors: {', '.join(errors)}")
                logger.warning(f"SAML last error reason: {auth.get_last_error_reason()}")
                return None
        except Exception as e:
            logger.exception(f"Error during SAML response processing: {e}")
            return None

    def _get_idp_settings_from_xml(self, idp_metadata_xml: str) -> dict:
        """
        Parses IdP metadata XML to extract necessary settings for OneLogin_Saml2_Auth.
        This is a simplified approach. In a real application, you might use a dedicated
        XML parser or a library if OneLogin_Saml2 doesn_t handle raw XML directly for settings.
        For the purpose of this example, we assume `onelogin.saml2.settings.OneLogin_Saml2_Settings`
        can parse the IDP metadata XML directly or we extract key fields.

        Note: The `python-saml` library expects IdP settings in a specific dictionary format.
              Direct parsing of the XML into this format is required.
              A robust implementation might use `onelogin.saml2.IdPMetadataParser` if available
              or manually parse the XML.
        """
        # This is a placeholder. A proper implementation would parse the XML
        # to extract entityId, singleSignOnService, and x509cert for the IdP.
        # For now, we rely on `OneLogin_Saml2_Auth`'s ability to handle IdP metadata XML
        # when passed within the settings, or we must pre-parse.
        # The python-saml library often expects a 'idp' key in the settings dict
        # with these explicitly defined. If idp_metadata_xml is to be used directly,
        # the library's usage pattern might differ or require a file path.

        # A common pattern is to have a tool that converts IdP metadata XML to the dict format.
        # For demonstration, we'll assume the library can be initialized with idp_metadata_xml
        # if placed in the settings correctly, or we extract key elements.

        # Example of how you *might* extract key info (simplified - real parsing is complex):
        from xml.etree import ElementTree as ET
        root = ET.fromstring(idp_metadata_xml)
        idp_entity_id = root.attrib.get('entityID')
        
        # Namespaces are crucial for proper parsing
        saml_ns = '{urn:oasis:names:tc:SAML:2.0:metadata}'
        ds_ns = '{http://www.w3.org/2000/09/xmldsig#}'

        sso_service_url = None
        x509cert = None

        for sso_descriptor in root.findall(f'.//{saml_ns}IDPSSODescriptor'):
            for sso_service in sso_descriptor.findall(f'.//{saml_ns}SingleSignOnService'):
                if sso_service.attrib.get('Binding') == 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect':
                    sso_service_url = sso_service.attrib.get('Location')
                    break
            for key_descriptor in sso_descriptor.findall(f'.//{saml_ns}KeyDescriptor'):
                if key_descriptor.attrib.get('use') == 'signing' or 'use' not in key_descriptor.attrib:
                    cert_node = key_descriptor.find(f'.//{ds_ns}X509Certificate')
                    if cert_node is not None:
                        x509cert = cert_node.text.strip()
                        break # Take the first signing cert
            if sso_service_url and x509cert: # Found enough info
                break

        if not idp_entity_id or not sso_service_url or not x509cert:
            logger.error("Failed to parse critical IdP metadata: entityID, SingleSignOnService or X509Certificate missing.")
            raise ValueError("Invalid IdP metadata XML provided. Missing critical information.")

        return {
            'entityId': idp_entity_id,
            'singleSignOnService': {
                'url': sso_service_url,
                'binding': 'urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect' # Assuming redirect binding
            },
            'x509cert': x509cert
        }