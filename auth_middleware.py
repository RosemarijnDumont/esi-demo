
from flask import request, jsonify
from functools import wraps
from auth_service import AuthService
import logging

auth_service = AuthService()

# Configure logging for the middleware
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # JWT is generally passed in the Authorization header as a Bearer token
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                logging.warning("Malformed Authorization header. No Bearer token found.")
                return jsonify({"message": "Token is missing or malformed!"}), 401

        if not token:
            logging.warning("No token provided in request.")
            return jsonify({"message": "Token is missing!"}), 401

        try:
            current_user_id = auth_service.validate_token(token)
            if current_user_id is None:
                logging.warning(f"Token validation failed for token: {token}")
                return jsonify({"message": "Token is invalid or expired!"}), 401
        except Exception as e:
            logging.error(f"Error during token validation: {e}")
            return jsonify({"message": "Token validation failed due to server error!"}), 500

        request.current_user = current_user_id # Attach user_id to request object
        return f(*args, **kwargs)
    return decorated

