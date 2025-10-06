# auth_service/app/utils/jwt_utils.py
import jwt
from flask import request, jsonify
from functools import wraps
import datetime

# Ideally, these would be loaded from environment variables or a secure configuration management system
SECRET_KEY = 'your_super_secret_key_change_this_in_production'
ACCESS_TOKEN_EXPIRATION_MINUTES = 15
REFRESH_TOKEN_EXPIRATION_DAYS = 7

def generate_token(user_id, token_type='access'):
    if token_type == 'access':
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    elif token_type == 'refresh':
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRATION_DAYS)
    else:
        raise ValueError('Invalid token type')

    payload = {
        'user_id': user_id,
        'exp': expiration,
        'iat': datetime.datetime.utcnow(),
        'token_type': token_type
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def jwt_required(token_type='access'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    scheme, token = auth_header.split(None, 1) # Split on first space
                    if scheme.lower() != 'bearer':
                        token = None
                except ValueError:
                    # Malformed Authorization header
                    pass

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                if data['token_type'] != token_type:
                    return jsonify({'message': f'Invalid token type. Expected {token_type}, got {data["token_type"]}'}), 403
                kwargs['user_id'] = data['user_id']
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired!'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token!'}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator

