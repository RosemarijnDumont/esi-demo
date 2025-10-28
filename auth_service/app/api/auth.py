from flask import Blueprint, request, jsonify, session
from auth_service.app.utils.jwt_utils import generate_token, decode_token, JwtError
from auth_service.app.models.user import User
from auth_service.app.utils.rate_limiter import rate_limit
from auth_service.app import db
import logging
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['POST'])
@rate_limit(limit=5, window=300) # 5 attempts every 5 minutes
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        logger.warning(f"Login attempt with missing credentials for username: {username}")
        return jsonify({'message': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        try:
            token = generate_token(user.id)
            session['token'] = token  # Store token in session for immediate use if needed
            logger.info(f"User {username} logged in successfully.")
            return jsonify({'message': 'Login successful', 'token': token}), 200
        except Exception as e:
            logger.error(f"Error generating token for user {username}: {e}")
            return jsonify({'message': 'Internal server error during token generation'}), 500
    else:
        logger.warning(f"Failed login attempt for username: {username}")
        return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('token', None)
    logger.info("User logged out.")
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/validate_session', methods=['GET'])
def validate_session():
    token = request.headers.get('Authorization')
    if not token:
        logger.warning("Session validation attempt without token.")
        return jsonify({'message': 'No token provided'}), 401

    if token.startswith('Bearer '):
        token = token.split(' ')[1]

    try:
        payload = decode_token(token)
        user_id = payload.get('user_id')
        user = User.query.get(user_id)
        if user:
            logger.info(f"Session validated for user ID: {user_id}")
            return jsonify({'message': 'Session valid', 'user_id': user_id}), 200
        else:
            logger.warning(f"Session token valid but user ID {user_id} not found.")
            return jsonify({'message': 'Invalid session token: User not found'}), 401
    except JwtError as e:
        logger.error(f"JWT error during session validation: {e}")
        return jsonify({'message': f'Invalid session token: {e}'}), 401
    except Exception as e:
        logger.error(f"Unexpected error during session validation: {e}")
        return jsonify({'message': 'Internal server error during session validation'}), 500

