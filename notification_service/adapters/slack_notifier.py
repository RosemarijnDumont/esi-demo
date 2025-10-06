import logging
import requests
from notification_service.adapters.base_notifier import BaseNotifier

class SlackNotifier(BaseNotifier):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def send(self, recipient: str, subject: str, message: str) -> bool:
        """
        Sends a Slack notification to a specified channel/user via webhook.
        The 'recipient' in this context is often ignored or used to specify a channel override
        if the webhook supports it, or simply for logging.
        """
        log_prefix = f"Slack notification to {recipient} for '{subject}': "
        logging.info(f"{log_prefix}Attempting to send.")
        
        # Customize the Slack message payload as needed
        slack_message = {
            "text": f"*{subject}*\n{message}",
            "channel": recipient # Assume recipient is a channel ID or name (e.g., #general, @user)
        }

        try:
            response = requests.post(self.webhook_url, json=slack_message)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            logging.info(f"{log_prefix}Successfully sent. Response: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"{log_prefix}Failed to send: {e}")
            return False
