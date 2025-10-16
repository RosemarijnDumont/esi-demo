
import pytest
from app.services.auth import AuthService
from app.services.data_sync import DataSyncService

# Assuming previous bug fixes are now part of the core logic and we are testing against them

@pytest.fixture
def auth_service():
    return AuthService()

@pytest.fixture
def data_sync_service():
    return DataSyncService()

def test_login_stability_regression(auth_service):
    # Test to ensure "Invalid session token" error does not reappear after fix
    user = auth_service.login("testuser", "password123")
    token = auth_service.generate_session_token(user)
    assert auth_service.validate_session_token(token) == user.id
    # Further attempts to log in multiple times or with slight variations

def test_dashboard_load_time_regression(data_sync_service):
    # This would require integration with a performance monitoring tool or an explicit API endpoint
    # which returns load time. For now, a placeholder assertion.
    start_time = data_sync_service.get_dashboard_load_time("testuser") # Assuming such a method exists
    assert start_time <= 3.0 # Ensures it loads within 3 seconds

def test_mobile_sync_regression(data_sync_service):
    # Ensure data sync remains immediate and consistent
    mobile_entry = {"user_id": 1, "content": "Regression Mobile Entry"}
    synced_entry = data_sync_service.sync_mobile_entry(mobile_entry)
    assert synced_entry.content == mobile_entry["content"]
    # Assert immediate visibility in web app (via mock or shared state)
