import os

class Config:
    # Flask configuration
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    # HCAT Notification Service base URL (for internal webhook calls)
    NOTIFICATION_SERVICE_BASE_URL = os.environ.get('NOTIFICATION_SERVICE_BASE_URL', 'http://127.0.0.1:5001')

    # Data storage configuration
    DATA_FILE = os.environ.get('DATA_FILE', 'data.json')

    # Scheduler configuration
    SCHEDULER_RUN_IMMEDIATELY = os.environ.get('SCHEDULER_RUN_IMMEDIATELY', 'True').lower() == 'true'
    # APScheduler configuration can be extended here if needed

    # Notification Channel Configurations (Examples - use environment variables for production)
    # Email
    EMAIL_SMTP_SERVER = os.environ.get('EMAIL_SMTP_SERVER', 'smtp.mailtrap.io')
    EMAIL_SMTP_PORT = int(os.environ.get('EMAIL_SMTP_PORT', 2525))
    EMAIL_SENDER_EMAIL = os.environ.get('EMAIL_SENDER_EMAIL', 'your_email@example.com')
    EMAIL_SENDER_PASSWORD = os.environ.get('EMAIL_SENDER_PASSWORD', None) # Use an app-specific password/token

    # Slack
    SLACK_WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/TEXAMPLE/BEXAMPLE/XXXXXXXXXXXXXX')

    # SMS (e.g., Twilio)
    SMS_ACCOUNT_SID = os.environ.get('SMS_ACCOUNT_SID', None)
    SMS_AUTH_TOKEN = os.environ.get('SMS_AUTH_TOKEN', None)
    SMS_FROM_PHONE_NUMBER = os.environ.get('SMS_FROM_PHONE_NUMBER', None)

    # Retry mechanism for notifications
    NOTIFICATION_MAX_RETRIES = int(os.environ.get('NOTIFICATION_MAX_RETRIES', 3))
    NOTIFICATION_RETRY_DELAY_SECONDS = int(os.environ.get('NOTIFICATION_RETRY_DELAY_SECONDS', 60))

    @staticmethod
    def init_app(app):
        # Any app-specific configurations can be applied here
        pass
