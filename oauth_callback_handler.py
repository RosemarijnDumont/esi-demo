
import os
import json
import hmac
import hashlib
import base64
from urllib.parse import urlencode, urlparse, parse_qs

# --- Configuration --- 
CLIENT_SECRETS = {
    "github": os.getenv("GITHUB_CLIENT_SECRET"),
    "google": os.getenv("GOOGLE_CLIENT_SECRET"),
    # Add other OAuth providers here
}

# In a real application, this would be a secure, long-lived key fetched from a secrets manager
# For demonstration, using an env var. 
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "super-secret-session-key-for-dev") 

# This should be a database or a secure cache in a production environment
# For this example, we'll use a simple in-memory dict.
ACTIVE_OAUTH_STATES = {}

# --- Helper Functions ---

def generate_state_parameter(user_session_id: str, provider: str) -> str:
    """
    Generates a cryptographically secure state parameter to prevent CSRF attacks.
    The state includes a hash of the user's session ID and the provider to ensure
    it's tied to the specific user and OAuth flow.
    """
    nonce = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8').rstrip('=')
    data_to_hash = f"{user_session_id}-{provider}-{nonce}".encode('utf-8')
    
    # Using HMAC for integrity and authenticity
    signature = hmac.new(SESSION_SECRET_KEY.encode('utf-8'), data_to_hash, hashlib.sha256).hexdigest()
    
    state_payload = {
        "nonce": nonce,
        "provider": provider,
        "signature": signature
    }
    
    encoded_state = base64.urlsafe_b64encode(json.dumps(state_payload).encode('utf-8')).decode('utf-8').rstrip('=')
    ACTIVE_OAUTH_STATES[encoded_state] = user_session_id # Store active states for validation
    return encoded_state

def validate_state_parameter(state: str, user_session_id: str) -> bool:
    """
    Validates the received state parameter to ensure it matches a known, active state
    and is valid for the current user's session.
    """
    if state not in ACTIVE_OAUTH_STATES or ACTIVE_OAUTH_STATES[state] != user_session_id:
        print(f"State mismatch or not found for session {user_session_id}")
        return False

    try:
        # Add padding back if missing
        missing_padding = len(state) % 4
        if missing_padding:
            state += '='* (4 - missing_padding)

        decoded_payload_bytes = base64.urlsafe_b64decode(state.encode('utf-8'))
        state_payload = json.loads(decoded_payload_bytes.decode('utf-8'))
    except (json.JSONDecodeError, base64.binascii.Error) as e:
        print(f"Error decoding state parameter: {e}")
        return False

    nonce = state_payload.get("nonce")
    provider = state_payload.get("provider")
    signature = state_payload.get("signature")

    if not all([nonce, provider, signature]):
        print("Missing components in state payload.")
        return False

    data_to_hash = f"{user_session_id}-{provider}-{nonce}".encode('utf-8')
    expected_signature = hmac.new(SESSION_SECRET_KEY.encode('utf-8'), data_to_hash, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_signature, signature):
        print("State signature mismatch.")
        return False

    # Remove the state after successful validation to prevent replay attacks
    del ACTIVE_OAUTH_STATES[state]
    return True

