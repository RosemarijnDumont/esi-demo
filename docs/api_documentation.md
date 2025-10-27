# API Documentation - Secure API Key Handling

## Overview
This document outlines the updated process for handling API keys, transitioning from client-side requests to a secure server-side proxy. This change addresses critical security vulnerabilities where API keys were previously exposed in browser DevTools.

## Changes to Existing API Endpoints
All API endpoints that previously required API keys directly from the client are now routed through a server-side proxy. Clients will no longer include API keys in their requests. The server-side proxy will securely inject the necessary API keys before forwarding the request to the external service.

### Example: Old Client-Side Request (DEPRECATED)
```javascript
fetch(`https://api.example.com/data?apiKey=${YOUR_API_KEY}`);
```

### Example: New Client-Side Request
```javascript
fetch(`/api/proxy/data`); // The API key is added by the server-side proxy
```

## New Server-Side Proxy Endpoints

To access external APIs that require keys, client applications should now make requests to the following server-side proxy endpoints. The proxy will handle the secure injection of API keys. Each external API requiring a key will have a corresponding proxy endpoint.

### General Proxy Endpoint Structure
`/api/proxy/{external_api_path}`

**Example:** To access `https://external-service.com/api/v1/resource`, the client would make a request to `/api/proxy/external-service/api/v1/resource`.

### Available Proxy Endpoints (Example)

*   **`/api/proxy/googlemaps/{endpoint}`**
    *   **Description:** Proxies requests to the Google Maps API.
    *   **Method:** `GET`, `POST`
    *   **Request Body/Query Parameters:** Pass through directly to the Google Maps API.
    *   **Example Usage:**
        ```javascript
        fetch('/api/proxy/googlemaps/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA')
            .then(response => response.json())
            .then(data => console.log(data));
        ```

*   **`/api/proxy/weatherapi/{endpoint}`**
    *   **Description:** Proxies requests to the Weather API.
    *   **Method:** `GET`
    *   **Request Body/Query Parameters:** Pass through directly to the Weather API.
    *   **Example Usage:**
        ```javascript
        fetch('/api/proxy/weatherapi/current?city=London')
            .then(response => response.json())
            .then(data => console.log(data));
        ```

## Authentication and Authorization for Proxy Endpoints

Access to the server-side proxy endpoints should be secured using your application's standard authentication and authorization mechanisms (e.g., session cookies, JWTs). The proxy itself does not handle user authentication, but rather acts as a secure intermediary for API key management.

---

*Last Updated: 2023-10-27*