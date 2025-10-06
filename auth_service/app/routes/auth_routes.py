# auth_service/app/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from ..services.auth_service import AuthService
from ..utils.jwt_utils import jwt_required, generate_token

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400

    user = auth_service.authenticate_user(data['username'], data['password'])
    if user:
        access_token = generate_token(user['id'], 'access')
        refresh_token = generate_token(user['id'], 'refresh')
        return jsonify({'message': 'Login successful', 'access_token': access_token, 'refresh_token': refresh_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/refresh_token', methods=['POST'])
@jwt_required(token_type='refresh')
def refresh_token(user_id):
    new_access_token = generate_token(user_id, 'access')
    return jsonify({'message': 'Token refreshed successfully', 'access_token': new_access_token}), 200

@auth_bp.route('/validate_session', methods=['GET'])
@jwt_required(token_type='access')
def validate_session(user_id):
    # If the jwt_required decorator passes, the token is valid and not expired.
    # We can also perform additional checks here if needed, e.g., blacklist checks.
    return jsonify({'message': 'Session is valid', 'user_id': user_id}), 200

