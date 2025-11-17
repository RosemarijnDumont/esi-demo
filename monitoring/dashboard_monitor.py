import requests
import time
import os
from datetime import datetime

# Configuration for monitoring
MONITOR_URL = os.getenv("MONITOR_DASHBOARD_URL", "http://your-production-dashboard.com") # Replace with actual production URL
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL_SECONDS", 300)) # Default to 5 minutes
ACCEPTABLE_LOAD_TIME = 3 # seconds, should match the performance test threshold
LOG_FILE = "dashboard_monitoring.log"

def log_performance_data(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def check_dashboard_load_time(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10) # Set a reasonable timeout for the request
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        end_time = time.time()
        load_time = end_time - start_time
        return load_time
    except requests.exceptions.Timeout:
        log_performance_data(f"Error: Request to {url} timed out.")
        return -1 # Indicate a timeout
    except requests.exceptions.RequestException as e:
        log_performance_data(f"Error fetching {url}: {e}")
        return -1 # Indicate a general request error

def continuous_dashboard_monitoring():
    log_performance_data("Starting continuous dashboard monitoring...")
    while True:
        load_time = check_dashboard_load_time(MONITOR_URL)

        if load_time > 0: # Only process if no error occurred
            if load_time > ACCEPTABLE_LOAD_TIME:
                log_performance_data(f"ALERT: Dashboard load time ({load_time:.2f}s) exceeded acceptable threshold ({ACCEPTABLE_LOAD_TIME}s) for {MONITOR_URL}")
            else:
                log_performance_data(f"Dashboard load time for {MONITOR_URL}: {load_time:.2f}s (within acceptable limits)")
        
        time.sleep(MONITOR_INTERVAL)

if __name__ == "__main__":
    # To run this monitor:
    # 1. Set the MONITOR_DASHBOARD_URL environment variable to your production dashboard URL.
    # 2. Optionally, set MONITOR_INTERVAL_SECONDS for the check frequency.
    # Example: MONITOR_DASHBOARD_URL="http://prod.example.com/dashboard" python monitoring/dashboard_monitor.py
    continuous_dashboard_monitoring()
