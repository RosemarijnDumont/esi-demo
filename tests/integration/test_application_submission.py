
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# Configuration
BASE_URL = "http://staging.clientonboardingportal.com"
ADMIN_API_URL = "http://adminapi.clientonboardingportal.com"
USERNAME = "testuser"
PASSWORD = "testpass"

@pytest.fixture(scope="module", params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {request.param}")
    driver.maximize_window()
    yield driver
    driver.quit()

def login(driver):
    driver.get(f"{BASE_URL}/login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    ).send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, 10).until(
        EC.url_contains(f"{BASE_URL}/dashboard")
    )

def complete_id_verification(driver):
    # Simulate ID verification completion, assuming this leads to the application form
    driver.get(f"{BASE_URL}/id-verification")
    # In a real scenario, you'd interact with upload elements, but for this test,
    # we assume a successful upload redirects to the application form or enables it.
    # For now, we'll directly navigate to the application form after a brief wait
    # as if ID verification was completed.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "id-upload-input"))
    ).send_keys("/path/to/dummy_id.pdf") # Replace with a test file path
    driver.find_element(By.ID, "upload-button").click()
    WebDriverWait(driver, 20).until(
        EC.url_contains(f"{BASE_URL}/application-form") or
        EC.visibility_of_element_located((By.ID, "continue-to-application-button"))
    )
    if driver.current_url != f"{BASE_URL}/application-form":
        driver.find_element(By.ID, "continue-to-application-button").click()
        WebDriverWait(driver, 10).until(
            EC.url_contains(f"{BASE_URL}/application-form")
        )


class TestApplicationSubmission:

    def test_application_form_submission_success(self, driver):
        login(driver)
        complete_id_verification(driver)

        # Fill out required application form fields
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "first-name"))
        ).send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "email").send_keys("john.doe@example.com")
        driver.find_element(By.ID, "phone").send_keys("123-456-7890")
        driver.find_element(By.ID, "address-line1").send_keys("123 Test St")
        driver.find_element(By.ID, "city").send_keys("Testville")
        driver.find_element(By.ID, "zip-code").send_keys("12345")
        # Assuming a dropdown for state/province
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "state"))
        ).send_keys("CA")

        # Submit the form
        submit_button = driver.find_element(By.ID, "submit-application-button")
        submit_button.click()

        # Verify successful submission - check for success message or redirect
        WebDriverWait(driver, 20).until(
            EC.url_contains(f"{BASE_URL}/submission-success") or
            EC.presence_of_element_located((By.ID, "success-message"))
        )
        assert "500 Internal Server Error" not in driver.page_source
        print("Application form submitted successfully, no 500 error found.")

        # Verify backend processing (example using an admin API)
        submitted_applications = self._get_submitted_applications()
        assert any("john.doe@example.com" in app["email"] for app in submitted_applications)
        print("Application successfully verified in backend.")

    def _get_submitted_applications(self):
        """Helper to fetch submitted applications from a mock Admin API."""
        try:
            response = requests.get(f"{ADMIN_API_URL}/applications", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to Admin API: {e}")

