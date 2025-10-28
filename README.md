# Testing for API Key Exposure Mitigation

This project contains comprehensive tests designed to ensure that API keys are no longer exposed in browser DevTools after implementing server-side proxying for sensitive API requests.

## Table of Contents

- [Setup](#setup)
- [Running Tests](#running-tests)
    - [End-to-End Tests](#end-to-end-tests)
    - [Negative Testing](#negative-testing)
    - [Performance Testing (Manual/Placeholder)](#performance-testing-manualplaceholder)
    - [Security Review (Manual/Placeholder)](#security-review-manualplaceholder)
    - [Documentation Verification (Manual/Placeholder)](#documentation-verification-manualplaceholder)
- [Acceptance Criteria](#acceptance-criteria)

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Install dependencies (for Playwright and Requests):**

    ```bash
    pip install playwright pytest requests pytest-playwright
    playwright install
    ```

3.  **Ensure your application is running:**

    The tests assume your application is running on `http://localhost:3000`. If your application runs on a different port or host, please update the `BASE_URL` variable in `tests/e2e/test_api_key_exposure.py`.

    ```bash
    # Example command to start your application (replace with your actual command)
    npm start
    # or
    python app.py
    ```

## Running Tests

### End-to-End Tests

These tests verify that API keys are not exposed in DevTools and that API requests are made from the server-side.

To run the end-to-end tests:

```bash
pytest tests/e2e/test_api_key_exposure.py --headed # Use --headed to see the browser UI
```

**Before running:**

*   **Update `sensitive_api_keys`:** In `tests/e2e/test_api_key_exposure.py`, update the `sensitive_api_keys` list with partial or full strings of the API keys you expect *not* to see in the browser's network tab.
*   **Update URLs:** Adjust `BASE_URL`, `/server-side-data-page`, and `/api/proxied-data` in the tests to match your application's actual endpoints.

### Negative Testing

This test verifies that unauthorized attempts to access protected resources directly (bypassing the server-side proxy) are blocked.

This test is part of the `tests/e2e/test_api_key_exposure.py` suite. Run it as described above.

**Before running:**

*   **Update `direct_api_url` and `ATTEMPTED_API_KEY`:** In `test_api_key_exposure.py`, update `direct_api_url` to an API endpoint that should now be protected by server-side proxying, and `ATTEMPTED_API_KEY` to simulate an attacker's attempt.

### Performance Testing (Manual/Placeholder)

The `test_performance_impact` function in `test_api_key_exposure.py` is a placeholder. Comprehensive performance testing requires dedicated tools and a baseline.

**Manual Steps:**

1.  **Establish Baseline:** Before implementing server-side proxying, measure key performance indicators (KPIs) such as page load times, API response times, and server resource utilization under various load conditions.
2.  **Use Performance Testing Tools:** Utilize tools like [JMeter](https://jmeter.apache.org/)/[Locust](https://locust.io/) to simulate user load and measure response times for the affected API calls.
3.  **Compare Results:** Compare the performance metrics after the change against the established baseline and your defined Service Level Objectives (SLOs) to ensure there is no unacceptable latency introduced.

### Security Review (Manual/Placeholder)

The `test_security_review_placeholder` function in `test_api_key_exposure.py` indicates a manual step.

**Manual Steps:**

1.  **Collaborate with Security Team:** Work closely with the security team to schedule and conduct a thorough security review of the implemented changes.
2.  **Penetration Testing:** Engage in penetration testing to actively try and bypass the new security measures and confirm the vulnerability is resolved.
3.  **Obtain Confirmation:** Get official confirmation from the security team that the API key exposure vulnerability has been successfully mitigated.

### Documentation Verification (Manual/Placeholder)

The `test_documentation_placeholder` function in `test_api_key_exposure.py` indicates a manual step.

**Manual Steps:**

1.  **Review Documentation:** Verify that all relevant documentation (e.g., developer guides, API documentation, security policies) has been updated to reflect the new secure API key handling process.
2.  **Ensure Clarity:** Confirm that the documentation clearly explains how developers should now interact with APIs that require server-side proxying and the reasons behind this change.

## Acceptance Criteria

Upon successful completion of these tests and manual steps, the following acceptance criteria should be met:

1.  **API keys are no longer visible in the browser's DevTools network tab.** (Verified by `test_api_keys_not_exposed_in_devtools`)
2.  **All API requests containing sensitive keys are made from the server-side.** (Verified by `test_server_side_api_requests`)
3.  **Existing integrations continue to function correctly after the change.** (To be covered by running existing integration/system tests, not explicit in this file, but assumed to be part of the overall test suite execution plan.)
4.  **A security review confirms the vulnerability is resolved.** (To be confirmed by the security team.)
5.  **Documentation is updated to reflect the new secure API key handling process.** (To be manually verified.)
