import requests
import json

class CRMIntegration:
    def __init__(self, crm_api_base_url, crm_api_key):
        self.crm_api_base_url = crm_api_base_url
        self.crm_api_key = crm_api_key
        self.headers = {
            "Authorization": f"Bearer {self.crm_api_key}",
            "Content-Type": "application/json"
        }

    def create_ticket(self, customer_email, subject, message):
        endpoint = f"{self.crm_api_base_url}/tickets"
        payload = {
            "customer_email": customer_email,
            "subject": subject,
            "description": message,
            "status": "new"
        }
        try:
            response = requests.post(endpoint, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status() # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating CRM ticket: {e}")
            return None

    def update_ticket_status(self, ticket_id, status):
        endpoint = f"{self.crm_api_base_url}/tickets/{ticket_id}"
        payload = {
            "status": status
        }
        try:
            response = requests.put(endpoint, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating CRM ticket {ticket_id}: {e}")
            return None

    def search_tickets(self, query_params):
        endpoint = f"{self.crm_api_base_url}/tickets"
        try:
            response = requests.get(endpoint, headers=self.headers, params=query_params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching CRM tickets: {e}")
            return None

# Example usage:
# crm = CRMIntegration("https://api.examplecrm.com", "your_crm_api_key")
# crm.create_ticket("test@example.com", "Urgent Issue", "My product is not working.")
