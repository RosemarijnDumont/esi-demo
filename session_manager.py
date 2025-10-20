
from redis import Redis
from flask import current_app

class SessionManager:
    def __init__(self):
        self.redis = Redis.from_url(current_app.config['REDIS_URL'])

    def set_session(self, user_id, token):
        """
        Stores the session token in Redis with an expiration.
        """
        try:
            self.redis.setex(f"session:{user_id}", current_app.config['SESSION_EXPIRY'], token)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to set session for user {user_id}: {e}")
            return False

    def get_session(self, user_id):
        """
        Retrieves the session token for a given user ID.
        """
        try:
            return self.redis.get(f"session:{user_id}")
        except Exception as e:
            current_app.logger.error(f"Failed to get session for user {user_id}: {e}")
            return None

    def delete_session(self, user_id):
        """
        Deletes the session token for a given user ID.
        """
        try:
            self.redis.delete(f"session:{user_id}")
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to delete session for user {user_id}: {e}")
            return False
