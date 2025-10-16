
import pytest
from app.services.auth import AuthService
from app.models.user import User

@pytest.fixture
def auth_service():
    return AuthService()

def test_valid_login(auth_service):
    # Assuming a mock or test database setup where a user exists
    user = auth_service.login("testuser", "password123")
    assert isinstance(user, User)
    assert user.username == "testuser"

def test_invalid_credentials(auth_service):
    with pytest.raises(ValueError, match="Invalid credentials"):
        auth_service.login("testuser", "wrongpassword")

def test_session_token_generation_and_validation(auth_service):
    user = auth_service.login("testuser", "password123")
    token = auth_service.generate_session_token(user)
    assert auth_service.validate_session_token(token) == user.id

def test_invalid_session_token(auth_service):
    with pytest.raises(ValueError, match="Invalid session token"):
        auth_service.validate_session_token("invalid_token")
