from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from sso_service import SSOService
from core.security import decode_jwt

sso_bp = Blueprint('sso', __name__)
sso_service = SSOService()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Authorization token is missing or invalid'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            payload = decode_jwt(token)
            request.current_user = payload # Attach user info to request context
        except Exception as e:
            return jsonify({'message': 'Invalid token', 'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function

@sso_bp.route('/sso/saml/config', methods=['POST'])
@login_required
def configure_saml():
    """
    API endpoint for trial account administrators to upload and manage their SAML Identity Provider (IdP) metadata.
    """
    data = request.get_json()
    account_id = request.current_user.get('account_id') # Assuming account_id is in JWT payload
    idp_metadata_xml = data.get('idp_metadata_xml')

    if not account_id or not idp_metadata_xml:
        return jsonify({'message': 'Account ID and IdP metadata XML are required'}), 400

    try:
        saml_config = sso_service.enable_saml_for_trial(account_id, idp_metadata_xml)
        return jsonify({
            'message': 'SAML configuration updated successfully',
            'saml_config_id': saml_config.id,
            'account_id': saml_config.account_id,
            'enabled': saml_config.enabled
        }), 200
    except ValueError as e:
        current_app.logger.error(f"SAML configuration error: {e}")
        return jsonify({'message': str(e)}), 400
    except Exception as e:
        current_app.logger.exception(f"Internal error configuring SAML: {e}")
        return jsonify({'message': 'Internal server error'}), 500

@sso_bp.route('/sso/saml/acs', methods=['POST'])
def saml_acs():
    """
    SAML Assertion Consumer Service (ACS) endpoint to receive and process SAML responses.
    This endpoint processes SAML responses for both trial and paid accounts.
    """
    saml_response = request.form.get('SAMLResponse')
    relay_state = request.form.get('RelayState') # Optionally used to carry account_id or other context

    if not saml_response:
        return 'SAMLResponse is missing', 400
    
    # In a real-world scenario, you'd extract account_id from RelayState or a subdomain/path
    # For this example, let's assume RelayState contains a simple account_id or can be derived.
    # For production, consider robust RelayState handling or dedicated ACS URLs per account.
    account_id = None
    if relay_state and relay_state.startswith("account_"):
        account_id = relay_state.split("account_")[1]
    
    if not account_id:
         # This is a critical point. Without RelayState providing account_id, 
         # we need another way to map the SAML response to an account. 
         # Options: 
         # 1. Dedicated ACS URL per account (e.g., /sso/<account_id>/saml/acs)
         # 2. Parse SAML response for an Issuer that maps to an account.
         # For now, raising an error for demonstration.
        current_app.logger.error("SAML ACS received a response without a verifiable account_id in RelayState.")
        return "Unable to determine account from SAML response.", 400

    try:
        user = sso_service.authenticate_saml_response(account_id, saml_response)
        if user:
            # Generate JWT or session token for the authenticated user
            # This token will be used by the frontend to authenticate subsequent requests
            token = sso_service.generate_user_session_token(user) # Assume this method exists in SSOService
            # Redirect to a frontend post-login URL with the token
            return current_app.redirect(f"/dashboard?token={token}")
            # For API-only, return JSON
            # return jsonify({'message': 'Authentication successful', 'user_id': user.id, 'token': token}), 200
        else:
            return jsonify({'message': 'SAML authentication failed'}), 401
    except Exception as e:
        current_app.logger.exception(f"Error processing SAML ACS for account {account_id}: {e}")
        return jsonify({'message': 'Internal server error during SAML authentication'}), 500

@sso_bp.route('/sso/saml/metadata', methods=['GET'])
def get_saml_metadata():
    """
    Provides the SAML Service Provider (SP) metadata XML.
    IdPs will need this to configure our application as a Service Provider.
    """
    try:
        metadata_xml = sso_service.get_saml_sp_metadata()
        return current_app.response_class(
            metadata_xml,
            mimetype='application/xml'
        )
    except Exception as e:
        current_app.logger.exception(f"Error generating SP metadata: {e}")
        return jsonify({'message': 'Error generating SP metadata'}), 500