def handle_oauth_callback(provider: str, query_params: dict, user_session_id: str) -> dict:
    """
    Handles the OAuth callback from various providers.
    This function would typically interact with a real HTTP request/response object.
    
    Args:
        provider (str): The OAuth provider (e.g., 'github', 'google').
        query_params (dict): A dictionary of query parameters from the callback URL.
        user_session_id (str): The unique identifier for the user's session.

    Returns:
        dict: A dictionary containing the success status and a message or data.
    """
    
    code = query_params.get("code")
    state = query_params.get("state")
    error = query_params.get("error")
    error_description = query_params.get("error_description")

    if error:
        print(f"OAuth error from {provider}: {error} - {error_description}")
        return {"success": False, "message": f"OAuth error: {error_description or error}"}

    if not code:
        print(f"No authorization code received for {provider}")
        return {"success": False, "message": "Authorization code missing."}

    if not state:
        print("State parameter missing in callback. Possible CSRF.")
        return {"success": False, "message": "State parameter missing. Please try again."}

    if not validate_state_parameter(state, user_session_id):
        print(f"Invalid or expired state parameter for {provider}. Session ID: {user_session_id}")
        return {"success": False, "message": "Invalid or expired state. Please try again."}

    # --- Exchange authorization code for access token --- 
    # In a real application, this would involve an HTTP POST request to the provider's
    # token endpoint. For this example, we'll simulate it. 
    
    client_secret = CLIENT_SECRETS.get(provider)
    if not client_secret:
        print(f"Client secret not configured for provider: {provider}")
        return {"success": False, "message": "OAuth provider not configured."}

    # Simulate token exchange (replace with actual API call)
    print(f"\n--- Simulating token exchange for {provider} ---")
    print(f"  Provider: {provider}")
    print(f"  Authorization Code: {code}")
    # print(f"  Client Secret: {'*' * len(client_secret)}") # Don't log secrets in production
    print(f"  Redirect URI: (dynamic or pre-configured based on setup)")
    print(f"  Grant Type: authorization_code")
    
    # Example of what you'd get back from a successful token exchange
    access_token_data = {
        "access_token": f"mock_access_token_for_{provider}_{code}",
        "token_type": "bearer",
        "expires_in": 3600,
        "scope": "user,email", # Example scopes
        "refresh_token": f"mock_refresh_token_for_{provider}_{code}" # Optional
    }
    print(f"  Simulated Token Response: {json.dumps(access_token_data, indent=2)}")
    print(f"--- End Simulation ---\n")

    # --- Further steps: Store token, retrieve user profile, link account ---
    # In a real application:
    # 1. Store the access_token and refresh_token securely, associated with user_session_id.
    # 2. Use the access_token to fetch user profile information from the OAuth provider (e.g., /userinfo or /me).
    # 3. Link the external user ID from the provider to your internal user account.
    # 4. Redirect the user to a success page or dashboard.

    print(f"Successfully handled OAuth callback for {provider} for session {user_session_id}.")
    return {"success": True, "message": "OAuth connection successful!", "data": access_token_data}

