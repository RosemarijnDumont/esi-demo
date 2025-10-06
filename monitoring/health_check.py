import requests
import os

def check_service_health(service_name, url, expected_status_code=200):
    """Performs a health check on a given service URL."""
    try:
        response = requests.get(url, timeout=5) # 5-second timeout
        if response.status_code == expected_status_code:
            print(f"[HEALTH_CHECK] {service_name} is UP (Status: {response.status_code})")
            return True
        else:
            print(f"[HEALTH_CHECK] {service_name} is DOWN (Status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[HEALTH_CHECK] {service_name} is DOWN (Error: {e})")
        return False

def run_all_health_checks():
    """Runs health checks for all integrated services."""
    crm_api_base_url = os.getenv("CRM_API_BASE_URL", "http://localhost:8080/crm") # Default for local testing
    email_service_api_base_url = os.getenv("EMAIL_SERVICE_API_BASE_URL", "http://localhost:8081/email") # Default for local testing

    print("\n--- Running System Health Checks ---")
    crm_health = check_service_health("CRM Service", f"{crm_api_base_url}/health")
    email_health = check_service_health("Email Service", f"{email_service_api_base_url}/health")
    print("--- Health Checks Complete ---")

    return crm_health and email_health

if __name__ == "__main__":
    if run_all_health_checks():
        print("All critical services are healthy.")
    else:
        print("One or more critical services are unhealthy.")
