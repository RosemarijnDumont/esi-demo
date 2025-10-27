# API Key Security Enhancement

This project implements a critical security enhancement to protect API keys from exposure in browser DevTools. Previously, API keys were directly used in client-side requests, making them visible in network traffic.

## Solution Overview

The solution involves transitioning all sensitive API key requests to a server-side proxy. The frontend now communicates with a new backend endpoint, which then securely injects API keys and forwards the requests to the intended third-party APIs.

## Key Components

### Backend (Python Flask)

- **`server/app.py`**: Contains the Flask application with the new `/api/proxy` endpoint. This endpoint receives requests from the frontend, retrieves API keys securely from environment variables, and forwards them to the respective third-party services. It also includes basic rate limiting, logging, and error handling.
- **`server/config.py`**: Configuration file for the Flask application.
- **`server/requirements.txt`**: Lists the Python dependencies.

### Frontend (JavaScript - Example)

- **`client/src/services/api.js`**: An example JavaScript service demonstrating how the frontend should now interact with the new backend proxy endpoint.

## Setup and Running

### 1. Environment Variables

Before running the server, you **must** set the following environment variables with your actual API keys:

```bash
export THIRD_PARTY_API_KEY="your_third_party_api_key_here"
export FOURTH_PARTY_API_KEY="your_fourth_party_api_key_here"
```

### 2. Backend Setup

Navigate to the `server` directory:

```bash
cd server
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the Flask application:

```bash
flask run
```

The server will typically run on `http://127.0.0.1:5000`.

### 3. Frontend Integration (Example)

Refer to `client/src/services/api.js` for an example of how to modify your frontend to use the new proxy endpoint.

Ensure your frontend is configured to send requests to the `/api/proxy` endpoint on your backend server. You might need to configure a proxy in your frontend development server (e.g., `package.json` for React apps) or set `REACT_APP_API_BASE_URL` in your frontend's environment variables.

**Example `client/src/App.js` usage:**

```javascript
import React, { useEffect, useState } from 'react';
import apiService from './services/api';

function App() {
  const [dataA, setDataA] = useState(null);
  const [dataB, setDataB] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Example: Fetch data from service_a
        const resultA = await apiService.getServiceAData('some-id');
        setDataA(resultA);

        // Example: Post data to service_b
        const postData = { name: 'test', value: 123 };
        const resultB = await apiService.postServiceBData(postData);
        setDataB(resultB);

      } catch (err) {
        setError(err.message);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>API Proxy Example</h1>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      <h2>Service A Data:</h2>
      <pre>{dataA ? JSON.stringify(dataA, null, 2) : 'Loading...'}</pre>

      <h2>Service B Data:</h2>
      <pre>{dataB ? JSON.stringify(dataB, null, 2) : 'Loading...'}</pre>
    </div>
  );
}

export default App;
```

## Rate Limiting

The backend proxy implements a basic in-memory rate limiting mechanism (50 requests per minute per IP address). This helps prevent abuse of the proxy endpoint.

## Error Handling and Logging

Robust error handling is implemented to gracefully manage issues during request processing and forwarding. Critical events and errors are logged to provide visibility into the proxy's operation.

## Security Considerations

- **API Keys**: Stored in environment variables and accessed only server-side.
- **HTTPS**: Ensure your frontend and backend communications are over HTTPS in production.
- **Input Validation**: While the proxy forwards requests, consider additional input validation on the backend if the third-party API is sensitive to malformed data.
- **CORS**: Configure CORS appropriately for your Flask application if your frontend and backend are on different domains.

## Future Enhancements

- **Advanced Rate Limiting**: Implement more sophisticated rate limiting (e.g., Redis-backed).
- **Caching**: Add caching mechanisms for frequently accessed third-party API data.
- **More Granular Access Control**: Implement user-specific access control for different third-party services.
- **Centralized Secrets Management**: Integrate with a secrets management service (e.g., AWS Secrets Manager, HashiCorp Vault) for API keys in a production environment.
 