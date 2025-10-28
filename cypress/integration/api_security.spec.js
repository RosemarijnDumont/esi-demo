describe('API Security Tests', () => {
  it('should not expose API keys in network requests', () => {
    cy.intercept('GET', '/api/proxy/**').as('proxiedApiCall');
    cy.visit('/'); // Visit the application

    // Trigger an action that makes an API call, e.g., waiting for data to load
    cy.wait('@proxiedApiCall').then((interception) => {
      // Assert that the request was made to the proxy endpoint
      expect(interception.request.url).to.include('/api/proxy');
      // Further checks can be added here if specific headers or body content are expected

      // Intercept all network requests and check for sensitive information
      cy.window().then((win) => {
        const performance = win.performance;
        const resources = performance.getEntriesByType('resource');

        resources.forEach(resource => {
          // This is a basic check. More sophisticated checks might involve parsing 
          // request bodies/headers if they were improperly exposed.
          expect(resource.name).to.not.include('YOUR_SENSITIVE_API_KEY'); // Replace with actual sensitive key strings
        });
      });

      // You might need to directly inspect network requests in a more advanced way
      // For example, by using browser developer tools protocol directly if Cypress allows.
    });
  });

  it('should ensure API requests are routed through the server-side proxy', () => {
    cy.intercept('GET', '/api/proxy/external-service/some-resource').as('getProxiedData');
    cy.visit('/');
    cy.wait('@getProxiedData').then((interception) => {
      expect(interception.request.url).to.include('/api/proxy/external-service/some-resource');
      expect(interception.response.statusCode).to.eq(200);
      // Ensure the UI displays data correctly after the proxied call
      cy.contains('Data from /external-service/some-resource').should('be.visible');
    });
  });
});