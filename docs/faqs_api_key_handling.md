# FAQ: Secure API Key Handling

This document provides answers to frequently asked questions and troubleshooting tips related to the new secure API key handling mechanism.

## General Questions

### Q1: Why was this change made?
**A1:** This change was implemented to address a critical security vulnerability where API keys were discoverable in the browser's DevTools. Moving API key handling to the server-side significantly enhances security by preventing client-side exposure, helping us pass security audits and protect our services from unauthorized access and abuse.

### Q2: What's the main difference in how I use APIs now?
**A2:** The primary difference is that your client-side code will no longer directly send API keys to external services. Instead, you will make requests to our backend's secure proxy endpoints, and our server will securely add the API key before forwarding the request to the external service.

### Q3: Do I need to make changes to all my API calls?
**A3:** You need to change any client-side API calls that previously included an API key. Instead of calling the external service directly, you will now call the corresponding server-side proxy endpoint. API calls that never used an API key directly from the client are unaffected.

### Q4: Are there any performance implications with the server-side proxy?
**A4:** Introducing a server-side proxy adds a small amount of latency due to the additional hop (Client -> Our Backend -> Proxy -> External API). However, for most applications, this overhead is negligible. The security benefits significantly outweigh this minor performance impact.

## Development and Integration

### Q5: How do I know which proxy endpoint to use?
**A5:** Refer to the [API Documentation - Secure API Key Handling](link-to-api-documentation.md) document. It lists the available proxy endpoints and provides examples for common external services.

### Q6: How do I pass parameters to the external API through the proxy?
**A6:** Query parameters and request bodies (for `POST`/`PUT` requests) sent to the proxy endpoint will generally be passed through to the external API. For example, `GET /api/proxy/googlemaps/geocode/json?address=1600+Amphitheatre+Parkway` will forward `address=1600+Amphitheatre+Parkway` to Google Maps.

### Q7: Where are the API keys stored now?
**A7:** API keys are stored securely as environment variables on the server where our backend application is deployed. In production, we utilize dedicated secrets management services (e.g., AWS Secrets Manager, Google Secret Manager). **They are never stored on the client-side.**

### Q8: Can I still test external APIs directly during development?
**A8:** While it's generally discouraged to expose API keys, for specific local development and debugging scenarios, you *might* temporarily use API keys directly if they are restricted to development environments and never committed to version control. However, it's highly recommended to develop and test against the full proxy flow to ensure consistent behavior with production.

## Troubleshooting

### T1: My API call is failing with a 404 or unknown service error.
**_Possible Causes:_**
*   **Incorrect Proxy Endpoint:** You might be using the wrong proxy path (e.g., `/api/proxy/my-service/` instead of the correct `/api/proxy/googlemaps/`).
*   **Missing Proxy Configuration:** The specific external service you're trying to reach might not yet be configured in the server-side proxy logic.

**_Troubleshooting Steps:_**
1.  Verify the proxy endpoint in your client code against the [API Documentation](link-to-api-documentation.md).
2.  Check the server logs for messages indicating an unknown service or a routing error.
3.  If you suspect a missing configuration, contact the backend development team.

### T2: I'm getting a 401/403 Unauthorized error from the external API.
**_Possible Causes:_**
*   **Missing or Incorrect Server-Side API Key:** The API key configured on the backend for the specific service might be missing, incorrect, or revoked.
*   **External API's Rate Limit/Quota Exceeded:** The external API might be returning an authorization error if the configured key has hit its usage limits.
*   **Incorrect API Key Injection Logic:** There might be an issue in the server-side proxy where the API key is not being correctly injected into the request (e.g., wrong header, query parameter name).

**_Troubleshooting Steps:_**
1.  Verify that the corresponding environment variable for the API key is correctly set on the server.
2.  Check the external service's dashboard for API key status and usage.
3.  Review the server-side proxy code to ensure the API key is being injected correctly for that specific service.
4.  Check network tab / server logs for specific messages from the external API.

### T3: My client-side API calls are taking too long or timing out.
**_Possible Causes:_**
*   **Network Latency:** Increased network latency between our server and the external API.
*   **External API Performance Issues:** The external API itself might be slow to respond.
*   **Server-Side Processing Overhead:** While typically small, heavy server-side processing or resource contention on our backend could contribute.

**_Troubleshooting Steps:_**
1.  Monitor the performance of the external API using their provided tools or dashboards.
2.  Check our backend server's resource utilization (CPU, memory) to ensure it's not under stress.
3.  Review server logs for any long-running operations or bottlenecks within the proxy logic.

### T4: I'm seeing an internal server error (500) from the proxy endpoint.
**_Possible Causes:_**
*   **Server-Side Proxy Error:** An unhandled error occurred within the proxy logic on our backend.
*   **Upstream Connection Issues:** Our server might be unable to connect to the external API.

**_Troubleshooting Steps:_**
1.  Immediately check the server logs for detailed error messages and stack traces. This is the most crucial step for a 500 error.
2.  Ensure the backend server has proper outbound network access to the external API's domain.

---

*Last Updated: 2023-10-27*