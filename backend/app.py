
from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Securely load API keys from environment variables
EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY")
EXTERNAL_API_BASE_URL = os.getenv("EXTERNAL_API_BASE_URL")

@app.route('/api/proxy/<path:external_path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(external_path):
    if not EXTERNAL_API_KEY or not EXTERNAL_API_BASE_URL:
        return jsonify({"error": "API keys or base URL not configured on server."}), 500

    # Construct the full URL for the external API
    external_url = f"{EXTERNAL_API_BASE_URL}/{external_path}"

    headers = {"x-api-key": EXTERNAL_API_KEY}
    
    # Pass through headers from the original request, excluding sensitive ones
    for header, value in request.headers:
        if header.lower() not in ['host', 'content-length', 'x-api-key']:
            headers[header] = value

    try:
        if request.method == 'GET':
            response = requests.get(external_url, headers=headers, params=request.args)
        elif request.method == 'POST':
            response = requests.post(external_url, headers=headers, json=request.json if request.is_json else request.data)
        elif request.method == 'PUT':
            response = requests.put(external_url, headers=headers, json=request.json if request.is_json else request.data)
        elif request.method == 'DELETE':
            response = requests.delete(external_url, headers=headers)
        else:
            return jsonify({"error": "Method not allowed"}), 405

        # Log the proxy request (can be expanded with more details)
        app.logger.info(f"Proxying {request.method} request to {external_url} - Status: {response.status_code}")

        # Return the external API's response to the client
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error proxying request to {external_url}: {e}")
        return jsonify({"error": "Failed to connect to external API.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
