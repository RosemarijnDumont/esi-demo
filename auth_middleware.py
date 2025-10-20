
from flask import request, jsonify, current_app, g
from functools import wraps
from auth_service import decode_token, refresh_token, generate_token
from session_manager import SessionManager

session_manager = SessionManager()

def token_required(f):
    """
    Decorator to protect routes that require a valid authentication token.
    Handles token expiration and refreshment.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        decoded_token = decode_token(token)

        if decoded_token.get("error") == "Token expired":
            user_id = decoded_token.get('sub')
            if user_id:
                current_app.logger.info(f"Attempting to refresh token for user {user_id}")
                new_token = refresh_token(token)
                if new_token:
                    session_manager.set_session(user_id, new_token)
                    g.user_id = user_id
                    g.new_token = new_token  # Attach new token to g for response if needed
                    return f(*args, **kwargs)
                else:
                    return jsonify({'message': 'Could not refresh token. Please log in again.'}), 401
            else:
                return jsonify({'message': 'Expired token without a valid user ID. Please log in again.'}), 401
        elif decoded_token.get("error") == "Invalid token":
            return jsonify({'message': 'Invalid session token. Please log in again.'}), 403
        elif decoded_token.get("error"):
            current_app.logger.error(f"Error decoding token: {decoded_token.get('error')}")
            return jsonify({'message': 'Failed to authenticate token. Please log in again.'}), 401

        g.user_id = decoded_token['sub']
        return f(*args, **kwargs)

    return decorated

def login_required(f):
    """
    Decorator to ensure a user is logged in and their session is valid.
    This will typically be used as a primary login check after initial authentication.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = g.get('user_id')
        if not user_id:
            return jsonify({'message': 'User not authenticated.'}), 401

        # Optional: Additional check against session store if needed
        # For highly sensitive operations, you might want to re-validate the token
        # or check its presence in the session store to prevent replay attacks
        # or to ensure it hasn't been explicitly logged out.
        stored_token_bytes = session_manager.get_session(user_id)
        if stored_token_bytes:
            stored_token = stored_token_bytes.decode('utf-8')
            current_token = request.headers.get('Authorization', '').split(' ')[1] if 'Authorization' in request.headers else None

            if stored_token != current_token:
                current_app.logger.warning(f"User {user_id} presented a token inconsistent with stored session.")
                return jsonify({'message': 'Session inconsistency detected. Please log in again.'}), 401
        else:
            current_app.logger.warning(f"No active session found for user {user_id}.")
            return jsonify({'message': 'No active session found. Please log in again.'}), 401

        return f(*args, **kwargs)

    return decorated
