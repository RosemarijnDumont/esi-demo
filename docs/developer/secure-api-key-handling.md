# Secure API Key Handling (Server-Side Only)

## Overview

This document outlines the updated procedure for securely handling and accessing API keys within our applications. To mitigate the risk of API keys being exposed in client-side environments (e.g., browser DevTools), all API requests requiring sensitive keys must now be made from the server-side.

## Principles

*   **Never expose API keys to the client-side:** API keys are sensitive credentials and should never be directly embedded in client-side code, sent as part of client-side requests, or exposed through any client-side accessible means.
*   **Server-side proxying:** All API requests that require sensitive API keys must be proxied through our backend services. The backend service will be responsible for securely storing and injecting the API keys into the outgoing requests to the third-party APIs.
*   **Environment Variables:** API keys on the server-side should be stored as environment variables and loaded at application startup. This prevents hardcoding keys directly into the codebase and allows for easy rotation and management across different environments.
*   **Least Privilege:** Ensure that the server-side components accessing API keys have only the necessary permissions to perform their intended function.
*   **Logging and Monitoring:** Implement robust logging and monitoring for all server-side API key usage to detect and respond to any unauthorized access attempts or suspicious activity.

## Implementation Guidelines

### 1. Storing API Keys

*   **Production:** In production environments, API keys must be stored in a secure secrets management system (e.g., AWS Secrets Manager, Google Cloud Secret Manager, HashiCorp Vault) and injected into the application's environment variables at deployment time.
*   **Development/Staging:** For development and staging environments, API keys can be stored in `.env` files (which must be excluded from version control via `.gitignore`) and loaded using a library like `python-dotenv` or similar for your chosen language/framework.

### 2. Making Server-Side API Requests

All API calls that require sensitive keys must be routed through a dedicated backend endpoint. Here's a conceptual example:

**Incorrect (Client-side exposure):**

```javascript
// Client-side JavaScript
const apiKey = "YOUR_API_KEY_HERE"; // Exposed!
fetch(`https://api.example.com/data?key=${apiKey}`)
  .then(response => response.json())
  .then(data => console.log(data));
```

**Correct (Server-side proxy):**

```javascript
// Client-side JavaScript (calls your backend)
fetch('/api/proxy/external-service') // Your backend handles the API call
  .then(response => response.json())
  .then(data => console.log(data));
```

```python
# Server-side Python (Flask example)
import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/proxy/external-service')
def proxy_external_service():
    api_key = os.environ.get("EXTERNAL_SERVICE_API_KEY")
    if not api_key:
        return jsonify({"error": "API key not configured"}), 500

    # Make the actual request to the external API
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get("https://api.example.com/data", headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors

    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
```

### 3. Securing Backend Endpoints

Ensure that your server-side proxy endpoints are themselves secured. Implement proper authentication and authorization mechanisms to ensure only authorized client applications or users can access these proxy endpoints.

### 4. Rotating API Keys

Regularly rotate your API keys. Refer to the documentation of the respective third-party API provider for their key rotation procedures.

## References

*   [OWASP Top 10 - Sensitive Data Exposure](https://owasp.org/www-project-top-ten/OWASP_Top_Ten_2017/0x3-Sensitive_Data_Exposure)
*   [Your team's secrets management solution documentation]

## Contact

For any questions regarding secure API key handling, please contact the Security Team.
