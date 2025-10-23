
import requests
import logging

class EmailServiceProvider:
    """
    A simplified client for sending emails via an external email service provider
    (e.g., SendGrid, Mailgun). This is a placeholder and should be replaced with
    actual integration code for the chosen email service.
    """
    def __init__(self, api_key: str, base_url: str = "https://api.sendgrid.com/v3/mail/send"):
        self.api_key = api_key
        self.base_url = base_url # Will vary based on ESP
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.from_email = "no-reply@yourcompany.com" # Customize your sender email
        logging.info(f"EmailServiceProvider initialized with base URL: {self.base_url}")

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Sends an email using the configured email service provider.
        """
        # This payload structure is an example, it will vary greatly per ESP.
        # This example roughly mimics SendGrid's API structure.
        payload = {
            "personalizations": [
                {
                    "to": [
                        {"email": to_email}
                    ],
                    "subject": subject
                }
            ],
            "from": {
                "email": self.from_email
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": body
                }
            ]
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=10)
            response.raise_for_status() # Raise an exception for HTTP errors
            logging.info(f"Successfully sent email to {to_email} with subject '{subject}'.")
            return True
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error sending email to {to_email}: {e.response.status_code} - {e.response.text}", exc_info=True)
            return False
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error sending email to {to_email}: {e}", exc_info=True)
            return False
        except requests.exceptions.Timeout:
            logging.error(f"Request to send email to {to_email} timed out.", exc_info=True)
            return False
        except requests.exceptions.RequestException as e:
            logging.error(f"Error sending email to {to_email}: {e}", exc_info=True)
            return False