# --- Example Usage (Simulated) ---
if __name__ == "__main__":
    # Simulate environment variables
    os.environ["GITHUB_CLIENT_SECRET"] = "gh_mock_client_secret_123"
    os.environ["GOOGLE_CLIENT_SECRET"] = "g_mock_client_secret_456"
    os.environ["SESSION_SECRET_KEY"] = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')

    print("--- Starting OAuth Callback Handler Simulation ---")

    # --- Scenario 1: Successful GitHub OAuth Flow ---
    print("\n### Scenario 1: Successful GitHub OAuth Flow ###")
    user_session_id_github = "user_session_123"
    
    # 1. User initiates OAuth, state is generated
    github_state = generate_state_parameter(user_session_id_github, "github")
    print(f"Generated GitHub State: {github_state}")

    # 2. GitHub redirects back to our callback URL with code and state
    mock_github_query_params_success = {
        "code": "mock_github_auth_code_xyz",
        "state": github_state
    }
    print(f"Mock GitHub Callback Params (Success): {mock_github_query_params_success}")

    github_result_success = handle_oauth_callback("github", mock_github_query_params_success, user_session_id_github)
    print(f"GitHub Callback Result (Success): {json.dumps(github_result_success, indent=2)}")
    assert github_result_success["success"] is True

    # --- Scenario 2: Successful Google OAuth Flow ---
    print("\n### Scenario 2: Successful Google OAuth Flow ###")
    user_session_id_google = "user_session_456"

    # 1. User initiates OAuth, state is generated
    google_state = generate_state_parameter(user_session_id_google, "google")
    print(f"Generated Google State: {google_state}")

    # 2. Google redirects back to our callback URL with code and state
    mock_google_query_params_success = {
        "code": "mock_google_auth_code_abc",
        "state": google_state
    }
    print(f"Mock Google Callback Params (Success): {mock_google_query_params_success}")

    google_result_success = handle_oauth_callback("google", mock_google_query_params_success, user_session_id_google)
    print(f"Google Callback Result (Success): {json.dumps(google_result_success, indent=2)}")
    assert google_result_success["success"] is True

    # --- Scenario 3: Missing Code Parameter ---
    print("\n### Scenario 3: Missing Code Parameter ###")
    user_session_id_invalid = "user_session_789"
    invalid_state = generate_state_parameter(user_session_id_invalid, "github") # Generate a valid state first
    mock_params_no_code = {"state": invalid_state}
    result_no_code = handle_oauth_callback("github", mock_params_no_code, user_session_id_invalid)
    print(f"Result (No Code): {json.dumps(result_no_code, indent=2)}")
    assert result_no_code["success"] is False
    assert "Authorization code missing" in result_no_code["message"]

     # --- Scenario 4: Missing State Parameter (Potential CSRF) ---
    print("\n### Scenario 4: Missing State Parameter (Potential CSRF) ###")
    mock_params_no_state = {"code": "some_code"}
    result_no_state = handle_oauth_callback("github", mock_params_no_state, user_session_id_github)
    print(f"Result (No State): {json.dumps(result_no_state, indent=2)}")
    assert result_no_state["success"] is False
    assert "State parameter missing" in result_no_state["message"]

    # --- Scenario 5: Invalid/Mismatched State Parameter ---
    print("\n### Scenario 5: Invalid/Mismatched State Parameter ###")
    mock_params_invalid_state = {
        "code": "some_code",
        "state": "invalid_or_manipulated_state_123"
    }
    result_invalid_state = handle_oauth_callback("github", mock_params_invalid_state, user_session_id_github)
    print(f"Result (Invalid State): {json.dumps(result_invalid_state, indent=2)}")
    assert result_invalid_state["success"] is False
    assert "Invalid or expired state" in result_invalid_state["message"]

    # --- Scenario 6: Expired/Used State Parameter (Replay Attack) ---
    print("\n### Scenario 6: Expired/Used State Parameter (Replay Attack) ###")
    user_session_id_replay = "user_session_replay"
    replay_state = generate_state_parameter(user_session_id_replay, "google")
    print(f"Generated Replay State: {replay_state}")

    # First use (should succeed)
    mock_replay_params_first_use = {"code": "first_code", "state": replay_state}
    result_first_use = handle_oauth_callback("google", mock_replay_params_first_use, user_session_id_replay)
    print(f"Result (Replay First Use): {json.dumps(result_first_use, indent=2)}")
    assert result_first_use["success"] is True

    # Second use of the *same* state (should fail as it's been removed)
    result_second_use = handle_oauth_callback("google", mock_replay_params_first_use, user_session_id_replay)
    print(f"Result (Replay Second Use): {json.dumps(result_second_use, indent=2)}")
    assert result_second_use["success"] is False
    assert "Invalid or expired state" in result_second_use["message"]

    # --- Scenario 7: OAuth Provider Reports Error ---
    print("\n### Scenario 7: OAuth Provider Reports Error ###")
    user_session_id_error_provider = "user_session_error_provider"
    mock_params_provider_error = {
        "error": "access_denied",
        "error_description": "The user denied the request."
    }
    result_provider_error = handle_oauth_callback("github", mock_params_provider_error, user_session_id_error_provider)
    print(f"Result (Provider Error): {json.dumps(result_provider_error, indent=2)}")
    assert result_provider_error["success"] is False
    assert "access_denied" in result_provider_error["message"]

    print("\n--- OAuth Callback Handler Simulation Complete ---")
