import jwt
import datetime
import pytz
from flask import current_app
from functools import wraps

def generate_session_token(user_id):
    """
    Generates a new session token for the given user ID.
    The token is set to expire in 24 hours and includes the user's ID.
    """
    try:
        payload = {
            'exp': datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=24),
            'iat': datetime.datetime.now(pytz.utc),
            'sub': user_id
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        current_app.logger.error(f"Error generating session token for user {user_id}: {e}")
        raise

def decode_session_token(token):
    """
    Decodes a session token and returns the payload if valid.
    Raises an exception if the token is invalid or expired.
    """
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        current_app.logger.warning("Expired session token received.")
        raise ValueError("Session token has expired")
    except jwt.InvalidTokenError:
        current_app.logger.warning("Invalid session token received.")
        raise ValueError("Invalid session token")
    except Exception as e:
        current_app.logger.error(f"Error decoding session token: {e}")
        raise

def session_required(f):
    """
    A decorator to ensure a valid session token is present in the request.
    This is a placeholder and should be integrated with Flask's request context
    and error handling for a complete implementation.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This is a simplified example. In a real application, you would
        # extract the token from headers (e.g., Authorization: Bearer <token>)
        # and handle Flask's request context.
        # For demonstration purposes, we assume a token is passed or available.
        print("Session required decorator triggered.") # Placeholder for actual token extraction and validation
        return f(*args, **kwargs)
    return decorated_function


