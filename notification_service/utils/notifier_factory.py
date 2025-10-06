from notification_service.adapters.email_notifier import EmailNotifier
from notification_service.adapters.slack_notifier import SlackNotifier
from notification_service.adapters.sms_notifier import SMSNotifier
from notification_service.adapters.base_notifier import BaseNotifier
import logging

class NotifierFactory:
    @staticmethod
    def get_notifier(channel: str, config: dict = None) -> BaseNotifier or None:
        """
        Factory method to get the appropriate notifier based on the channel.
        Configuration for the notifiers (e.g., API keys, webhook URLs) should ideally 
        come from a central configuration management system or environment variables.
        For this example, we'll use sensible defaults or assume they are pre-configured.
        """
        if config is None: # Load default configs if not provided
            config = {
                "email": {"smtp_server": "smtp.mailtrap.io", "smtp_port": 2525, "sender_email": "your_email@example.com", "sender_password": "your_password"}, # Use Mailtrap for testing
                "slack": {"webhook_url": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"}, # Replace with your Slack webhook
                "sms": {"account_sid": "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "auth_token": "your_auth_token", "from_phone_number": "+15017122661"} # Replace with Twilio credentials
            }
            # In a real application, these should come from environment variables or a secret manager
            logging.warning("Using placeholder/default configurations for notifiers. \n"\
                            "For production, ensure these are loaded securely from environment variables or a secret management system.")

        channel = channel.lower()
        if channel == 'email':
            email_config = config.get('email', {})
            return EmailNotifier(
                smtp_server=email_config.get('smtp_server', 'smtp.mailtrap.io'),
                smtp_port=email_config.get('smtp_port', 2525),
                sender_email=email_config.get('sender_email', 'your_email@example.com'),
                sender_password=email_config.get('sender_password', None)
            )
        elif channel == 'slack':
            slack_config = config.get('slack', {})
            webhook_url = slack_config.get('webhook_url')
            if not webhook_url or "hooks.slack.com" not in webhook_url:
                logging.error("Slack webhook URL is missing or invalid in configuration.")
                return None
            return SlackNotifier(webhook_url=webhook_url)
        elif channel == 'sms':
            sms_config = config.get('sms', {})
            # For real usage, ensure Twilio or similar credentials are provided
            return SMSNotifier(
                account_sid=sms_config.get('account_sid'),
                auth_token=sms_config.get('auth_token'),
                from_phone_number=sms_config.get('from_phone_number')
            )
        else:
            logging.error("Unsupported notification channel: %s", channel)
            return None