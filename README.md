# esi-demo
adapt and test

## Testing Strategy

This project employs a comprehensive testing strategy to ensure the quality and reliability of the application, focusing on unit, integration, end-to-end, performance, and regression testing. The goal is to address critical bugs, prevent regressions, and ensure a smooth user experience.

### Unit Tests
Located in `tests/unit/`, these tests focus on individual components and services. For example, `tests/unit/test_authentication.py` verifies the functionality of the authentication service, including user login and session token management.

To run unit tests:
```bash
pytest tests/unit/
```

### Integration Tests
Located in `tests/integration/`, these tests verify the interaction between different modules or services. `tests/integration/test_data_sync.py` ensures that data synchronization between mobile and web applications works as expected.

To run integration tests:
```bash
pytest tests/integration/
```

### End-to-End (E2E) Tests
Located in `tests/e2e/`, these tests simulate real user scenarios using a web browser. `tests/e2e/test_full_user_flow.py` covers essential user journeys like successful login, dashboard access, and data synchronization verification. Requires `selenium` and a compatible web driver (e.g., ChromeDriver).

To run E2E tests:
```bash
pytest tests/e2e/
```

### Performance Tests
Located in `tests/performance/`, these tests use Locust to conduct load and stress testing on critical paths like login, dashboard, and reports pages. This helps identify bottlenecks and ensure the application performs well under high traffic.

To run performance tests (ensure Locust is installed: `pip install locust`):
```bash
locust -f tests/performance/locustfile.py
```
Then open your browser to `http://0.0.0.0:8089` to start the test.

### Regression Tests
Located in `tests/regression/`, these tests are designed to ensure that previously fixed bugs do not re-emerge. `tests/regression/test_regression_suite.py` includes tests for login stability, dashboard load times, and mobile data synchronization.

To run regression tests:
```bash
pytest tests/regression/
```

### User Acceptance Testing (UAT)
UAT will be conducted with a representative group of users to validate the overall experience and functionality in a real-world scenario. This involves manual testing against the defined acceptance criteria and gathering user feedback.

**Acceptance Criteria for UAT:**
1.  Users can log in consistently without "Invalid session token" errors.
2.  Dashboard and Reports pages load within 2-3 seconds.
3.  All entries added via mobile app sync immediately with the web app.
4.  All notifications (email and in-app) trigger consistently and without delay.
5.  UI elements display correctly on all screen sizes and dark mode contrast is optimized for readability.
