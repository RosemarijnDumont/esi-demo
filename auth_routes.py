
from flask import Blueprint, request, jsonify
from auth_service import AuthService
import logging

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()

# Configure logging for the blueprint
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # In a real application, you'd verify username and password against a database
    # For this example, we'll use a simple hardcoded check
    if username == "user" and password == "password": # Replace with actual user validation
        user_id = "test_user_id"  # Replace with actual user ID from your user management system
        try:
            token = auth_service.generate_token(user_id)
            logging.info(f"User '{username}' logged in successfully.")
            return jsonify({"message": "Login successful", "token": token}), 200
        except Exception as e:
            logging.error(f"Error during token generation for user '{username}': {e}")
            return jsonify({"message": "Login failed due to server error."}), 500
    else:
        logging.warning(f"Failed login attempt for username: {username}")
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    data = request.get_json()
    user_id = data.get("user_id") # In a real app, this might come from a validated token

    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    
    try:
        new_token = auth_service.refresh_token(user_id)
        if new_token:
            logging.info(f"Token refreshed successfully for user_id: {user_id}")
            return jsonify({"message": "Token refreshed", "token": new_token}), 200
        else:
            logging.warning(f"Failed to refresh token for user_id: {user_id}. Token not found or invalid.")
            return jsonify({"message": "Could not refresh token. User session not found or invalid."}), 401
    except Exception as e:
            logging.error(f"Error refreshing token for user_id '{user_id}': {e}")
            return jsonify({"message": "Token refresh failed due to server error."}), 500
        

@auth_bp.route("/logout", methods=["POST"])
def logout():
    data = request.get_json()
    user_id = data.get("user_id") # In a real app, this would come from the current authenticated user
    
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400

    try:
        if auth_service.invalidate_token(user_id):
            logging.info(f"User '{user_id}' logged out successfully.")
            return jsonify({"message": "Logout successful"}), 200
        else:
            logging.warning(f"Failed to logout user '{user_id}'. Session not found.")
            return jsonify({"message": "Logout failed. User session not found."}), 404
    except Exception as e:
        logging.error(f"Error during logout for user '{user_id}': {e}")
        return jsonify({"message": "Logout failed due to server error."}), 500

