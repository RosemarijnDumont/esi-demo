
import jwt
import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AuthService:
    def __init__(self):
        self.secret_key = os.environ.get("JWT_SECRET_KEY", "super-secret-key")
        self.session_tokens = {}

    def generate_token(self, user_id):
        try:
            payload = {
                "user_id": user_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token valid for 1 hour
            }
            token = jwt.encode(payload, self.secret_key, algorithm="HS256")
            self.session_tokens[user_id] = token # Store token for session management
            logging.info(f"Generated new token for user_id: {user_id}")
            return token
        except Exception as e:
            logging.error(f"Error generating token for user_id {user_id}: {e}")
            raise

    def refresh_token(self, user_id):
        try:
            if user_id in self.session_tokens:
                # Invalidate old token (optional, depending on desired behavior)
                del self.session_tokens[user_id]
                logging.info(f"Refreshed token for user_id: {user_id}")
                return self.generate_token(user_id)
            else:
                logging.warning(f"Attempted to refresh non-existent token for user_id: {user_id}")
                return None
        except Exception as e:
            logging.error(f"Error refreshing token for user_id {user_id}: {e}")
            raise

    def validate_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload["user_id"]
            if self.session_tokens.get(user_id) == token: # Ensure token is still active in our session store
                logging.info(f"Token validated successfully for user_id: {user_id}")
                return user_id
            else:
                logging.warning(f"Invalid or expired token for user_id: {user_id}")
                return None
        except jwt.ExpiredSignatureError:
            logging.warning("Expired token provided.")
            return None
        except jwt.InvalidTokenError:
            logging.warning("Invalid token provided.")
            return None
        except Exception as e:
            logging.error(f"Error validating token: {e}")
            raise

    def invalidate_token(self, user_id):
        try:
            if user_id in self.session_tokens:
                del self.session_tokens[user_id]
                logging.info(f"Invalidated token for user_id: {user_id}")
                return True
            else:
                logging.warning(f"Attempted to invalidate non-existent token for user_id: {user_id}")
                return False
        except Exception as e:
            logging.error(f"Error invalidating token for user_id {user_id}: {e}")
            raise

