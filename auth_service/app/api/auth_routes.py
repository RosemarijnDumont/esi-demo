from flask import Blueprint, request, jsonify, current_app
from auth_service.app.services.auth_service import generate_session_token, decode_session_token
from auth_service.app.exceptions import InvalidUsage

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handles user login. Authenticates user credentials and issues a session token.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise InvalidUsage("Missing username or password", status_code=400)

    # In a real application, you would verify username and password against a database
    # For this example, we'll use a dummy check.
    if username == "test_user" and password == "password123":
        try:
            user_id = 123 # Dummy user ID
            token = generate_session_token(user_id)
            current_app.logger.info(f"User {username} logged in successfully.")
            return jsonify({'message': 'Login successful', 'token': token}), 200
        except Exception as e:
            current_app.logger.error(f"Login failed for user {username} due to token generation error: {e}")
            raise InvalidUsage("Login failed due to an internal error", status_code=500)
    else:
        current_app.logger.warning(f"Failed login attempt for username: {username}")
        raise InvalidUsage("Invalid username or password", status_code=401)

@auth_bp.route('/validate_session', methods=['GET'])
def validate_session():
    """
    Validates the provided session token.
    This API can be called by clients to check the validity of their current session.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise InvalidUsage("Authorization header missing", status_code=401)

    try:
        token = auth_header.split(" ")[1]
        payload = decode_session_token(token)
        current_app.logger.info(f"Session token valid for user {payload['sub']}")
        return jsonify({'message': 'Session valid', 'user_id': payload['sub']}), 200
    except IndexError:
        raise InvalidUsage("Bearer token not found in Authorization header", status_code=401)
    except ValueError as e:
        current_app.logger.warning(f"Session validation failed: {e}")
        raise InvalidUsage(str(e), status_code=401)
    except Exception as e:
        current_app.logger.error(f"Unexpected error during session validation: {e}")
        raise InvalidUsage("Internal server error during session validation", status_code=500)


