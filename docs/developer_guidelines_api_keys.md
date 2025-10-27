# Developer Guidelines: Secure API Key Handling

## Overview

These guidelines outline the mandatory procedures for handling API keys within our applications, emphasizing a server-side-only approach to prevent exposure in client environments. Adhering to these guidelines is crucial for maintaining the security posture of our systems and ensuring compliance with security standards.

## 1. No Client-Side API Key Exposure (CRITICAL)

**NEVER embed, hardcode, or directly expose API keys in any client-side code (JavaScript, mobile apps, frontend configurations, etc.).** This includes:

*   Directly including API keys in frontend JavaScript files.
*   Using API keys in URLs or request parameters from client-side code.
*   Storing API keys in local storage, session storage, cookies, or any other client-side storage mechanism.
*   Committing API keys to client-side version control.

**Rationale:** Client-side exposure allows attackers to easily extract API keys via browser DevTools, network inspection, or code analysis, leading to unauthorized access, abuse, and potential financial costs.

## 2. All API Key Dependent Requests MUST Go Through a Server-Side Proxy

Any interaction with external services that require an API key must be routed through a dedicated server-side proxy. The client application will make a request to our backend, which in turn will call the server-side proxy.

### New Request Flow

1.  **Client initiates request:** The client application (web or mobile) makes a standard HTTP request to a *backend endpoint within our application*.
    *   **Crucially:** This client request **does not** contain the API key.
2.  **Backend receives request:** Our backend application receives the client's request.
3.  **Backend calls Server-Side Proxy:** The backend processes the request and forwards it to the *secure API proxy component*.
4.  **Proxy injects API Key:** The secure API proxy retrieves the necessary API key from a secure server-side storage (environment variables/secrets management).
5.  **Proxy forwards to External API:** The proxy constructs the request, injecting the API key (e.g., in a header or query parameter, as required by the external API), and sends it to the external third-party service.
6.  **Proxy returns response:** The proxy receives the response from the external API and forwards it back to our backend.
7.  **Backend sends response to client:** Our backend processes the response and sends it back to the client application.

## 3. Secure API Key Storage on the Server

API keys must be stored securely on the server and accessed only by the server-side proxy.

*   **Environment Variables:** For local development and some simple deployments, store API keys as environment variables (e.g., using `dotenv` for local `.env` files, but *never commit .env to repo*).
    *   `APPLICATION_SERVICE_API_KEY=your_secret_key`
*   **Secrets Management Services:** For production environments, utilize dedicated secrets management solutions provided by your cloud provider (e.g., AWS Secrets Manager, Google Secret Manager, Azure Key Vault) or container orchestration platforms (e.g., Kubernetes Secrets).

**NEVER hardcode API keys directly into server-side code.** They should be loaded dynamically at runtime.

## 4. Naming Conventions for API Keys

Use clear and consistent naming conventions for environment variables storing API keys. Prefix them with the service or application name.

*   `GOOGLE_MAPS_API_KEY`
*   `STRIPE_SECRET_KEY`
*   `WEATHER_API_KEY`

## 5. Auditing and Monitoring

Implement logging for all requests made through the API proxy. Ensure logs capture request details (origin, timestamp, target service) but **NEVER the API key itself or sensitive response data.** Monitor for unusual activity or excessive API calls.

## 6. Access Control

Ensure that the backend endpoints that trigger API proxy calls are properly secured with appropriate authentication and authorization checks. Only authorized users or services should be able to initiate requests that ultimately use a sensitive API key.

## 7. Code Review

All code changes involving API key handling, or new integrations with external APIs, must undergo a rigorous code review process to ensure these guidelines are followed.

---

*Last Updated: 2023-10-27*