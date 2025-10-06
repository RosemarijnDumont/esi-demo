import requests
import json

class EmailServiceIntegration:
    def __init__(self, email_service_api_base_url, email_service_api_key):
        self.email_service_api_base_url = email_service_api_base_url
        self.email_service_api_key = email_service_api_key
        self.headers = {
            "Authorization": f"Bearer {self.email_service_api_key}",
            "Content-Type": "application/json"
        }

    def send_email(self, to_email, subject, body, template_id=None, template_vars=None):
        endpoint = f"{self.email_service_api_base_url}/send"
        payload = {
            "to": to_email,
            "subject": subject,
            "body": body
        }
        if template_id:
            payload["template_id"] = template_id
            payload["template_vars"] = template_vars if template_vars else {}

        try:
            response = requests.post(endpoint, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending email: {e}")
            return None

    def get_email_templates(self):
        endpoint = f"{self.email_service_api_base_url}/templates"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching email templates: {e}")
            return None

    def update_email_template(self, template_id, new_content):
        endpoint = f"{self.email_service_api_base_url}/templates/{template_id}"
        payload = {
            "content": new_content
        }
        try:
            response = requests.put(endpoint, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating email template {template_id}: {e}")
            return None

# Example usage:
# email_service = EmailServiceIntegration("https://api.exampleemailservice.com", "your_email_api_key")
# email_service.send_email("customer@example.com", "Your Support Request", "We have received your request.")
