# auth_service/app/services/auth_service.py
import bcrypt

class AuthService:
    def __init__(self):
        # In a real application, this would interact with a database
        self.users = {
            'user1': {'id': 1, 'username': 'user1', 'password_hash': self._hash_password('password123')}
        }

    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return user
        return None

    def get_user_by_id(self, user_id):
        for user in self.users.values():
            if user['id'] == user_id:
                return user
        return None

