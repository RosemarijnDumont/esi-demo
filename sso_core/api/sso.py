
from flask import Blueprint, request, jsonify
from sso_core.services.sso_service import SSOService
from sso_core.security.decorators import auth_required, role_required
from sso_core.models.account import AccountType

sso_bp = Blueprint('sso', __name__)

@sso_bp.route('/saml/config', methods=['POST'])
@auth_required
@role_required(roles=[AccountType.PAID, AccountType.TRIAL]) # Allow trial accounts to configure
def create_saml_config():
    data = request.json
    account_id = request.user.account_id

    try:
        config = SSOService.create_saml_configuration(account_id, data)
        return jsonify(config.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Log the error with more details
        return jsonify({'error': 'An unexpected error occurred'}), 500

@sso_bp.route('/saml/config', methods=['GET'])
@auth_required
@role_required(roles=[AccountType.PAID, AccountType.TRIAL])
def get_saml_config():
    account_id = request.user.account_id
    try:
        config = SSOService.get_saml_configuration(account_id)
        if config:
            return jsonify(config.to_dict()), 200
        return jsonify({'message': 'No SAML configuration found'}), 404
    except Exception as e:
        # Log the error with more details
        return jsonify({'error': 'An unexpected error occurred'}), 500

@sso_bp.route('/saml/config', methods=['PUT'])
@auth_required
@role_required(roles=[AccountType.PAID, AccountType.TRIAL])
def update_saml_config():
    data = request.json
    account_id = request.user.account_id

    try:
        config = SSOService.update_saml_configuration(account_id, data)
        return jsonify(config.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Log the error with more details
        return jsonify({'error': 'An unexpected error occurred'}), 500

@sso_bp.route('/saml/config', methods=['DELETE'])
@auth_required
@role_required(roles=[AccountType.PAID, AccountType.TRIAL])
def delete_saml_config():
    account_id = request.user.account_id
    try:
        SSOService.delete_saml_configuration(account_id)
        return jsonify({'message': 'SAML configuration deleted successfully'}), 204
    except Exception as e:
        # Log the error with more details
        return jsonify({'error': 'An unexpected error occurred'}), 500

@sso_bp.route('/saml/metadata', methods=['GET'])
def get_saml_metadata():
    # This endpoint is typically public for IdP to fetch SP metadata
    account_id = request.args.get('account_id') # Assuming account_id can be passed as a query param for public metadata endpoint
    if not account_id:
        return jsonify({'error': 'account_id is required'}), 400
    try:
        metadata = SSOService.generate_saml_metadata(account_id)
        return metadata, 200, {'Content-Type': 'application/xml'}
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        # Log the error with more details
        return jsonify({'error': 'An unexpected error occurred'}), 500
