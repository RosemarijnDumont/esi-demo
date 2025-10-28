import jwt
import datetime
import os

class JwtError(Exception):
    pass

def generate_token(user_id):
    try:
        secret_key = os.environ.get('SECRET_KEY', 'super-secret-key') # Fallback for local development
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable not set.")

        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24), # Token expires in 24 hours
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')
    except Exception as e:
        raise JwtError(f"Token generation failed: {e}")

def decode_token(token):
    try:
        secret_key = os.environ.get('SECRET_KEY', 'super-secret-key') # Fallback for local development
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable not set.")
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise JwtError("Token has expired")
    except jwt.InvalidTokenError:
        raise JwtError("Invalid token")
    except Exception as e:
        raise JwtError(f"Token decoding failed: {e}")
