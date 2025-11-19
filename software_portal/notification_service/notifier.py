import smtplib
from email.mime.text import MIMEText
import requests
import json

class Notifier:
    """
    Handles sending notifications via email and chat (e.g., Slack/Teams).
    """
    def __init__(self, smtp_server=None, smtp_port=None, smtp_user=None, smtp_password=None, 
                 slack_webhook_url=None, teams_webhook_url=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.slack_webhook_url = slack_webhook_url
        self.teams_webhook_url = teams_webhook_url

    def send_email(self, to_email, subject, body):
        """
        Sends an email notification.
        """
        if not all([self.smtp_server, self.smtp_port, self.smtp_user, self.smtp_password]):
            print("SMTP not configured. Skipping email notification.")
            return False
        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = to_email

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            print(f"Email sent to {to_email} with subject '{subject}'.")
            return True
        except Exception as e:
            print(f"Error sending email to {to_email}: {e}")
            return False

    def send_slack_message(self, message, channel=None):
        """
        Sends a message to a Slack channel via webhook.
        """
        if not self.slack_webhook_url:
            print("Slack webhook URL not configured. Skipping Slack notification.")
            return False

        payload = {"text": message}
        if channel:
            payload["channel"] = channel

        try:
            response = requests.post(self.slack_webhook_url, data=json.dumps(payload), 
                                     headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            print(f"Slack message sent: {message}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending Slack message: {e}")
            return False

    def send_teams_message(self, message):
        """
        Sends a message to a Microsoft Teams channel via webhook.
        """
        if not self.teams_webhook_url:
            print("Teams webhook URL not configured. Skipping Teams notification.")
            return False

        payload = {"text": message}
        try:
            response = requests.post(self.teams_webhook_url, data=json.dumps(payload), 
                                     headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            print(f"Teams message sent: {message}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending Teams message: {e}")
            return False