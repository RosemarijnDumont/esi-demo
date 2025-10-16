
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def browser():
    driver = webdriver.Chrome()  # or Firefox, Edge
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_successful_login_and_dashboard_access(browser):
    browser.get("http://localhost:8000/login")
    browser.find_element(By.ID, "username").send_keys("testuser")
    browser.find_element(By.ID, "password").send_keys("password123")
    browser.find_element(By.ID, "login_button").click()

    WebDriverWait(browser, 10).until(
        EC.url_contains("/dashboard")
    )
    assert "Dashboard" in browser.title
    assert browser.find_element(By.ID, "dashboard_welcome_message").is_displayed()

def test_data_entry_from_mobile_and_web_sync(browser):
    # This would typically involve a separate mobile app test automation, but for E2E
    # we simulate the effect or use a direct API call for mobile entry
    # For this example, we'll assume a new entry appears on the dashboard after a 'mobile' action

    # Simulate a mobile entry (e.g., via a direct API call to the backend for testing)
    # requests.post("http://localhost:8000/api/mobile/entry", json={"user_id": 1, "content": "E2E Mobile Entry"})

    browser.get("http://localhost:8000/dashboard")
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'E2E Mobile Entry')]"))
    )
    assert browser.find_element(By.XPATH, "//div[contains(text(), 'E2E Mobile Entry')]").is_displayed()
