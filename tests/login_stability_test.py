import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Fixtures for WebDriver Initialization ---
@pytest.fixture(params=["chrome", "firefox"])
def setup_driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()  # Assumes chromedriver is in PATH
    elif request.param == "firefox":
        driver = webdriver.Firefox()  # Assumes geckodriver is in PATH
    else:
        raise ValueError("Unsupported browser")
    driver.implicitly_wait(10) # Implicit wait for elements to appear
    yield driver
    driver.quit()

# --- Helper Functions ---
def login(driver, username, password):
    driver.get("http://your-application-url.com/login") # Replace with your application's login URL
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

def verify_successful_login(driver):
    # This assumes a unique element appears after successful login, e.g., a dashboard header
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "dashboard-header")))
    assert "dashboard" in driver.current_url

def verify_error_message(driver, error_message_text):
    error_message_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "error-message"))
    )
    assert error_message_text in error_message_element.text

# --- Test Cases ---

def test_successful_login_admin(setup_driver):
    driver = setup_driver
    login(driver, "admin", "adminpassword") # Replace with valid admin credentials
    verify_successful_login(driver)

def test_successful_login_user(setup_driver):
    driver = setup_driver
    login(driver, "user1", "userpassword") # Replace with valid user credentials
    verify_successful_login(driver)

def test_invalid_credentials_login(setup_driver):
    driver = setup_driver
    login(driver, "invaliduser", "invalidpassword")
    verify_error_message(driver, "Invalid username or password") # Adjust expected error message

@pytest.mark.flaky(reruns=3) # Rerun flaky tests up to 3 times
def test_intermittent_login_with_delay(setup_driver):
    driver = setup_driver
    # Simulate network latency or API delay (e.g., by using a proxy or mocking server in a real scenario)
    # For this example, we'll introduce a simple time.sleep before verifying login
    # In a real environment, this would involve more sophisticated network condition simulation.
    login(driver, "intermittent_user", "intermittent_password") # Use credentials that might fail intermittently
    time.sleep(5)  # Simulate a delay that might cause a session token issue
    try:
        verify_successful_login(driver)
    except Exception: # Catch any exception, specifically looking for session token issues
        driver.refresh() # Try refreshing to see if it resolves
        try:
            verify_successful_login(driver)
        except Exception as e:
            # If still failing, check for the specific 'Invalid session token' error
            if "Invalid session token" in driver.page_source:
                pytest.fail(f"Intermittent 'Invalid session token' error detected: {e}")
            else:
                raise e

# You might add more tests for different roles, edge cases, and specific error messages here.
