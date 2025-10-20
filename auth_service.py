
import jwt
import datetime
from flask import current_app

def generate_token(user_id):
    """
    Generates a new JWT token for the given user ID.
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
        current_app.logger.error(f"Token generation failed: {e}")
        return None

def decode_token(token):
    """
    Decodes a JWT token and returns the payload.
    """
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        current_app.logger.warning("Expired token encountered.")
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        current_app.logger.warning("Invalid token encountered.")
        return {"error": "Invalid token"}
    except Exception as e:
        current_app.logger.error(f"Token decoding failed: {e}")
        return {"error": "Decoding failed"}

def refresh_token(token):
    """
    Refreshes an expired or nearly expired token.
    """
    decoded = decode_token(token)
    if decoded and 'sub' in decoded:
        user_id = decoded['sub']
        return generate_token(user_id)
    return None
