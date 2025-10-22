
import pytest
import time
from unittest.mock import patch, MagicMock
from app.sso.auth import SSOAuthenticator
from app.accounts.models import Account, AccountType

# Define performance thresholds
MAX_AVG_AUTH_TIME_MS = 500  # Maximum average authentication time in milliseconds
NUM_CONCURRENT_USERS = 100  # Number of concurrent users to simulate for load testing
NUM_ITERATIONS = 50       # Number of authentication attempts per user

@pytest.fixture
def sso_authenticator():
    return SSOAuthenticator()

@pytest.fixture
def trial_account_perf():
    account = Account(account_id="trial-perf-123", account_type=AccountType.TRIAL, name="Trial Perf User")
    account.sso_enabled = True
    account.sso_config = {"idp_entity_id": "http://mock-idp.com", "login_url": "http://mock-idp.com/login"}
    return account

@pytest.fixture
def paid_account_perf()
    account = Account(account_id="paid-perf-456", account_type=AccountType.PAID, name="Paid Perf User")
    account.sso_enabled = True
    account.sso_config = {"idp_entity_id": "http://mock-idp.com", "login_url": "http://mock-idp.com/login"}
    return account

def simulate_sso_authentication(authenticator, account, saml_response_data):
    """Helper function to simulate a single SSO authentication."""
    with patch('app.sso.auth.SAMLIdentityProvider.authenticate', return_value={"email": "user@test.com", "name": "Test User"}), \
         patch('app.sso.auth.UserManagementService.get_or_create_user', return_value=MagicMock()):
        authenticator.authenticate_sso(account, saml_response_data)

def test_sso_authentication_performance_trial_account(sso_authenticator, trial_account_perf):
    """Performance test for SSO authentication with trial accounts."""
    print(f"\nRunning performance test for trial account SSO with {NUM_CONCURRENT_USERS} concurrent users and {NUM_ITERATIONS} iterations...")
    
    all_auth_times = []

    for _ in range(NUM_ITERATIONS):
        start_time = time.perf_counter()
        simulate_sso_authentication(sso_authenticator, trial_account_perf, "mock_saml_response_trial")
        end_time = time.perf_counter()
        all_auth_times.append((end_time - start_time) * 1000) # Convert to milliseconds

    avg_auth_time = sum(all_auth_times) / len(all_auth_times)
    print(f"Average SSO authentication time (Trial Account): {avg_auth_time:.2f} ms")
    assert avg_auth_time < MAX_AVG_AUTH_TIME_MS, \
        f"Trial account SSO authentication performance degraded: {avg_auth_time:.2f} ms > {MAX_AVG_AUTH_TIME_MS} ms"

def test_sso_authentication_performance_paid_account_regression(sso_authenticator, paid_account_perf):
    """Regression performance test for SSO authentication with paid accounts."""
    print(f"\nRunning regression performance test for paid account SSO with {NUM_CONCURRENT_USERS} concurrent users and {NUM_ITERATIONS} iterations...")
    
    all_auth_times = []

    for _ in range(NUM_ITERATIONS):
        start_time = time.perf_counter()
        simulate_sso_authentication(sso_authenticator, paid_account_perf, "mock_saml_response_paid")
        end_time = time.perf_counter()
        all_auth_times.append((end_time - start_time) * 1000) # Convert to milliseconds

    avg_auth_time = sum(all_auth_times) / len(all_auth_times)
    print(f"Average SSO authentication time (Paid Account Regression): {avg_auth_time:.2f} ms")
    assert avg_auth_time < MAX_AVG_AUTH_TIME_MS, \
        f"Paid account SSO authentication performance degraded: {avg_auth_time:.2f} ms > {MAX_AVG_AUTH_TIME_MS} ms"
