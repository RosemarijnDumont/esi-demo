import os
import logging
from flask import Flask, request, jsonify, abort
import requests
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Securely load API keys from environment variables
THIRD_PARTY_API_KEY = os.environ.get("THIRD_PARTY_API_KEY")
FOURTH_PARTY_API_KEY = os.environ.get("FOURTH_PARTY_API_KEY")

# Define allowed third-party services and their base URLs
THIRD_PARTY_SERVICES = {
    "service_a": {
        "base_url": "https://api.thirdparty.com/service_a",
        "api_key": THIRD_PARTY_API_KEY,
        "headers": {"Authorization": f"Bearer {THIRD_PARTY_API_KEY}"}
    },
    "service_b": {
        "base_url": "https://api.fourthparty.com/service_b",
        "api_key": FOURTH_PARTY_API_KEY,
        "headers": {"X-Api-Key": FOURTH_PARTY_API_KEY}
    }
}

@app.before_request
def log_request_info():
    """Logs incoming request information."""
    app.logger.info(f