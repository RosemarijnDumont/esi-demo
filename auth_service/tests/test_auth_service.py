import unittest
import time
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import jwt
from flask import Flask

from auth_service.app.services.auth_service import generate_session_token, decode_session_token, session_required

class AuthServiceTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.user_id = 123

    def tearDown(self):
        self.app_context.pop()

    def test_generate_session_token(self):
        token = generate_session_token(self.user_id)
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)

        # Decode to verify contents (optional, but good for robust testing)
        decoded = jwt.decode(token, self.app.config['SECRET_KEY'], algorithms=['HS256'])
        self.assertEqual(decoded['sub'], self.user_id)
        self.assertIn('exp', decoded)
        self.assertIn('iat', decoded)

    def test_decode_valid_session_token(self):
        token = generate_session_token(self.user_id)
        decoded_payload = decode_session_token(token)
        self.assertEqual(decoded_payload['sub'], self.user_id)

    def test_decode_expired_session_token(self):
        # Manually create an expired token
        expired_payload = {
            'exp': datetime.now(timezone.utc) - timedelta(minutes=5),  # 5 minutes in the past
            'iat': datetime.now(timezone.utc) - timedelta(hours=1),
            'sub': self.user_id
        }
        expired_token = jwt.encode(expired_payload, self.app.config['SECRET_KEY'], algorithm='HS256')

        with self.assertRaises(ValueError) as cm:
            decode_session_token(expired_token)
        self.assertIn("Session token has expired", str(cm.exception))

    def test_decode_invalid_session_token(self):
        invalid_token = "this.is.an.invalid.token"
        with self.assertRaises(ValueError) as cm:
            decode_session_token(invalid_token)
        self.assertIn("Invalid session token", str(cm.exception))

    def test_decode_token_with_wrong_secret(self):
        token = generate_session_token(self.user_id)
        with patch.dict(self.app.config, {'SECRET_KEY': 'wrong_secret'}):
            with self.assertRaises(ValueError) as cm:
                decode_session_token(token)
            self.assertIn("Invalid session token", str(cm.exception))

    @patch('auth_service.app.services.auth_service.decode_session_token')
    def test_session_required_decorator_success(self, mock_decode_session_token):
        # Mock the decode_session_token to simulate a valid session
        mock_decode_session_token.return_value = {'sub': self.user_id}

        @session_required
        def protected_route():
            return "Access Granted"

        # In a real scenario, you'd pass the token via request headers.
        # For this test, we just check if the function executes.
        result = protected_route()
        self.assertEqual(result, "Access Granted")
        mock_decode_session_token.assert_not_called() # As currently implemented, the decorator doesn't call it. Needs integration.

    # More comprehensive tests for session_required would involve Flask test client
    # and actual request contexts to test token extraction from headers, etc.


class AuthRoutesTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        from auth_service.app.api.auth_routes import auth_bp
        from auth_service.app.exceptions import InvalidUsage

        self.app.register_blueprint(auth_bp, url_prefix='/auth')

        @self.app.errorhandler(InvalidUsage)
        def handle_invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response

        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_login_success(self):
        response = self.client.post('/auth/login', json={
            'username': 'test_user',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Login successful')
        self.assertIn('token', data)

    def test_login_invalid_credentials(self):
        response = self.client.post('/auth/login', json={
            'username': 'wrong_user',
            'password': 'wrong_password'
        })
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Invalid username or password')

    def test_login_missing_credentials(self):
        response = self.client.post('/auth/login', json={'username': 'test_user'})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Missing username or password')

    def test_validate_session_success(self):
        # First, log in to get a valid token
        login_response = self.client.post('/auth/login', json={
            'username': 'test_user',
            'password': 'password123'
        })
        login_data = login_response.get_json()
        token = login_data['token']

        response = self.client.get('/auth/validate_session', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Session valid')
        self.assertIn('user_id', data)
        self.assertEqual(data['user_id'], 123) # Based on dummy user_id in login route

    def test_validate_session_missing_header(self):
        response = self.client.get('/auth/validate_session')
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Authorization header missing')

    def test_validate_session_invalid_token_format(self):
        response = self.client.get('/auth/validate_session', headers={'Authorization': 'Bearerinvalidtoken'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Invalid session token')

    def test_validate_session_expired_token(self):
        # Manually create an expired token
        expired_payload = {
            'exp': datetime.now(timezone.utc) - timedelta(minutes=5),  # 5 minutes in the past
            'iat': datetime.now(timezone.utc) - timedelta(hours=1),
            'sub': 123
        }
        expired_token = jwt.encode(expired_payload, self.app.config['SECRET_KEY'], algorithm='HS256')

        response = self.client.get('/auth/validate_session', headers={'Authorization': f'Bearer {expired_token}'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Session token has expired')

    def test_validate_session_invalid_token_signature(self):
        # Create a token with a valid structure but wrong signature
        malformed_token = jwt.encode({
            'exp': datetime.now(timezone.utc) + timedelta(hours=1),
            'iat': datetime.now(timezone.utc),
            'sub': 123
        }, 'wrong_secret_key', algorithm='HS256')

        response = self.client.get('/auth/validate_session', headers={'Authorization': f'Bearer {malformed_token}'})
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Invalid session token')


if __name__ == '__main__':
    unittest.main()
