
import unittest
import json
from app import app
from auth_service import AuthService

class TestAuthentication(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.auth_service = AuthService()

    def test_a_user_login_success(self):
        response = self.app.post(
            "/auth/login",
            data=json.dumps({"username": "user", "password": "password"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("token", data)
        self.assertEqual(data["message"], "Login successful")
        self.user_token = data["token"] # Store token for subsequent tests

    def test_b_user_login_failure(self):
        response = self.app.post(
            "/auth/login",
            data=json.dumps({"username": "user", "password": "wrong_password"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data["message"], "Invalid credentials")

    def test_c_token_validation_success(self):
        # First, log in to get a valid token
        login_response = self.app.post(
            "/auth/login",
            data=json.dumps({"username": "user", "password": "password"}),
            content_type="application/json"
        )
        token = json.loads(login_response.data)["token"]

        # Now, try to validate it (e.g., call a protected endpoint - here we just use the service directly)
        user_id = self.auth_service.validate_token(token)
        self.assertIsNotNone(user_id)
        self.assertEqual(user_id, "test_user_id")

    def test_d_token_validation_failure_invalid_token(self):
        invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        user_id = self.auth_service.validate_token(invalid_token)
        self.assertIsNone(user_id)

    def test_e_token_refresh_success(self):
        # Log in to get an initial token
        login_response = self.app.post(
            "/auth/login",
            data=json.dumps({"username": "user", "password": "password"}),
            content_type="application/json"
        )
        initial_token = json.loads(login_response.data)["token"]
        initial_user_id = self.auth_service.validate_token(initial_token)

        # Refresh the token for the same user_id
        refresh_response = self.app.post(
            "/auth/refresh",
            data=json.dumps({"user_id": initial_user_id}),
            content_type="application/json"
        )
        self.assertEqual(refresh_response.status_code, 200)
        data = json.loads(refresh_response.data)
        self.assertIn("token", data)
        self.assertNotEqual(initial_token, data["token"])
        self.assertEqual(data["message"], "Token refreshed")

    def test_f_token_refresh_failure_no_user_id(self):
        response = self.app.post(
            "/auth/refresh",
            data=json.dumps({}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("User ID is required", json.loads(response.data)["message"])

    def test_g_user_logout_success(self):
        # Log in first to have a session to logout from
        login_response = self.app.post(
            "/auth/login",
            data=json.dumps({"username": "user", "password": "password"}),
            content_type="application/json"
        )
        token = json.loads(login_response.data)["token"]
        user_id = self.auth_service.validate_token(token)
       
        # Now logout
        logout_response = self.app.post(
            "/auth/logout",
            data=json.dumps({"user_id": user_id}),
            content_type="application/json"
        )
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(json.loads(logout_response.data)["message"], "Logout successful")
        
        # Assert that the token is no longer valid after logout
        self.assertIsNone(self.auth_service.validate_token(token))

    def test_h_user_logout_failure_not_logged_in(self):
        # Attempt to logout a user that isn't logged in
        response = self.app.post(
            "/auth/logout",
            data=json.dumps({"user_id": "nonexistent_user"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)["message"],"Logout failed. User session not found.")

if __name__ == '__main__':
    unittest.main()