# API Documentation: Server-Side Proxy Endpoints

To enhance security and protect sensitive API keys from client-side exposure, certain API integrations now leverage server-side proxy endpoints. This document outlines the usage and behavior of these new endpoints.

## General Principles

*   **Client-side calls your backend:** Your client-side application will no longer directly call third-party APIs that require sensitive keys. Instead, it will make requests to a dedicated endpoint on our backend.
*   **Backend handles external communication:** Our backend service will securely store the necessary API keys, construct the request to the external API, make the call, and then return the sanitized response to your client.
*   **No API Keys on Client:** No API keys for these integrated services will ever be exposed to the client-side browser or application.

## Available Proxy Endpoints

### 1. `GET /api/proxy/external-service`

This endpoint proxies requests to the `https://api.example.com/data` external API, which requires a sensitive API key. 

#### Parameters

This endpoint currently accepts no client-side parameters. All necessary parameters for the external API call are configured on the server-side.

#### Example Request (Client-Side)

```javascript
fetch('/api/proxy/external-service', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        // Include any authentication headers for your backend if required
        'Authorization': 'Bearer <YOUR_BACKEND_AUTH_TOKEN>'
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
})
.then(data => {
    console.log('Data from external service:', data);
})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error);
});
```

#### Example Response (Success - 200 OK)

```json
{
    