
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()  # You can use other browsers like Firefox, Edge
    yield driver
    driver.quit()

def test_consistent_login(browser):
    """Verify users can log in consistently without 'Invalid session token' errors."""
    browser.get("http://localhost:3000/login")  # Replace with your application's login URL
    
    # Wait for the login form to be visible
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    
    # Input credentials (replace with actual test credentials)
    browser.find_element(By.ID, "username").send_keys("testuser")
    browser.find_element(By.ID, "password").send_keys("testpassword")
    browser.find_element(By.ID, "loginButton").click()
    
    # Wait for successful login or error message
    WebDriverWait(browser, 10).until(
        EC.url_contains("/dashboard") or EC.presence_of_element_located((By.ID, "errorMessage"))
    )
    
    # Assert no 'Invalid session token' error message is displayed
    error_message_elements = browser.find_elements(By.ID, "errorMessage")
    assert not any("Invalid session token" in elem.text for elem in error_message_elements),
        "'Invalid session token' error found during login."
    
    # Optional: Verify user is on dashboard if login is successful
    if "/dashboard" in browser.current_url:
        assert "Dashboard" in browser.title

def test_multiple_login_attempts(browser):
    """Test multiple login attempts to ensure consistency and no session token issues."""
    for i in range(3):
        test_consistent_login(browser)
        # Logout for the next attempt (replace with your application's logout URL)
        browser.get("http://localhost:3000/logout") 
        WebDriverWait(browser, 10).until(
            EC.url_contains("/login")
        )
        time.sleep(1) # Small delay between login attempts

