
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
STAGE_URL = "http://staging.example.com/dashboard"  # Replace with actual staging URL
PROD_URL = "http://production.example.com/dashboard" # Replace with actual production URL
LOAD_TIMEOUT = 30  # Maximum time to wait for the dashboard to load in seconds
ACCEPTABLE_LOAD_TIME = 3  # Acceptable dashboard load time in seconds

@pytest.fixture(scope="module")
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for CI/CD environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def get_dashboard_load_time(driver, url):
    driver.get(url)
    start_time = time.time()
    try:
        # Wait for a specific element on the dashboard to be visible,
        # indicating the page has loaded. Adjust the locator as needed.
        WebDriverWait(driver, LOAD_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "dashboard-main-content"))  # Replace with a real element ID
        )
        end_time = time.time()
        load_time = end_time - start_time
        print(f"Dashboard load time for {url}: {load_time:.2f} seconds")
        return load_time
    except Exception as e:
        pytest.fail(f"Dashboard did not load within {LOAD_TIMEOUT} seconds for {url}: {e}")

def test_dashboard_baseline_load_time(setup_driver):
    driver = setup_driver
    baseline_load_time = get_dashboard_load_time(driver, STAGE_URL)
    pytest.baseline_load_time = baseline_load_time # Store for comparison
    assert baseline_load_time < LOAD_TIMEOUT, f"Baseline dashboard load time ({baseline_load_time:.2f}s) exceeded timeout ({LOAD_TIMEOUT}s)"
    print(f"Baseline dashboard load time: {baseline_load_time:.2f} seconds")

def test_dashboard_post_fix_load_time_staging(setup_driver):
    driver = setup_driver
    post_fix_load_time = get_dashboard_load_time(driver, STAGE_URL)

    # Compare against baseline if available, otherwise just check against acceptable time
    if hasattr(pytest, 'baseline_load_time'):
        baseline_load_time = pytest.baseline_load_time
        assert post_fix_load_time < baseline_load_time, \
            f"Dashboard load time increased after fix! Was {baseline_load_time:.2f}s, now {post_fix_load_time:.2f}s"
        print(f"Post-fix dashboard load time on staging: {post_fix_time:.2f} seconds (Baseline: {baseline_load_time:.2f}s)")
    else:
        print("Baseline load time not available for direct comparison. Ensure baseline test runs first.")

    assert post_fix_load_time < ACCEPTABLE_LOAD_TIME, \
        f"Dashboard post-fix load time ({post_fix_load_time:.2f}s) exceeded acceptable threshold ({ACCEPTABLE_LOAD_TIME}s)"
    print(f"Post-fix dashboard load time on staging: {post_fix_load_time:.2f} seconds")

# Although this agent focuses on pre/post-fix, including a production check is good for continuous monitoring.
def test_dashboard_production_load_time(setup_driver):
    driver = setup_driver
    prod_load_time = get_dashboard_load_time(driver, PROD_URL)
    assert prod_load_time < ACCEPTABLE_LOAD_TIME, \
        f"Dashboard production load time ({prod_load_time:.2f}s) exceeded acceptable threshold ({ACCEPTABLE_LOAD_TIME}s)"
    print(f"Production dashboard load time: {prod_load_time:.2f} seconds")

