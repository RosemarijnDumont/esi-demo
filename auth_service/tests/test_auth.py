import unittest
import json
from auth_service.app import create_app, db
from auth_service.app.models.user import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create a test user
            user = User(username='testuser')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_successful_login(self):
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)

    def test_failed_login_invalid_credentials(self):
        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', response.json['message'])

    def test_failed_login_missing_credentials(self):
        response = self.client.post('/auth/login', json={
            'username': 'testuser'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing username or password', response.json['message'])

    def test_logout(self):
        # First, log in to get a session
        self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        response = self.client.post('/auth/logout')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged out successfully', response.json['message'])

    def test_session_validation_valid_token(self):
        login_response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        token = json.loads(login_response.data)['token']

        response = self.client.get('/auth/validate_session', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Session valid', response.json['message'])

    def test_session_validation_invalid_token(self):
        response = self.client.get('/auth/validate_session', headers={'Authorization': 'Bearer invalidtoken'})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid session token', response.json['message'])

    def test_session_validation_no_token(self):
        response = self.client.get('/auth/validate_session')
        self.assertEqual(response.status_code, 401)
        self.assertIn('No token provided', response.json['message'])

    def test_rate_limiting(self):
        # Attempt more than 5 logins within a short window
        for _ in range(5):
            self.client.post('/auth/login', json={'username': 'testuser', 'password': 'wrongpassword'})

        response = self.client.post('/auth/login', json={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 429)
        self.assertIn('Too many requests', response.json['message'])

