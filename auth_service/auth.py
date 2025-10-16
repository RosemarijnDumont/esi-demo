import jwt
import datetime
from flask import request, jsonify, make_response
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AuthService:
    def __init__(self, secret_key, session_duration_minutes=30):
        self.secret_key = secret_key
        self.session_duration_minutes = session_duration_minutes

    def generate_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.session_duration_minutes),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            token = jwt.encode(payload, self.secret_key, algorithm='HS256')
            logging.info(f"Token generated for user_id: {user_id}")
            return token
        except Exception as e:
            logging.error(f"Error generating token for user_id {user_id}: {e}")
            raise

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            logging.info(f"Token decoded for user_id: {payload['sub']}")
            return payload
        except jwt.ExpiredSignatureError:
            logging.warning("Attempted to decode expired token.")
            return {'error': 'Signature expired'}
        except jwt.InvalidTokenError:
            logging.warning("Attempted to decode invalid token.")
            return {'error': 'Invalid token'}
        except Exception as e:
            logging.error(f"Error decoding token: {e}")
            raise

    def login_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']

            if not token:
                logging.warning("Login attempt without token.")
                return make_response(jsonify({'message': 'Token is missing!'}), 401)

            try:
                data = self.decode_token(token)
                if 'error' in data:
                    logging.warning(f"Authentication failed: {data['error']}")
                    return make_response(jsonify({'message': data['error']}), 401)
                current_user = data['sub']
            except Exception as e:
                logging.error(f"Token validation error: {e}")
                return make_response(jsonify({'message': 'Token is invalid!'}), 401)

            return f(current_user, *args, **kwargs)
        return decorated

    def refresh_token(self, token):
        try:
            payload = self.decode_token(token)
            if 'error' in payload:
                logging.warning(f"Token refresh failed due to: {payload['error']}")
                return {'error': payload['error']}

            user_id = payload['sub']
            # Generate a new token with a renewed expiration time
            new_token = self.generate_token(user_id)
            logging.info(f"Token refreshed for user_id: {user_id}")
            return {'token': new_token}
        except Exception as e:
            logging.error(f"Error refreshing token: {e}")
            return {'error': 'Could not refresh token'}

    def authenticate_user(self, username, password):
        # This is a placeholder. In a real application, you would check a database.
        # For demonstration purposes, let's assume a simple check.
        if username == "testuser" and password == "password123":
            logging.info(f"User {username} successfully authenticated.")
            return {"user_id": 1, "username": username}
        logging.warning(f"Authentication failed for user: {username}")
        return None

